"""CP4 U12: grupuri, anomalii, silhouette, bootstrap si compararea surselor.
Rulare: python -X utf8 CP4_analiza.py. Genereaza numai 5 CSV si 3 PNG.
Varianta extinsa este pastrata separat in CP4_analiza_detaliata.py.
"""
from pathlib import Path
import os
ROOT = Path(__file__).resolve().parent
os.environ.setdefault('NUMBA_CACHE_DIR', str(ROOT / '.numba_cache'))
os.environ.setdefault('LOKY_MAX_CPU_COUNT', '1')
import math
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from sklearn.metrics import adjusted_rand_score, silhouette_score, pairwise_distances
from sklearn.preprocessing import StandardScaler
from threadpoolctl import threadpool_limits
import umap

OUT = ROOT / 'CP4_rezultate'
PM = 'RNMCA | PM2.5 mediu (\u00b5g/m\u00b3)'
TEMP = 'Open-Meteo | Temperatura medie (\u00b0C)'
WIND = 'Open-Meteo | Vant mediu (km/h)'
FEATURES = [PM, TEMP, WIND]
SETS = {'RNMCA': [PM], 'OpenMeteo': [TEMP, WIND], 'Combinate': FEATURES}
SEEDS = (42, 21, 123)
BOOTSTRAP = 100
BLOCK_DAYS = 7
COLORS = plt.get_cmap('tab10').colors


def save_csv(rows, filename):
    pd.DataFrame(rows).to_csv(OUT / filename, index=False, encoding='utf-8-sig')


def load_data():
    raw = pd.read_excel(ROOT / 'CP2_matrice.xlsx', sheet_name='Matrice_CP2', engine='openpyxl')
    required = FEATURES + ['Statie', 'Data', 'Interval 6h', 'Anotimp', 'Status interval']
    if not set(required).issubset(raw.columns):
        raise ValueError('Coloanele asteptate lipsesc: ' + str(set(required) - set(raw.columns)))
    data = raw.copy()
    data['Data'] = pd.to_datetime(data['Data'], errors='raise')
    for col in FEATURES:
        data[col] = pd.to_numeric(data[col], errors='coerce')
    complete = data['Status interval'].astype(str).str.strip().str.casefold().eq('complet')
    valid = np.isfinite(data[FEATURES].to_numpy()).all(axis=1)
    data = data.loc[complete & valid].sort_values(['Data', 'Statie', 'Interval 6h']).reset_index(drop=True)
    if data[required].isna().any().any() or data.duplicated(['Statie', 'Data', 'Interval 6h']).any():
        raise ValueError('Metadate lipsa sau identificatori duplicati.')
    if set(data.Statie) != {'B-12', 'B-14', 'B-21', 'B-26'}:
        raise ValueError('Statii neasteptate.')
    data.insert(0, 'observatie_id', np.arange(len(data)))
    return raw, data


def fit_kmeans(z, k, seed=42):
    return KMeans(n_clusters=k, n_init=10, max_iter=300, random_state=seed).fit(z)


def canonical_labels(model, raw_values):
    """Numerele grupurilor se ordoneaza descriptiv dupa PM2.5, temperatura, vant."""
    labels = model.labels_
    means = [tuple(raw_values[labels == k].mean(axis=0)) for k in range(model.n_clusters)]
    order = sorted(range(model.n_clusters), key=lambda k: means[k])
    mapping = {old: new for new, old in enumerate(order)}
    return np.array([mapping[int(k)] for k in labels]), mapping


def safe_silhouette(distances, labels):
    if not 1 < len(np.unique(labels)) < len(labels):
        return float('nan')
    return float(silhouette_score(distances, labels, metric='precomputed'))


def bootstrap_indices(data, count, block_days):
    """Moving-block bootstrap pe zile calendaristice, toate statiile/intervalele impreuna."""
    dates = pd.date_range(data.Data.min(), data.Data.max(), freq='D')
    rows = {pd.Timestamp(d): np.flatnonzero(data.Data.eq(d).to_numpy()) for d in dates}
    if len(dates) < block_days:
        raise ValueError('Prea putine zile pentru bootstrap.')
    result = []
    for b in range(count):
        rng = np.random.default_rng(42000 + b)
        starts = rng.integers(0, len(dates) - block_days + 1, size=math.ceil(len(dates)/block_days))
        drawn = np.concatenate([dates[s:s+block_days].to_numpy() for s in starts])[:len(dates)]
        sampled = np.concatenate([rows[pd.Timestamp(d)] for d in drawn])
        result.append(sampled)
    return result


