# Analiza grafică PM2.5 în București

## Scop
Analiza variației concentrațiilor PM2.5 în funcție de **anotimp și intervalul zilei**, pentru stațiile B-12, B-14, B-21 și B-26, precum și pentru media celor patru stații.

## Date și metodologie
- **Sursa:** `CP2_matrice.xlsx`, foaia `Matrice_CP2`.
- **Intervale:** Noapte (00–06), Dimineață (06–12), După-amiază (12–18), Seară (18–24).
- **Anotimpuri:** iarnă, primăvară, vară, toamnă.
- Se folosesc numai intervalele complete, fără interpolare.
- Pentru media generală se utilizează intervalele cu date complete la toate cele patru stații.

## Grafice generate

Scriptul `cp2_grafice.py` produce **10 grafice**:

| Analiză | Reprezentări |
|---|---|
| B-12 | Grafic cu bare + heatmap |
| B-14 | Grafic cu bare + heatmap |
| B-21 | Grafic cu bare + heatmap |
| B-26 | Grafic cu bare + heatmap |
| Media celor 4 stații | Grafic cu bare + heatmap |

Fiecare grafic prezintă **cele 16 combinații anotimp × interval al zilei**, prin concentrația medie PM2.5 (µg/m³).

## Ce analizăm
- Intervalele zilei cu cele mai mari și cele mai mici concentrații în fiecare anotimp.
- Diferențele dintre anotimpuri pentru același interval al zilei.
- Diferențele și asemănările dintre cele patru stații.
- Tiparul general rezultat din media celor patru stații.

## Rulare

```bash
python -m pip install pandas openpyxl matplotlib numpy
python cp2_grafice.py
```

Graficele sunt salvate în folderul `cp2_grafice`.

**Notă:** Media generală reprezintă media celor patru stații analizate, nu a întregului București. Rezultatele se referă exclusiv la perioada disponibilă în matrice.

## GitHub
https://github.com/LitaAna/Proiect_MEDE
