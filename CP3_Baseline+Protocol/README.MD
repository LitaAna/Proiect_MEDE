# CP3 — Analiza tiparelor de poluare cu PM2.5 în București

Proiect MEDE, Checkpoint 3 — Liță Ana-Maria-Larisa, U12.

## Scopul analizei

Am comparat PCA, ca metodă de referință (baseline), cu UMAP, pentru a evalua modul în care păstrează structura datelor despre poluare și condițiile meteorologice.

Analiza pornește de la matricea realizată la CP2, fără refacerea colectării și alinierii datelor.

## Date utilizate

- Stații: B-12, B-14, B-21 și B-26, București.
- RNMCA: concentrația PM2.5 (µg/m³).
- Open-Meteo: temperatura (°C) și viteza vântului (km/h).
- Perioada observațiilor folosite: 13.10.2025–31.10.2026.
- Unitatea de analiză: stație × zi × interval de 6 ore.
- Au fost păstrate 6.067 de observații complete din 6.148 de rânduri inițiale, fără imputarea valorilor lipsă.

## Metode și evaluare

Variabilele au fost standardizate înainte de aplicarea PCA și UMAP. Metodele au fost aplicate pe aceleași observații, în trei variante:

| Set | Variabile | Dimensiuni păstrate |
|---|---|---|
| RNMCA | PM2.5 | 1→1 |
| Open-Meteo | Temperatură și vânt | 2→2 |
| Combinate | PM2.5, temperatură și vânt | 3→2 |

Numai setul combinat are reducere dimensională efectivă. Pentru RNMCA și Open-Meteo, PCA păstrează toate dimensiunile disponibile.

Am evaluat varianța explicată și eroarea de reconstrucție pentru PCA, respectiv trustworthiness pentru ambele metode. Trustworthiness a fost calculat cu 10 vecini, pe același eșantion reproductibil de 1.000 de observații. Modelele au fost ajustate pe toate observațiile eligibile.

Stabilitatea UMAP a fost verificată cu seed-urile 42, 21 și 123, prin compararea scorurilor și a vecinilor păstrați. Analiza a fost repetată și pe două subperioade:

- 13.10.2025–22.04.2026;
- 23.04.2026–31.10.2026.

## Rezultatul principal

Pe datele combinate, PCA păstrează 85,26% din varianță, cu o eroare de reconstrucție de 0,147412 în spațiul standardizat.

Trustworthiness este 0,958481 pentru PCA și 0,989307 ± 0,000275 pentru UMAP, unde ± reprezintă deviația standard între cele trei seed-uri.

UMAP păstrează mai bine vecinătățile locale pe setul combinat, iar avantajul se menține în ambele subperioade. Această concluzie se referă la protocolul analizat, nu la o superioritate generală a UMAP.

## Fișiere și rulare

- `CP2_matrice.xlsx`: matricea de intrare.
- `CP3_analiza.py`: codul principal.
- `requirements.txt`: bibliotecile necesare.
- `CP3_rezultate/`: tabelele, graficele și evidența datelor folosite.

Rulare cu Python 3.12, din folderul proiectului:

    python -m pip install -r requirements.txt
    python -X utf8 CP3_analiza.py

Rezultatele sunt salvate automat în `CP3_rezultate`.

## Limitări

Analiza este exploratorie, fără evaluare predictivă pe un set de test. Trustworthiness măsoară păstrarea vecinătăților, nu acuratețea predicției poluării. Pentru unele ajustări Open-Meteo, UMAP a trecut automat de la inițializare spectrală la inițializare aleatoare.