def anomalies(z):
    model = IsolationForest(n_estimators=300, contamination='auto', random_state=42, n_jobs=1).fit(z)
    score = -model.score_samples(z)
    # Prag percentile, nu o rata de anomalii descoperita automat.
    threshold = float(np.quantile(score, .99))
    return score, score > threshold, threshold


def profile(data, labels, name, method):
    records = []
    for group in np.unique(labels):
        subset = data.loc[labels == group]
        row = dict(set=name, metoda=method, grup=int(group+1), n=len(subset), procent=100*len(subset)/len(data))
        for col, short in zip(FEATURES, ['PM25', 'temperatura', 'vant']):
            row[short+'_medie'] = float(subset[col].mean())
            row[short+'_mediana'] = float(subset[col].median())
            row[short+'_p10'] = float(subset[col].quantile(.1))
            row[short+'_p90'] = float(subset[col].quantile(.9))
        records.append(row)
    return records


def enrich_seed_summary(summary, seedrows):
    seedframe=pd.DataFrame(seedrows)
    for row in summary:
        subset=seedframe[(seedframe['set']==row['set']) & (seedframe['seed']!=42)]
        if row['metoda']=='UMAP':
            row['ari_seed_min']=float(subset['ari_cu_seed42'].min())
            row['ari_seed_medie']=float(subset['ari_cu_seed42'].mean())
        else:
            row['ari_seed_min']=np.nan
            row['ari_seed_medie']=np.nan


def plots(data, labels, summary, profiles):
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    for row, method in enumerate(['PCA','UMAP']):
        for col, name in enumerate(SETS):
            item = labels[(name,method)]
            z, lab = item['z'], item['labels']
            ax = axes[row,col]
            for g in np.unique(lab):
                mask = lab == g
                ax.scatter(z[mask,0], z[mask,1] if z.shape[1]>1 else np.zeros(mask.sum()),
                           s=6, alpha=.45, color=COLORS[g], label=f'G{g+1}')
            mask = item['outliers']
            ax.scatter(z[mask,0], z[mask,1] if z.shape[1]>1 else np.zeros(mask.sum()),
                       marker='x', c='black', s=25, linewidths=.8, label='Candidati anomalii')
            ax.set_title(f'{name} - {method}, k={item["k"]}')
            ax.set_xlabel('PC1' if method=='PCA' else 'UMAP 1')
            ax.set_ylabel(('PC2' if method=='PCA' else 'UMAP 2') if z.shape[1]>1 else 'Axa auxiliara zero')
            ax.legend(fontsize=7, markerscale=1.5)
    fig.suptitle('CP4: partitii K-means si candidati anomalii (n=6.067); seed 42\nCulorile grupurilor nu au identitate comuna intre panouri', fontsize=13)
    fig.tight_layout()
    fig.savefig(OUT/'clustering_anomalii_comparativ.png',dpi=180)
    plt.close(fig)
    # Tabel comparativ pe un singur spatiu original comun.
    fig, ax=plt.subplots(figsize=(13,4.5))
    ax.axis('off')
    rows=[]
    for r in summary:
        rows.append([r['set'],r['metoda'],r['k'],f"{r['silhouette_redus']:.3f}",
                     f"{r['silhouette_original_comun3']:.3f}", f"{r['bootstrap_ari_oob_medie']:.3f}", f"{r['ari_seed_min']:.3f}" if r['metoda']=='UMAP' else '-', r['n_anomalii']])
    t=ax.table(cellText=rows,colLabels=['Set','Spatiu','k','Sil. redus','Sil. comun 3D','ARI boot. OOB','ARI seed min','Candidati*'],loc='center',cellLoc='center')
    t.auto_set_font_size(False); t.set_fontsize(9); t.scale(1,1.8)
    for cell in t.get_celld().values(): cell.set_edgecolor('#d0d5dc')
    ax.set_title('Combinarea surselor stabilizeaza gruparea UMAP intre seed-uri',fontsize=15,pad=15)
    fig.text(.05,.05,'* Prag prestabilit: scor Isolation Forest peste percentila 99; numarul nu estimeaza prevalenta reala.\nBootstrap pe blocuri de 7 zile; embedding fix; scorurile silhouette din spatii diferite nu sunt direct comparabile.\nARI seed min: minimul acordului cu seed 42 pentru UMAP 21 si 123, la k fixat pentru fiecare sursa.',fontsize=8)
    fig.tight_layout(rect=[0,.12,1,1]); fig.savefig(OUT/'tabel_comparatie_CP4.png',dpi=180); plt.close(fig)
    # Evidenta interpretabila: aceleasi date, grupuri ale fiecarei surse, in variabilele fizice.
    fig, axes=plt.subplots(1,3,figsize=(16,5),sharex=True,sharey=True)
    for ax,name in zip(axes,SETS):
        lab=labels[(name,'PCA')]['fixed3']
        for g in np.unique(lab):
            m=lab==g
            ax.scatter(data.loc[m,TEMP], data.loc[m,PM], s=7,alpha=.35,color=COLORS[g],label=f'G{g+1}')
        ax.set(title=f'{name}: PCA + K-means, k=3',xlabel='Temperatura (°C)')
        ax.legend(fontsize=8)
    axes[0].set_ylabel('PM2.5 (µg/m³)')
    fig.suptitle('Comparatie la acelasi k: etichete din fiecare sursa, afisate in aceleasi variabile originale\nGrupurile sunt descriptive; nu demonstreaza cauzalitate sau regimuri naturale distincte',fontsize=12)
    fig.tight_layout(); fig.savefig(OUT/'structura_surse_comparativ.png',dpi=180); plt.close(fig)


