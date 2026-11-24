
# Rezultate CP4 — Grupări și anomalii

Analiză pe 6.067 observații complete din RNMCA și Open-Meteo, pentru perioada 13.10.2025–31.10.2026. Fiecare observație reprezintă o stație × o zi × un interval de 6 ore.

## Fișiere CSV

- **comparatie_CP4.csv** — sinteza analizelor PCA și UMAP pentru fiecare sursă și datele combinate: numărul grupurilor, silhouette, stabilitatea bootstrap, stabilitatea între seed-uri și numărul observațiilor semnalate ca neobișnuite.
- **profil_grupuri_CP4.csv** — caracteristicile fiecărui grup: numărul observațiilor și statisticile PM2.5, temperaturii și vântului, în unitățile originale.
- **anomalii_CP4.csv** — observațiile semnalate de Isolation Forest, cu stația, data, intervalul zilei, măsurătorile și scorul de anomalie. 
- **stabilitate_seeduri_CP4.csv** — comparația grupărilor UMAP pentru seed-urile 42, 21 și 123. ARI măsoară acordul dintre grupări; valori apropiate de 1 indică acord ridicat.
- **comparatie_surse_CP4.csv** — comparația la același număr de grupuri, k=3: arată cum se repartizează grupurile unei surse separate între grupurile datelor combinate și care sunt mediile măsurătorilor pentru fiecare intersecție.

## Imagini

- **tabel_comparatie_CP4.png** — tabelul de sinteză cu grupurile, silhouette, stabilitatea și numărul observațiilor neobișnuite.
- **clustering_anomalii_comparativ.png** — grupările în PCA și UMAP, separat pe surse și pe datele combinate. Culorile indică grupurile, iar marcajele negre indică observațiile semnalate ca anomalii.
- **structura_surse_comparativ.png** — comparația grupărilor PCA la k=3, afișate pe aceleași axe: temperatură și PM2.5. Permite examinarea diferențelor dintre sursele separate și datele combinate.

