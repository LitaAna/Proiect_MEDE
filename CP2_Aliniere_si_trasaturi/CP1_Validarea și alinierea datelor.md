# Validarea și alinierea datelor RNMCA și Open-Meteo

## 1. Scopul etapei

Acest folder conține seturile de date și codul Python utilizate pentru validarea și alinierea concentrațiilor de PM2.5 din București cu datele meteorologice privind temperatura aerului și viteza vântului.

În urma feedbackului primit la CP0, proiectul a fost extins de la o singură stație (B-12) la patru stații RNMCA: **B-12, B-14, B-21 și B-26**.

**Întrebarea de cercetare:**

Ce tipare de poluare cu PM2.5 pot fi identificate la stațiile B-12, B-14, B-26 și B-21 din București și cum diferă concentrațiile între cele patru anotimpuri și cele patru intervale ale zilei?

Scopul acestei etape este obținerea unui set de date orare validate și aliniate, care să permită analiza ulterioară a variațiilor PM2.5 în funcție de stație, anotimp și momentul zilei.

**Unitatea de observație pentru CP1:** stație × oră.

**Unitatea de analiză planificată pentru CP2:** stație × zi × interval al zilei.

## 2. Fișierele din folder

| Fișier | Descriere |
| --- | --- |
| `date_validate_RNMCA_OpenMeteo.xlsx` | Datele RNMCA și Open-Meteo validate, organizate în două foi Excel separate |
| `date_aliniate_RNMCA_meteo.xlsx` | Setul de date orare aliniate, cu PM2.5, temperatură și viteza vântului într-un singur tabel |
| `pipeline_cp1_U12.py` | Scriptul Python pentru încărcarea, validarea și alinierea datelor |
| `raport_validare_CP1.json` | Raport privind acoperirea temporală și valorile lipsă |

Documentarea surselor este realizată separat prin Data Card-urile RNMCA și Open-Meteo.

## 3. Sursele datelor

### RNMCA — Rețeaua Națională de Monitorizare a Calității Aerului

Datele provin din portalul oficial CalitateAer și reprezintă concentrațiile orare de PM2.5 măsurate la patru stații din București:

- B-12
- B-14
- B-21
- B-26

**Variabilă principală:** PM2.5, exprimată în µg/m³.

**Rezoluție temporală:** orară.

**Rezoluție spațială:** patru stații fixe de monitorizare.

### Open-Meteo — Date meteorologice istorice

Datele meteorologice sunt utilizate pentru caracterizarea condițiilor atmosferice asociate concentrațiilor PM2.5.

Variabile utilizate:

- Temperatura aerului la 2 m (°C).
- Viteza vântului la 10 m (km/h).

**Rezoluție temporală:** orară.

**Rezoluție spațială:** un punct meteorologic modelat, utilizat pentru toate cele patru stații.

**Perioada nominală a datelor:** 13.10.2025–01.11.2026. Acoperirea efectivă diferă între surse, iar ultima zi RNMCA este incompletă.

## 4. Validarea datelor

Validarea a fost realizată separat pentru fiecare sursă, înainte de alinierea observațiilor.

### 4.1. Validarea datelor RNMCA

Operațiile de validare au inclus:

1. Citirea datelor din raportul Excel RNMCA.
2. Extragerea valorilor PM2.5 pentru cele patru stații.
3. Uniformizarea formatelor de dată și oră.
4. Conversia concentrațiilor PM2.5 în valori numerice.
5. Identificarea și marcarea valorilor lipsă.
6. Verificarea acoperirii temporale.

**Rezultatele verificării:**

| Stație | Înregistrări orare | Valori PM2.5 lipsă |
| --- | ---: | ---: |
| B-12 | 9.217 | 66 |
| B-14 | 9.217 | 27 |
| B-21 | 9.217 | 1 |
| B-26 | 9.217 | 31 |
| **Total** | **36.868** | **125** |

### 4.2. Validarea datelor Open-Meteo

Pentru datele meteorologice au fost verificate:

1. Formatul datei și orei.
2. Conversia temperaturii și vitezei vântului în valori numerice.
3. Identificarea valorilor lipsă.
4. Conversia timpului din UTC în fusul orar `Europe/Bucharest`.
5. Identificarea orelor locale repetate la schimbarea orei.

