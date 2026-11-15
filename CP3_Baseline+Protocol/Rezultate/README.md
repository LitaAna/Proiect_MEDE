# Rezultate CP3 — PCA și UMAP

Analiză pe 6.067 observații complete, în perioada 13.10.2025–31.10.2026. Surse: RNMCA (PM2.5) și Open-Meteo (temperatură și vânt).

- `comparatie_CP3.csv`: comparația PCA–UMAP pentru fiecare sursă și datele combinate.
- `stabilitate_CP3.csv`: rezultatele pentru seed-urile 42, 21, 123 și cele două subperioade.
- `*_PCA_UMAP.png`: grafice comparative.
- `tabel_slide2.png`: tabelul comparativ
- `audit_date.json`: evidența verificării datelor și versiunile bibliotecilor.
- `observatii_folosite.csv`: identificatorii observațiilor incluse.

Fișiere generate prin rularea `CP3_analiza.py`. Reducerea dimensională efectivă are loc numai pentru datele combinate (3→2).
