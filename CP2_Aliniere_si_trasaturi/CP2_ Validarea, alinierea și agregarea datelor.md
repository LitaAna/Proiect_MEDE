# Validarea, alinierea și agregarea datelor RNMCA și Open-Meteo

## 1. Scopul proiectului

Proiectul analizează variația concentrațiilor de PM2.5 în București, utilizând date de la patru stații ale Rețelei Naționale de Monitorizare a Calității Aerului (RNMCA): **B-12, B-14, B-21 și B-26**, împreună cu date meteorologice Open-Meteo.

În urma feedbackului primit la CP0, analiza a fost extinsă de la o singură stație (B-12) la patru stații.

**Întrebarea de cercetare:**

*Ce tipare de poluare cu PM2.5 pot fi identificate la stațiile B-12, B-14, B-21 și B-26 din București și cum diferă concentrațiile între cele patru anotimpuri și cele patru intervale ale zilei?*

Procesarea datelor este organizată în două etape:

- **CP1:** validarea surselor și alinierea observațiilor la nivel orar.
- **CP2:** agregarea observațiilor pe intervale de șase ore, construirea matricei finale și calcularea statisticilor descriptive și a corelațiilor.

## 2. Sursele datelor

### RNMCA — CalitateAer

Datele RNMCA conțin concentrațiile orare de PM2.5 măsurate la patru stații fixe din București:

- B-12
- B-14
- B-21
- B-26

**Variabilă:** concentrația PM2.5 (µg/m³).

**Rezoluție temporală:** orară.

**Rezoluție spațială:** patru stații de monitorizare.

### Open-Meteo — Historical Weather

Datele meteorologice sunt utilizate pentru analiza asocierilor dintre poluare și condițiile atmosferice.

**Variabile:**

- Temperatura aerului la 2 m (°C).
- Viteza vântului la 10 m (km/h).

**Rezoluție temporală:** orară.

**Rezoluție spațială:** un punct meteorologic modelat, utilizat pentru toate cele patru stații.

**Perioada nominală:** 13.10.2025–01.11.2026. Ultima zi RNMCA este incompletă.

Documentarea detaliată a surselor se regăsește în Data Card-urile RNMCA și Open-Meteo.

## 3. Fișierele proiectului

| Fișier | Conținut |
| --- | --- |
| `date_validate_RNMCA_OpenMeteo.xlsx` | Datele RNMCA și Open-Meteo validate, în două foi separate |
| `date_aliniate_RNMCA_meteo.xlsx` | Datele validate, asociate la nivel orar |
| `pipeline_U12.py` | Scriptul pentru validarea și alinierea datelor din CP1 |
| `raport_validare_CP1.json` | Raportul de validare și acoperire a datelor |
| `CP2_matrice.xlsx` | Matricea finală agregată pe intervale de șase ore, statisticile descriptive și corelațiile |

## 4. CP1 — Validarea datelor

Validarea a fost realizată separat pentru fiecare sursă, înainte de alinierea observațiilor.

### 4.1. Validarea RNMCA

Au fost realizate următoarele operații:

1. Citirea raportului Excel RNMCA.
2. Extragerea valorilor PM2.5 pentru cele patru stații.
3. Uniformizarea formatelor de dată și oră.
4. Conversia concentrațiilor în valori numerice.
5. Identificarea valorilor lipsă și a valorilor negative invalide.
6. Verificarea acoperirii temporale.

**Rezultatele validării:**

| Stație | Înregistrări orare | Valori PM2.5 lipsă |
| --- | ---: | ---: |
| B-12 | 9.217 | 66 |
| B-14 | 9.217 | 27 |
| B-21 | 9.217 | 1 |
| B-26 | 9.217 | 31 |
| **Total** | **36.868** | **125** |

### 4.2. Validarea Open-Meteo

Au fost verificate:

1. Formatul datei și orei.
2. Conversia temperaturii și vitezei vântului în valori numerice.
3. Identificarea valorilor lipsă.
4. Conversia timpului din UTC în fusul orar `Europe/Bucharest`.
5. Identificarea orelor locale repetate la schimbarea orei de vară/iarnă.

### 4.3. Tratarea valorilor lipsă

Valorile lipsă au fost păstrate ca valori nule (`NaN`).

Nu au fost aplicate interpolări și nu au fost înlocuite valorile lipsă cu zero sau cu alte valori estimate.

Rezultatul validării este fișierul `date_validate_RNMCA_OpenMeteo.xlsx`, care conține două foi:

- `RNMCA_validate`
- `OpenMeteo_validate`

## 5. CP1 — Alinierea temporală a surselor

Pentru integrarea datelor RNMCA și Open-Meteo, observațiile au fost asociate după data și ora locală.

### 5.1. Uniformizarea timpului

- RNMCA furnizează observații cu etichete orare `01–24`.
- Pentru analiza de față, aceste etichete au fost interpretate ca intervale orare consecutive, de la `00:00–00:59` până la `23:00–23:59`.
- Open-Meteo furnizează marcaje temporale UTC, convertite în `Europe/Bucharest`.
- Asocierea a fost realizată folosind data calendaristică și ora locală.
- Orele repetate la trecerea la ora de iarnă au fost marcate ca ambigue și nu au fost asociate automat.

Interpretarea etichetelor RNMCA reprezintă o convenție de prelucrare adoptată pentru acest proiect, pe baza structurii exportului, nu o regulă oficială verificată independent.

### 5.2. Setul de date aliniate

Rezultatul este fișierul `date_aliniate_RNMCA_meteo.xlsx`.

