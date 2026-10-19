# CP1 — Alinierea datelor RNMCA și Open-Meteo

## Scop

Acest folder conține datele și codul Python utilizate pentru alinierea concentrațiilor de PM2.5 de la stația B-12 din București cu datele meteorologice privind temperatura și viteza vântului.

**Întrebarea de cercetare:** Cum variază concentrația medie zilnică de PM2.5 la stația B-12 din București în funcție de temperatura medie și viteza medie a vântului?

Unitatea de analiză este **stația B-12 × zi calendaristică**.

## Fișierele din folder

| Fișier | Descriere |
|---|---|
| `RNMCA_B12_concentratii.xlsx` | Datele orare PM2.5 provenite din RNMCA |
| `Meteo.csv(1).xlsx` | Datele meteorologice orare provenite din Open-Meteo |
| `align_b12.py` | Scriptul Python pentru prelucrarea și alinierea datelor |
| `B12_date_aliniate.csv` | Setul de date zilnice aliniate |
| `B12_date_valide.csv` | Setul de date cu observații valide |
| `coverage_report.json` | Raportul privind acoperirea și valorile lipsă |

## Metodologia de prelucrare

1. Importarea datelor orare PM2.5 și meteorologice.
2. Armonizarea formatelor de dată și oră.
3. Alinierea observațiilor pe zile calendaristice.
4. Calcularea mediilor zilnice pentru PM2.5, temperatură și viteza vântului.
5. Verificarea valorilor lipsă și a acoperirii datelor.
6. Exportarea seturilor de date și a raportului de acoperire.

## Reproducerea rezultatelor

Pentru rularea scriptului este necesar Python 3 și biblioteca `openpyxl`.

Instalarea bibliotecii:

```bash
python -m pip install openpyxl
```

Rularea scriptului din folderul care conține fișierele:

```bash
python align_b12.py --rnmca RNMCA_B12_concentratii.xlsx --meteo "Meteo.csv(1).xlsx" --out rezultate
```

Scriptul generează în folderul `rezultate` seturile de date aliniate și raportul de acoperire.

## Rezultatele CP1

În urma procesării au fost obținute:

- 364 de observații zilnice aliniate;
- 340 de zile cu 24 de măsurători orare PM2.5 valide;
- 24 de zile cu acoperire incompletă pentru PM2.5.

Valorile trebuie interpretate în raport cu regulile de validare și agregare implementate în script.

## Sursele datelor

- **RNMCA — Rețeaua Națională de Monitorizare a Calității Aerului:** https://www.calitateaer.ro/
- **Open-Meteo — Historical Weather:** https://open-meteo.com/

## Etapa următoare

În CP2 vor fi analizate distribuțiile variabilelor, valorile lipsă și relațiile preliminare dintre PM2.5, temperatură și viteza vântului.
