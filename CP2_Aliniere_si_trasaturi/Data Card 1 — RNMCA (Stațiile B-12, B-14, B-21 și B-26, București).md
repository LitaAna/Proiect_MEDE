
# Data Card 1 — RNMCA (Stațiile B-12, B-14, B-21 și B-26, București)

## 1. Proveniența datelor

- **Sursă:** Rețeaua Națională de Monitorizare a Calității Aerului (RNMCA)
- **Portal oficial:** https://www.calitateaer.ro/public/home-page/?__locale=ro
- **Stații:** B-12, B-14, B-21, B-26, București
- **Fișier descărcat:** `B12_B14_B21_B26(2).xls` (convertit în `.xlsx` pentru procesare)
- **Format:** Excel (.xls / .xlsx)
- **Metoda de obținere:** export de raport din portalul CalitateAer
- **Tipul datelor:** concentrații orare de poluanți atmosferici; pentru proiect se extrage PM2.5

## 2. Perioada și rezoluția datelor

| **Caracteristică** | **Valoare** |
| --- | --- |
| Perioada | 13.10.2025 – 01.11.2026 (ultima zi parțială) |
| Rezoluție temporală originală | Orară; ore etichetate 01–24 |
| Rezoluție temporală pentru CP1 | Orară, pentru validare și aliniere |
| Rezoluție spațială | Patru stații fixe de monitorizare |
| Localizare | București, B-12, B-14, B-21, B-26 |
| Număr de înregistrări orare | 9.217 pentru fiecare stație; 36.868 stație–oră |
| Unitate de observație CP1 | Stație × oră |

Agregarea la intervale de șase ore se va face ulterior, în CP2; nu se aplică în această etapă.

## 3. Variabile și unități

| **Variabilă** | **Descriere** | **Unitate** |
| --- | --- | --- |
| Data | Data măsurătorii | YYYY-MM-DD |
| Ora | Eticheta intervalului orar RNMCA | 01–24 |
| Stație | Identificatorul punctului de monitorizare | B-12 / B-14 / B-21 / B-26 |
| PM2.5 | Concentrația particulelor fine | µg/m³ |
| PM10 | Poluant prezent în export, neutilizat în analiza curentă | µg/m³ |

Variabila principală pentru analiza MEDE este **PM2.5**.

## 4. Calitatea datelor și goluri

| **Stație** | **Înregistrări orare** | **Valori PM2.5 lipsă** |
| --- | ---: | ---: |
| B-12 | 9.217 | 66 |
| B-14 | 9.217 | 27 |
| B-21 | 9.217 | 1 |
| B-26 | 9.217 | 31 |

- **Reprezentarea valorilor lipsă:** celule goale / valori nenumerice, convertite în `NaN`.
- **Tratament:** fără completare cu zero și fără interpolare.
- **Validări:** conversie numerică, valori negative, acoperire temporală și corespondență cu sursa meteo.
- **Limitare de timp:** ultima zi, 01.11.2026, este parțială (în export apar doar orele 01 și 02).
- **Aliniere:** eticheta RNMCA `01` → ora locală `00:00` este o **ipoteză provizorie**, care trebuie verificată.

## 5. Licență și condiții de utilizare

Datele provin din portalul oficial RNMCA / CalitateAer.

**Document privind termenii RNMCA API:** https://www.calitateaer.ro/export/sites/default/.galleries/Legislation/Termeni-si-conditii.pdf_2063068895.pdf

Acest document privește utilizarea API; **aplicabilitatea la rapoartele Excel exportate trebuie verificată**. Fișierul furnizat nu declară o licență explicită. Datele sunt folosite în scop academic, cu atribuirea sursei.

## 6. Limitări

- Convenția etichetelor orare `01–24` nu este confirmată; alinierea cu meteo rămâne provizorie.
- Unele valori PM2.5 lipsesc, iar ultima zi este incompletă.
- Coordonatele exacte ale celor patru stații nu apar în exportul examinat.
- Datele reflectă patru puncte fixe și nu descriu automat întregul oraș.
- Nu se pot deduce cauze ale poluării doar din PM2.5 și variabilele meteo.

---