Acesta conține concentrația PM2.5, temperatura și viteza vântului, împreună cu informații privind stația, data, ora și statusul alinierii.

**Unitatea de observație CP1:** stație × oră.

Setul conține **36.868 de înregistrări stație–oră**, inclusiv observațiile cu valori lipsă sau asocieri temporale ambigue.

## 6. CP2 — Grid comun și agregare temporală

Pentru a compara variațiile PM2.5 între momentele zilei, datele orare aliniate în CP1 au fost agregate într-o matrice comună.

### 6.1. Definirea gridului

**Unitatea finală de analiză:** stație × zi × interval al zilei.

Fiecare zi a fost împărțită în patru intervale de câte șase ore:

| Interval | Ore |
| --- | --- |
| Noapte | 00:00–05:59 |
| Dimineață | 06:00–11:59 |
| Prânz / după-amiază | 12:00–17:59 |
| Seară | 18:00–23:59 |

Fiecare combinație stație–zi–interval reprezintă un rând în matricea CP2.

### 6.2. Agregarea datelor

Pentru fiecare interval de șase ore au fost calculate separat:

- Media concentrației PM2.5 (µg/m³), din datele RNMCA.
- Temperatura medie (°C), din datele Open-Meteo.
- Viteza medie a vântului (km/h), din datele Open-Meteo.

Mediile au fost calculate folosind valorile orare disponibile.

Au fost păstrate și numerele de observații care au contribuit la fiecare medie, pentru verificarea completitudinii intervalelor.

### 6.3. Interpolare și tratarea golurilor

**Nu a fost aplicată interpolare.**

Valorile lipsă nu au fost înlocuite cu zero sau cu valori estimate.

Intervalele incomplete au fost păstrate în matrice și marcate prin indicatori de completitudine. Pentru statisticile și corelațiile finale au fost selectate numai intervalele complete, pentru a evita comparațiile între medii calculate dintr-un număr diferit de observații.

Această abordare permite păstrarea trasabilității datelor și documentarea explicită a golurilor.

## 7. CP2 — Matricea finală unitate × trăsături

Matricea finală este disponibilă în fișierul:

**`CP2_matrice.xlsx`**

Fiecare rând reprezintă o combinație **stație × zi × interval de șase ore**.

Trăsăturile sunt grupate în funcție de sursa datelor:

| Grup | Trăsături |
| --- | --- |
| Identificarea unității | Stație, dată, interval al zilei |
| RNMCA | PM2.5 mediu (µg/m³), numărul observațiilor PM2.5 |
| Open-Meteo | Temperatură medie (°C), vânt mediu (km/h), numărul observațiilor meteorologice |
| Controlul calității | Indicatori de completitudine a intervalului |

Matricea conține **6.148 de rânduri**, dintre care:

- **6.067 de intervale complete**, utilizate pentru statisticile și corelațiile finale.
- **81 de intervale incomplete**, păstrate pentru transparență, dar excluse din analizele statistice finale.

## 8. CP2 — Statistici descriptive și corelații între surse

Pentru caracterizarea variabilelor au fost calculate statistici descriptive, precum media, mediana, minimul, maximul și dispersia valorilor.

Au fost analizate distribuțiile următoarelor variabile:

- PM2.5 mediu pe interval de șase ore.
- Temperatura medie pe interval de șase ore.
- Viteza medie a vântului pe interval de șase ore.

Pentru examinarea relațiilor dintre surse a fost utilizat coeficientul de corelație Pearson.

**Rezultatele calculate:**

| Relație | Coeficient Pearson |
| --- | ---: |
| PM2.5 – Temperatură | −0,423 |
| PM2.5 – Viteza vântului | −0,267 |

Ambele corelații sunt negative. În datele analizate, concentrațiile PM2.5 mai ridicate tind să fie asociate cu temperaturi și viteze ale vântului mai reduse.

Corelațiile descriu asocieri statistice și nu demonstrează relații de cauzalitate. Rezultatele pot fi influențate de sezonalitate și de diferențele dintre stații.

Fișierul Excel conține trei foi:

- `Matrice_CP2` — matricea finală agregată.
- `Statistici` — indicatorii statistici descriptivi.
- `Corelatii` — corelațiile dintre PM2.5 și variabilele meteorologice.

## 9. Limitări

- Interpretarea etichetelor RNMCA `01–24` este o convenție de prelucrare adoptată pentru proiect, care nu a fost confirmată independent printr-o specificație oficială.
- Ultima zi RNMCA, 01.11.2026, este incompletă.
- Omogenitatea spațială a datelor Open-Meteo pentru 01.11.2026 necesită verificare.
- Open-Meteo reprezintă un punct meteorologic modelat, utilizat pentru toate cele patru stații, nu observații meteorologice individuale pentru fiecare stație.
- Nu au fost interpolate valorile lipsă.
- Corelațiile nu implică relații cauzale.

## 10. Reproducibilitate

Procesarea datelor pentru CP1 este documentată prin scriptul Python `pipeline_U12.py`.

Fluxul de lucru este:

**Date originale RNMCA și Open-Meteo → validare → aliniere orară → agregare pe intervale de șase ore → matrice finală CP2 → statistici descriptive și corelații.**

Fișierele validate și aliniate permit verificarea etapelor de prelucrare. Matricea CP2 și rezultatele statistice sunt păstrate în repository pentru consultare și verificare.

## 11. Surse și repository

- **RNMCA — CalitateAer:** https://www.calitateaer.ro/
- **Open-Meteo — Historical Weather:** https://open-meteo.com/en/docs/historical-weather-api
- **Repository GitHub:** https://github.com/LitaAna/Proiect_MEDE