def bootstrap_stability(z, reference, k, samples):
    """Reajusteaza K-means; ARI pe zile out-of-bag, reprezentarea si k fixe."""
    scores=[]
    for ix in samples:
        prediction=fit_kmeans(z[ix],k).predict(z)
        oob=~np.isin(np.arange(len(z)),np.unique(ix))
        if oob.sum()<3:
            raise ValueError('Prea putine observatii out-of-bag.')
        # ARI nu necesita alinierea numerelor grupurilor.
        scores.append(adjusted_rand_score(reference[oob],prediction[oob]))
    return dict(bootstrap_ari_oob_medie=float(np.mean(scores)),
                bootstrap_ari_oob_sd=float(np.std(scores,ddof=1)),
                bootstrap_ari_oob_p025=float(np.quantile(scores,.025)),
                bootstrap_ari_oob_p975=float(np.quantile(scores,.975)))


def compare_sources(data,labels):
    """Partitii la acelasi k=3; cat din fiecare grup separat se regaseste in cele combinate."""
    rows=[]
    for method in ['PCA','UMAP']:
        joint=labels[('Combinate',method)]['fixed3']
        for name in ['RNMCA','OpenMeteo']:
            single=labels[(name,method)]['fixed3']
            agreement=float(adjusted_rand_score(single,joint))
            for s in range(3):
                for j in range(3):
                    mask=(single==s)&(joint==j)
                    n=int(mask.sum())
                    row=dict(metoda=method,sursa=name,k_comun=3,grup_sursa=s+1,
                             grup_combinat=j+1,n=n,
                             procent_din_grup_sursa=100*n/int((single==s).sum()),
                             ari_sursa_vs_combinate=agreement)
                    for col,short in zip(FEATURES,['PM25','temperatura','vant']):
                        row[short+'_medie']=float(data.loc[mask,col].mean()) if n else np.nan
                    rows.append(row)
    return rows


