"""Analiza CP3 reproductibila. Rulare: python -X utf8 CP3_analiza.py."""
from pathlib import Path
import json
import itertools
import importlib.metadata as metadata
import os

# Keep Numba compilation caches in the writable project, not site-packages.
os.environ.setdefault('NUMBA_CACHE_DIR', str(Path(__file__).resolve().parent / '.numba_cache'))
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import trustworthiness
from sklearn.neighbors import NearestNeighbors
from scipy.linalg import subspace_angles
import umap

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'CP3_rezultate'
SEEDS = (42, 21, 123)
K = 10
FEATURES = ['RNMCA | PM2.5 mediu (µg/m³)', 'Open-Meteo | Temperatura medie (°C)', 'Open-Meteo | Vant mediu (km/h)']
SETS = {'RNMCA': FEATURES[:1], 'OpenMeteo': FEATURES[1:], 'Combinate': FEATURES}


def neighbors(z):
    # X=None excludes each point itself, including when distances are tied.
    return NearestNeighbors(n_neighbors=K).fit(z).kneighbors(return_distance=False)


def overlap(a, b):
    return float(np.mean([len(set(x) & set(y)) / K for x, y in zip(a, b)]))


def scatter(ax, z, stations, title, pca=False):
    for station in sorted(stations.unique()):
        mask = stations.eq(station).to_numpy()
        ax.scatter(z[mask, 0], z[mask, 1] if z.shape[1] > 1 else np.zeros(mask.sum()),
                   s=8, alpha=.5, label=station)
    ax.set(title=title, xlabel='PC1' if pca else 'UMAP 1',
           ylabel=('PC2' if pca else 'UMAP 2') if z.shape[1] > 1 else 'Axa auxiliara (zero)')
    ax.legend(title='Statie', markerscale=2, fontsize=8)


def write_slide():
    out = Path(__file__).resolve().parent / 'CP3_rezultate'
    audit = json.loads((out / 'audit_date.json').read_text(encoding='utf-8'))
    c = pd.read_csv(out / 'comparatie_CP3.csv')
    row = c[(c['set'] == 'Combinate') & (c['perioada'] == 'Integral')].iloc[0]
    better = 'UMAP' if row['trust_UMAP_medie'] > row['trust_PCA'] else 'PCA'
    title = f"{better} păstrează mai bine vecinătățile în reducerea combinată 3→2"
    text = f'''# Slide 2 — Dovada etapei

**Titlu:** {title}

**Unicul element vizual:** `tabel_slide2.png` (include toate cele trei surse).

**Surse și perioadă:** RNMCA (PM2.5) și Open-Meteo (temperatură, vânt), București, {audit['inceput']} – {audit['sfarsit']}.

**Date:** {audit['n_folosit']:,} observații complete din {audit['randuri_initiale']:,}; patru stații B-12, B-14, B-21, B-26; unitate stație × zi × 6 ore. RNMCA: 1 variabilă, Open-Meteo: 2, combinate: 3.

**Protocol:** StandardScaler; PCA/UMAP ajustate pe toate observațiile eligibile; trustworthiness cu k=10 pe același eșantion reproductibil de 1.000 observații; dimensiuni 1→1, 2→2 și 3→2; MSE în spațiul standardizat. UMAP: n_neighbors=15, min_dist=0.1, metrică euclidiană; seed-uri 42, 21, 123. Stabilitate prin scoruri și vecini comuni între seed-uri și reajustare pe două subperioade separate la {audit['prag_temporal']}.

**Interpretare:** Pe datele combinate, PCA păstrează {100*row['var_explicata_PCA']:.4f}% din varianță (MSE={row['eroare_reconstructie_PCA']:.6f}), iar trustworthiness este {row['trust_PCA']:.6f} pentru PCA și {row['trust_UMAP_medie']:.6f} ± {row['trust_UMAP_std']:.6f} pentru UMAP (medie ± SD între seed-uri), favorizând {better} pentru vecinătățile locale în acest protocol.

**Limitare:** Numai setul combinat are reducere dimensională efectivă; PCA 1→1 și 2→2 păstrează toate dimensiunile. Rezultatele sunt exploratorii, fără validare predictivă. Media pe trei seed-uri nu este interval de încredere.

**Repository GitHub:** https://github.com/LitaAna/Proiect_MEDE
'''
    (out / 'slide2.md').write_text(text, encoding='utf-8')
    print(text)



