# Slide 2 — Dovada etapei

**Titlu:** UMAP păstrează mai bine vecinătățile în reducerea combinată 3→2

**Unicul element vizual:** `tabel_slide2.png` (include toate cele trei surse).

**Surse și perioadă:** RNMCA (PM2.5) și Open-Meteo (temperatură, vânt), București, 2025-10-13 – 2026-10-31.

**Date:** 6,067 observații complete din 6,148; patru stații B-12, B-14, B-21, B-26; unitate stație × zi × 6 ore. RNMCA: 1 variabilă, Open-Meteo: 2, combinate: 3.

**Protocol:** StandardScaler; PCA/UMAP ajustate pe toate observațiile eligibile; trustworthiness cu k=10 pe același eșantion reproductibil de 1.000 observații; dimensiuni 1→1, 2→2 și 3→2; MSE în spațiul standardizat. UMAP: n_neighbors=15, min_dist=0.1, metrică euclidiană; seed-uri 42, 21, 123. Stabilitate prin scoruri și vecini comuni între seed-uri și reajustare pe două subperioade separate la 2026-04-23.

**Interpretare:** Pe datele combinate, PCA păstrează 85.2588% din varianță (MSE=0.147412), iar trustworthiness este 0.958481 pentru PCA și 0.989307 ± 0.000275 pentru UMAP (medie ± SD între seed-uri), favorizând UMAP pentru vecinătățile locale în acest protocol.

**Limitare:** Numai setul combinat are reducere dimensională efectivă; PCA 1→1 și 2→2 păstrează toate dimensiunile. Rezultatele sunt exploratorii, fără validare predictivă. Media pe trei seed-uri nu este interval de încredere.

**Repository GitHub:** https://github.com/LitaAna/Proiect_MEDE
