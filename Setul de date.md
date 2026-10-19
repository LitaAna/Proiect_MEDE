---

# CP1 — Alinierea datelor RNMCA și Open-Meteo

## 1. Scopul alinierii

Scopul acestei etape este integrarea datelor despre calitatea aerului și a datelor meteorologice într-un singur set de date, pentru a analiza relația dintre concentrația PM2.5, temperatura aerului și viteza vântului.

**Întrebarea de cercetare:**

*Cum variază concentrația medie zilnică de PM2.5 la stația B-12 din București în funcție de temperatura medie și viteza medie a vântului?*

Unitatea de analiză este **stație × zi**, fiecare rând din tabelul final reprezentând o zi calendaristică pentru stația B-12.

## 2. Sursele de date utilizate

Pentru aliniere au fost utilizate două surse:

| Sursa | Date utilizate | Rezoluție inițială |
|---|---|---|
| RNMCA — CalitateAer | Concentrația PM2.5 la stația B-12 | Orară |
| Open-Meteo Historical Weather | Temperatura la 2 m și viteza vântului la 10 m | Orară |

**Perioada analizată:** 13 octombrie 2025 – 11 octombrie 2026.

Datele provin din surse diferite și au fost prelucrate pentru a avea aceeași rezoluție temporală: **o zi calendaristică**.

## 3. Metodologia de preprocesare și aliniere

Procesul de aliniere a inclus următoarele etape:

1. **Încărcarea fișierelor:** importarea raportului Excel RNMCA și a datelor meteorologice Open-Meteo.
2. **Selectarea variabilelor:** extragerea concentrației PM2.5, a temperaturii aerului și a vitezei vântului.
3. **Tratarea valorilor lipsă:** transformarea valorilor PM2.5 lipsă, reprezentate prin `-`, în valori nule (`NaN`).
4. **Standardizarea timpului:** conversia datelor Open-Meteo din UTC/GMT în fusul orar al Bucureștiului, ținând cont de schimbările de oră.
5. **Agregarea zilnică:** calcularea mediilor zilnice pentru cele trei variabile.
6. **Alinierea datelor:** unirea seturilor de date pe baza datei calendaristice.
7. **Verificarea acoperirii:** calcularea numărului de zile aliniate și a observațiilor lipsă sau incomplete.

Pentru RNMCA, convenția de reprezentare a orelor `01–24` a fost tratată în procesare, însă interpretarea exactă a intervalelor orare trebuie confirmată din documentația sursei.

## 4. Structura setului de date final

Fișierul rezultat este `B12_date_aliniate.csv`.

| Variabilă | Descriere | Unitate |
|---|---|---|
| `date` | Data calendaristică | YYYY-MM-DD |
| `station_id` | Identificatorul stației | B-12 |
| `pm25_mean` | Concentrația medie zilnică PM2.5 | µg/m³ |
| `temperature_mean` | Temperatura medie zilnică | °C |
| `wind_speed_mean` | Viteza medie zilnică a vântului | km/h |
| `pm25_valid_hours` | Numărul de valori orare PM2.5 valide într-o zi | Număr |

Setul de date final permite compararea evoluției zilnice a concentrației PM2.5 cu variațiile temperaturii și vitezei vântului.

## 5. Raportul de acoperire a datelor

După preprocesare și aliniere, au fost obținute următoarele rezultate:

| Indicator | Rezultat |
|---|---:|
| Zile aliniate | 364 |
| Zile cu toate variabilele disponibile | 364 |
| Zile cu 24 de valori PM2.5 valide | 340 |
| Zile cu observații PM2.5 incomplete | 24 |
| Valori orare PM2.5 lipsă | 65 |

**Interpretare:**

Toate cele 364 de zile aliniate au valori disponibile pentru PM2.5, temperatură și viteza vântului.

Totuși, pentru 24 de zile, media zilnică PM2.5 a fost calculată din mai puțin de 24 de măsurători orare valide. Aceste zile au fost păstrate în tabelul general, iar numărul observațiilor valide este documentat pentru a permite evaluarea calității mediilor zilnice.

Fișierul `coverage_report.csv` conține raportul de acoperire.

## 7. Limitări

- Datele despre poluare provin de la o singură stație de monitorizare, B-12.
- Datele meteorologice Open-Meteo sunt asociate unei locații geografice și nu reprezintă măsurători efectuate direct la stația RNMCA.
- Există 65 de valori orare PM2.5 lipsă.
- Unele medii zilnice PM2.5 sunt calculate din mai puțin de 24 de observații valide.
- Convenția temporală RNMCA trebuie confirmată pentru validarea completă a alinierii.
- Alinierea temporală permite explorarea relațiilor dintre variabile, dar nu demonstrează o relație cauzală.