def main():
    OUT.mkdir(exist_ok=True)
    _,data=load_data()
    original=data[FEATURES].to_numpy()
    ix=np.sort(np.random.default_rng(42).choice(len(data),min(1000,len(data)),replace=False))
    common=StandardScaler().fit_transform(data[FEATURES])
    common_dist=pairwise_distances(common[ix]); np.fill_diagonal(common_dist,0)
    samples=bootstrap_indices(data,BOOTSTRAP,BLOCK_DAYS)
    summary,profiles,anomalyrows,seedrows=[],[],[],[]
    labels={}
    for name,cols in SETS.items():
        x=StandardScaler().fit_transform(data[cols])
        _,original_flags,_=anomalies(x)
        for method in ['PCA','UMAP']:
            print(f'Analiza: {name} / {method}',flush=True)
            if method=='PCA':
                z=PCA(n_components=min(2,len(cols)),svd_solver='full').fit_transform(x)
            else:
                z=umap.UMAP(n_components=min(2,len(cols)),n_neighbors=15,min_dist=.1,
                            metric='euclidean',random_state=42,n_jobs=1,
                            compatibility_layout=True).fit_transform(x)
            distances=pairwise_distances(z[ix]); np.fill_diagonal(distances,0)
            options=[]
            for k in range(2,7):
                model=fit_kmeans(z,k)
                silhouette=safe_silhouette(distances,model.labels_[ix])
                if np.bincount(model.labels_).min()>=math.ceil(.01*len(data)):
                    options.append((silhouette,k,model))
                if k==3:
                    fixed3,_=canonical_labels(model,original)
            if not options:
                raise ValueError('Nicio partitie eligibila.')
            silhouette,k,model=max(options,key=lambda v:(v[0],-v[1]))
            lab,_=canonical_labels(model,original)
            stability=bootstrap_stability(z,lab,k,samples)
            score,flags,threshold=anomalies(z)
            union=np.count_nonzero(flags|original_flags)
            summary.append(dict(set=name,metoda=method,k=k,
                                silhouette_redus=silhouette,
                                silhouette_original_comun3=safe_silhouette(common_dist,lab[ix]),
                                **stability,n_anomalii=int(flags.sum()),
                                jaccard_anomalii_original=float(np.count_nonzero(flags&original_flags)/union) if union else np.nan,
                                prag_scor_anomalie=threshold))
            labels[(name,method)]=dict(z=z,labels=lab,k=k,fixed3=fixed3,outliers=flags)
            profiles.extend(profile(data,lab,name,method))
            for i in np.flatnonzero(flags):
                anomalyrows.append(dict(set=name,metoda=method,grup=int(lab[i]+1),
                                        scor_anomalie=float(score[i]),
                                        **data.iloc[i][['observatie_id','Statie','Data','Interval 6h','Anotimp']+FEATURES].to_dict()))
            if method=='UMAP':
                for seed in SEEDS:
                    if seed==42:
                        zz,ll=z,lab
                    else:
                        zz=umap.UMAP(n_components=min(2,len(cols)),n_neighbors=15,min_dist=.1,
                                     metric='euclidean',random_state=seed,n_jobs=1,
                                     compatibility_layout=True).fit_transform(x)
                        ll=fit_kmeans(zz,k).labels_
                    dd=pairwise_distances(zz[ix]); np.fill_diagonal(dd,0)
                    seedrows.append(dict(set=name,metoda=method,seed=seed,k_fix=k,
                                         ari_cu_seed42=float(adjusted_rand_score(lab,ll)),
                                         silhouette_redus=safe_silhouette(dd,ll[ix]),
                                         silhouette_original_comun3=safe_silhouette(common_dist,ll[ix])))
            print(f'  k={k}; silhouette={silhouette:.4f}; ARI bootstrap={stability["bootstrap_ari_oob_medie"]:.4f}',flush=True)
    enrich_seed_summary(summary,seedrows)
    save_csv(summary,'comparatie_CP4.csv')
    save_csv(profiles,'profil_grupuri_CP4.csv')
    save_csv(anomalyrows,'anomalii_CP4.csv')
    save_csv(seedrows,'stabilitate_seeduri_CP4.csv')
    save_csv(compare_sources(data,labels),'comparatie_surse_CP4.csv')
    plots(data,labels,summary,profiles)
    print('Finalizat: '+str(OUT),flush=True)
    print('8 fisiere finale: 5 CSV si 3 PNG. Fara exportul etapelor intermediare.',flush=True)


if __name__=='__main__':
    with threadpool_limits(limits=1):
        main()
