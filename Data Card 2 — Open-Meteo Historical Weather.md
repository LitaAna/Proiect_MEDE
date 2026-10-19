# Data Card 2 — Open-Meteo Historical Weather

## 1. Proveniența datelor

- **Sursă:** Open-Meteo Historical Weather API
- **Website oficial:** https://open-meteo.com/
- **Documentație:** https://open-meteo.com/en/docs/historical-weather-api
- **Fișier descărcat:** `Meteo.csv`
- **Format:** CSV
- **Metoda de obținere:** export din serviciul Open-Meteo Historical Weather
- **Tipul datelor:** date meteorologice istorice

## 2. Perioada și rezoluția datelor

| Caracteristică | Valoare |
|---|---|
| Perioada | 13.10.2025 – 11.10.2026 |
| Rezoluție temporală originală | Orară |
| Rezoluție temporală pentru proiect | Zilnică |
| Rezoluție spațială | Punct geografic / celulă a modelului meteorologic |
| Latitudine | Aproximativ 44,46° N |
| Longitudine | Aproximativ 26,09° E |
| Altitudine indicată în fișier | 93 m |
| Număr de înregistrări orare | 8.736 |
| Unitate de analiză | Locație × zi |

Datele meteorologice vor fi agregate la nivel zilnic pentru a putea fi comparate cu concentrațiile PM2.5.

## 3. Variabile și unități

| Variabilă | Descriere | Unitate |
|---|---|---|
| `time` | Data și ora observației | YYYY-MM-DD HH:MM |
| `temperature_2m` | Temperatura aerului la 2 m | °C |
| `wind_speed_10m` | Viteza vântului la 10 m | km/h |

Variabilele utilizate în proiect sunt temperatura medie zilnică și viteza medie zilnică a vântului.

## 4. Calitatea datelor și goluri

Verificarea preliminară a fișierului a evidențiat:

| Indicator | Valoare |
|---|---:|
| Înregistrări orare | 8.736 |
| Valori lipsă pentru temperatură | 0 |
| Valori lipsă pentru viteza vântului | 0 |
| Rezoluție temporală | Orară |

Pentru analiza zilnică, valorile orare vor fi agregate prin calcularea mediilor.

## 5. Licență și condiții de utilizare

Open-Meteo publică informații despre licențe și condiții de utilizare pe website-ul oficial.

- **Website:** https://open-meteo.com/
- **Termeni și licențe:** https://open-meteo.com/en/terms
- **Atribuire:** Open-Meteo

Licența exactă aplicabilă datelor istorice și condițiile de redistribuire vor fi verificate în raport cu termenii serviciului utilizat.

## 6. Limitări

- Datele Open-Meteo sunt date meteorologice furnizate pentru o locație geografică, nu măsurători efectuate direct de stația RNMCA B-12.
- Pot exista diferențe între condițiile meteorologice estimate pentru coordonatele selectate și condițiile reale din imediata apropiere a stației.
- Datele meteorologice și cele de calitate a aerului pot utiliza convenții temporale diferite.
- Agregarea zilnică poate ascunde variațiile meteorologice de scurtă durată.

---