### 4.3. Tratarea valorilor lipsă

Valorile lipsă au fost păstrate ca valori nule (`NaN`).

Nu au fost aplicate interpolări și nu au fost înlocuite valorile lipsă cu zero sau cu medii calculate.

Datele validate au fost exportate în fișierul:

`date_validate_RNMCA_OpenMeteo.xlsx`

Acesta conține două foi:

- `RNMCA_validate` — concentrațiile PM2.5 validate.
- `OpenMeteo_validate` — temperatura și viteza vântului validate.

## 5. Alinierea datelor

După validare, datele din cele două surse au fost organizate într-un set comun, folosind informațiile calendaristice și orare.

### 5.1. Armonizarea temporală

- Datele RNMCA sunt raportate prin dată și etichete orare `01–24`.
- Datele Open-Meteo sunt furnizate în UTC.
- Orele Open-Meteo au fost convertite în fusul orar `Europe/Bucharest`.
- Observațiile au fost asociate în funcție de data și ora locală.
- Situațiile de asociere temporală ambiguă au fost marcate.

**Important:** interpretarea exactă a etichetelor RNMCA `01–24` trebuie confirmată. Din acest motiv, alinierea este considerată provizorie.

### 5.2. Setul de date aliniate

Rezultatul alinierii este fișierul:

`date_aliniate_RNMCA_meteo.xlsx`

Acesta conține într-un singur tabel:

| Informație | Descriere |
| --- | --- |
| Stație | B-12, B-14, B-21 sau B-26 |
| Data | Data calendaristică a observației |
| Ora | Ora locală utilizată la aliniere |
| PM2.5 | Concentrația particulelor fine (µg/m³) |
| Temperatură | Temperatura aerului la 2 m (°C) |
| Viteza vântului | Viteza vântului la 10 m (km/h) |
| Indicatori de validare | Disponibilitatea și statusul asocierii observațiilor |

Fiecare rând reprezintă o combinație **stație × oră**.

Setul de date conține **36.868 de înregistrări stație–oră**, inclusiv observațiile cu valori lipsă sau cu aliniere neconfirmată.

## 6. Pregătirea pentru analiza pe intervale ale zilei

Pentru a analiza variațiile concentrațiilor PM2.5 în funcție de momentul zilei, ziua va fi împărțită în patru intervale de câte șase ore.

| Interval al zilei | Ore |
| --- | --- |
| Noapte | 00:00–05:59 |
| Dimineață | 06:00–11:59 |
| Prânz / după-amiază | 12:00–17:59 |
| Seară | 18:00–23:59 |

## 7. Rezultatele CP1

În urma procesării au fost obținute două seturi principale:

**1. Date validate — `date_validate_RNMCA_OpenMeteo.xlsx`**

Conține datele RNMCA și Open-Meteo verificate, organizate separat pe surse. Acest fișier documentează rezultatul validării.

**2. Date aliniate — `date_aliniate_RNMCA_meteo.xlsx`**

Conține concentrațiile PM2.5 și variabilele meteorologice asociate temporal într-un singur tabel. Acesta constituie baza pentru construirea matricei de trăsături din CP2.

## 8. Limitări

- Convenția orelor RNMCA `01–24` necesită confirmare.
- Ultima zi RNMCA, 01.11.2026, este incompletă.
- Datele meteorologice pentru 01.11.2026 necesită verificarea omogenității spațiale.
- Datele Open-Meteo reprezintă un singur punct meteorologic modelat, nu măsurători individuale pentru fiecare stație.
- Valorile lipsă nu au fost interpolate.
- Asocierea temporală este provizorie până la finalizarea verificărilor.

## 9. Reproducibilitate

Prelucrarea datelor este documentată prin scriptul Python `pipeline_U12.py` și prin raportul `raport_validare.json`.

Pentru reproducerea rezultatelor sunt necesare fișierele sursă RNMCA și Open-Meteo descrise în Data Card-uri.

Scriptul și raportul de validare trebuie păstrate în repository împreună cu seturile de date rezultate.

## 10. Sursele datelor

- **RNMCA — CalitateAer:** https://www.calitateaer.ro/
- **Open-Meteo — Historical Weather:** https://open-meteo.com/en/docs/historical-weather-api