def main():
    OUT.mkdir(exist_ok=True)
    raw = pd.read_excel(ROOT / 'CP2_matrice.xlsx', sheet_name='Matrice_CP2', engine='openpyxl')
    required = FEATURES + ['Statie', 'Data', 'Interval 6h', 'Status interval']
    missing = set(required) - set(raw.columns)
    if missing:
        raise ValueError(f'Coloane absente: {missing}')
    data = raw.copy()
    data['Data'] = pd.to_datetime(data['Data'], errors='raise')
    for col in FEATURES:
        data[col] = pd.to_numeric(data[col], errors='coerce')
    finite = np.isfinite(data[FEATURES].to_numpy()).all(axis=1)
    complete = data['Status interval'].astype(str).str.strip().str.casefold().eq('complet')
    data = data.loc[complete & finite].copy().sort_values(['Data', 'Statie', 'Interval 6h']).reset_index(drop=True)
    if data[required].isna().any().any() or data.duplicated(['Statie', 'Data', 'Interval 6h']).any():
        raise ValueError('Metadate lipsa sau unitati statie/zi/interval duplicate.')
    if set(data['Statie']) != {'B-12', 'B-14', 'B-21', 'B-26'}:
        raise ValueError('Lista statiilor difera de protocol.')
    dates = np.sort(data['Data'].unique())
    cutoff = pd.Timestamp(dates[len(dates)//2])
    periods = {'Integral': data, 'Prima_subperioada': data[data['Data'] < cutoff],
               'A_doua_subperioada': data[data['Data'] >= cutoff]}
    audit = {'randuri_initiale': len(raw), 'status': raw['Status interval'].value_counts().to_dict(),
             'lipsa_initial': raw.isna().sum().to_dict(), 'complete_cu_valori_nefinite': int((complete & ~finite).sum()),
             'n_folosit': len(data), 'inceput': str(data['Data'].min().date()), 'sfarsit': str(data['Data'].max().date()),
             'prag_temporal': str(cutoff.date()), 'coloane_tipuri': raw.dtypes.astype(str).to_dict(),
             'versiuni': {p: metadata.version(p) for p in ['pandas', 'openpyxl', 'numpy', 'scipy', 'scikit-learn', 'matplotlib', 'umap-learn', 'numba', 'llvmlite']}}
    (OUT / 'audit_date.json').write_text(json.dumps(audit, indent=2, ensure_ascii=False), encoding='utf-8')
    data[['Statie', 'Data', 'Interval 6h']].to_csv(OUT / 'observatii_folosite.csv', index=False, encoding='utf-8-sig')
    results, stability, bases = [], [], {}
    for period, frame in periods.items():
        ix = np.sort(np.random.default_rng(42).choice(len(frame), min(1000, len(frame)), replace=False))
        for name, cols in SETS.items():
            print(f'{period}: {name}, n={len(frame)}', flush=True)
            x = StandardScaler().fit_transform(frame[cols])
            dim = min(2, len(cols))
            pca = PCA(n_components=dim, svd_solver='full')
            p = pca.fit_transform(x)
            bases[(period, name)] = pca.components_.T
            tp = float(trustworthiness(x[ix], p[ix], n_neighbors=K))
            ev = float(pca.explained_variance_ratio_.sum())
            mse = float(np.mean((x - pca.inverse_transform(p))**2))
            embeddings, trusts = {}, {}
            base = dict(set=name, perioada=period, inceput=str(frame['Data'].min().date()),
                        sfarsit=str(frame['Data'].max().date()), n=len(frame), n_evaluare=len(ix),
                        variabile=len(cols), dimensiuni=dim, reducere_reala=dim < len(cols),
                        var_explicata_PCA=ev, eroare_reconstructie_PCA=mse, trust_PCA=tp)
            for seed in SEEDS:
                u = umap.UMAP(n_components=dim, n_neighbors=15, min_dist=.1,
                              metric='euclidean', random_state=seed, n_jobs=1,
                              compatibility_layout=True).fit_transform(x)
                tu = float(trustworthiness(x[ix], u[ix], n_neighbors=K))
                embeddings[seed], trusts[seed] = neighbors(u[ix]), tu
                stability.append(dict(**base, tip='seed', seed=seed, seed_referinta=42,
                                      trust_UMAP=tu, diferenta_trust_fata_seed42=tu-trusts[42],
                                      suprapunere_vecini_cu_seed42=overlap(embeddings[42], embeddings[seed])))
                if seed == 42 and period == 'Integral':
                    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
                    scatter(axes[0], p[ix], frame.iloc[ix]['Statie'], f'{name}: PCA ({dim}D)', True)
                    scatter(axes[1], u[ix], frame.iloc[ix]['Statie'], f'{name}: UMAP ({dim}D), seed 42')
                    fig.suptitle(f'n ajustare={len(frame)}; n afisat/evaluat={len(ix)}; {len(cols)} variabile')
                    fig.tight_layout()
                    fig.savefig(OUT / f'{name}_PCA_UMAP.png', dpi=180)
                    plt.close(fig)
            pair_overlap = [overlap(embeddings[a], embeddings[b]) for a,b in itertools.combinations(SEEDS, 2)]
            row = dict(**base, **{f'trust_UMAP_seed{s}': trusts[s] for s in SEEDS},
                       trust_UMAP_medie=float(np.mean(list(trusts.values()))),
                       trust_UMAP_std=float(np.std(list(trusts.values()), ddof=1)),
                       suprapunere_vecini_seeduri_medie=float(np.mean(pair_overlap)))
            results.append(row)
            # Save progress after each completed experiment.
            pd.DataFrame(results).to_csv(OUT / 'comparatie_CP3.csv', index=False, encoding='utf-8-sig')
            pd.DataFrame(stability).to_csv(OUT / 'stabilitate_CP3.csv', index=False, encoding='utf-8-sig')
    for name in SETS:
        first, second = [next(r for r in results if r['set']==name and r['perioada']==period)
                         for period in ['Prima_subperioada', 'A_doua_subperioada']]
        stability.append(dict(set=name, perioada='Comparatie_subperioade', tip='temporal',
                              diferenta_trust_PCA=second['trust_PCA']-first['trust_PCA'],
                              diferenta_trust_UMAP_medie=second['trust_UMAP_medie']-first['trust_UMAP_medie'],
                              diferenta_var_explicata_PCA=second['var_explicata_PCA']-first['var_explicata_PCA'],
                              unghi_max_subspatii_PCA_grade=float(np.degrees(subspace_angles(
                                  bases[('Prima_subperioada', name)], bases[('A_doua_subperioada', name)])).max())))
    pd.DataFrame(stability).to_csv(OUT / 'stabilitate_CP3.csv', index=False, encoding='utf-8-sig')
    full = pd.DataFrame(results).query("perioada == 'Integral'")
    fig, ax = plt.subplots(figsize=(11, 2.8))
    ax.axis('off')
    table_rows = [[r['set'], f"{r['variabile']} → {r['dimensiuni']}", f"{100*r['var_explicata_PCA']:.2f}%",
                   f"{r['eroare_reconstructie_PCA']:.6f}", f"{r['trust_PCA']:.6f}",
                   f"{r['trust_UMAP_medie']:.6f} ± {r['trust_UMAP_std']:.6f}"] for r in full.to_dict('records')]
    table = ax.table(cellText=table_rows, colLabels=['Set', 'Dim.', 'Varianta PCA', 'MSE PCA', 'Trust PCA', 'Trust UMAP (medie ± SD)'], loc='center', cellLoc='center', colWidths=[.12,.08,.14,.13,.13,.30])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.8)
    ax.set_title('Comparatie PCA–UMAP pe aceleasi observatii; k=10; seeduri 42, 21, 123')
    fig.tight_layout()
    fig.savefig(OUT / 'tabel_slide2.png', dpi=200)
    plt.close(fig)
    write_slide()
    print(full.to_string(index=False), flush=True)
    print('Analiza finalizata: ' + str(OUT), flush=True)


if __name__ == '__main__':
    main()
