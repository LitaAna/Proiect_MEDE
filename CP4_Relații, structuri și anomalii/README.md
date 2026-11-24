# CP4 — Grupări și anomalii în datele PM2.5 din București

## Scop

Identificarea grupărilor și observațiilor neobișnuite în reprezentările PCA și UMAP, cu evaluare prin silhouette și stabilitate bootstrap. Comparația include RNMCA separat, Open-Meteo separat și datele combinate.

Sunt folosite 6.067 observații complete din matricea CP2, pentru stațiile B-12, B-14, B-21 și B-26, în perioada 13.10.2025–31.10.2026. Unitate: stație × zi × interval de 6 ore. Variabile: PM2.5 (µg/m³), temperatură (°C), vânt (km/h).

## Rulare

Python 3.12, din folderul proiectului:

```powershell
python -m pip install -r requirements.txt
python -X utf8 CP4_analiza.py
```

Codul este independent: are nevoie doar de matrice și bibliotecile din `requirements.txt`. Generează **5 CSV și 3 PNG** în `CP4_rezultate`, fără exportul etapelor intermediare. La rerulare, fișierele cu aceleași nume sunt înlocuite.

## Protocol

- StandardScaler, PCA și UMAP, cu configurația CP3. Dimensiuni 1→1, 2→2, 3→2; numai setul combinat are reducere efectivă. UMAP: n_neighbors=15, min_dist=0.1, metrică euclidiană, compatibility_layout=True.
- K-means: seed 42, n_init=10; k ales dintre 2–6 prin silhouette, cu grupuri de minimum 1% din observații. Silhouette pe aceiași 1.000 de indici (RNG 42), atât în reprezentare, cât și în spațiul original comun cu trei variabile standardizate. Scorurile din spații diferite nu sunt direct comparabile.
- Stabilitate: 100 repetări bootstrap pe blocuri de 7 zile calendaristice, toate stațiile și intervalele unei zile împreună. Se reajustează K-means și se calculează ARI pe zilele neextrase (out-of-bag). **Reprezentarea, scalarea și k rămân fixe:** stabilitate condiționată a clusteringului, nu a întregii analize.
- Separat: UMAP reajustat cu seed-urile 42, 21 și 123; ARI compară grupările la k fixat pentru fiecare sursă.
- Isolation Forest: 300 arbori, seed 42; scor peste percentila 99. Pragul este prestabilit, deci numărul semnalat nu este o prevalență descoperită automat. Jaccard verifică acordul cu detecția în variabilele originale ale sursei.
- Comparația structurală: suplimentar, k=3 pentru toate sursele; tabelul arată cum se repartizează grupurile separate între grupurile combinate, cu mediile măsurătorilor originale. Graficul comparativ folosește aceleași axe fizice. Numerele grupurilor sunt ordonate descriptiv după medii; nu au identitate comună între analize.

## Rezultate finale

| Fișier | Conținut |
|---|---|
| `comparatie_CP4.csv` | Numărul grupurilor, silhouette, stabilitate bootstrap, anomalii și rezumatul stabilității între seed-uri |
| `profil_grupuri_CP4.csv` | Număr de observații și caracteristicile fiecărui grup |
| `anomalii_CP4.csv` | Observațiile semnalate, cu stația, data, intervalul și măsurătorile |
| `stabilitate_seeduri_CP4.csv` | Comparația grupărilor UMAP între seed-uri |
| `comparatie_surse_CP4.csv` | Comparația structurală la același k=3, separat versus combinat |
| `tabel_comparatie_CP4.png` | Sinteza metricilor pentru prezentare |
| `clustering_anomalii_comparativ.png` | Grupările și anomaliile în PCA și UMAP |
| `structura_surse_comparativ.png` | Grupările la k=3 afișate în temperatură și PM2.5 |

## Interpretare și limite

Pe datele combinate sunt selectate trei grupuri. Gruparea UMAP are ARI față de seed 42 de aproximativ 0,993 și 0,997 pentru celelalte două seed-uri, mult peste acordul observat pentru sursele separate în acest protocol. Grupurile descriu contexte PM2.5–meteo, dar această stabilitate nu demonstrează existența unor regimuri naturale exclusive datelor combinate. Comparația structurală trebuie citită împreună cu profilele grupurilor.

K-means impune partiții compacte chiar pe distribuții continue. UMAP poate modifica geometria și densitățile; unele inițializări spectrale Open-Meteo folosesc fallback aleatoriu, semnalat în consolă. Observațiile atipice nu sunt automat erori sau depășiri legale. Selectarea k este exploratorie; nu există validare externă sau concluzii cauzale.


