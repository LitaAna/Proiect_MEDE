# Data Card 1 — RNMCA (Stația B-12, București)

## 1. Proveniența datelor

- **Sursă:** Rețeaua Națională de Monitorizare a Calității Aerului (RNMCA)
- **Portal oficial:** https://www.calitateaer.ro/public/home-page/?__locale=ro
- **Stație:** B-12, București
- **Fișier descărcat:** `Raport_20261019122509.xls`
- **Format:** Excel (.xls)
- **Metoda de obținere:** export de raport din portalul CalitateAer
- **Tipul datelor:** concentrații de poluanți atmosferici

## 2. Perioada și rezoluția datelor

| Caracteristică | Valoare |
|---|---|
| Perioada | 13.10.2025 – 11.10.2026 |
| Rezoluție temporală originală | Orară |
| Rezoluție temporală pentru proiect | Zilnică |
| Rezoluție spațială | O stație fixă de monitorizare |
| Localizare | B-12, București |
| Număr de înregistrări orare | 8.724 |
| Unitate de analiză | Stație × zi |

Datele orare PM2.5 vor fi agregate prin calcularea mediei zilnice.

## 3. Variabile și unități

| Variabilă | Descriere | Unitate |
|---|---|---|
| Data | Data măsurătorii | YYYY-MM-DD |
| Ora | Intervalul orar | Oră |
| PM2.5 | Concentrația particulelor fine | µg/m³ |
| PM10 | Concentrația particulelor în suspensie | µg/m³ |

Variabila principală pentru analiza MEDE este **PM2.5**.

## 4. Calitatea datelor și goluri

În verificarea preliminară au fost identificate valori lipsă pentru PM2.5.

- **Valori PM2.5 lipsă identificate:** 65
- **Reprezentarea valorilor lipsă:** simbolul `-`
- **Tratament planificat:** conversia valorilor lipsă în `NaN`, fără înlocuirea lor cu zero
- **Agregare:** media zilnică a măsurătorilor valide
- **Verificări suplimentare:** zile incomplete, duplicate și intervale fără observații

Numărul final de zile complete va fi calculat după alinierea cu Open-Meteo.

## 5. Licență și condiții de utilizare

Datele provin din portalul oficial RNMCA / CalitateAer.

**Document privind termenii RNMCA API:**

https://www.calitateaer.ro/export/sites/default/.galleries/Legislation/Termeni-si-conditii.pdf_2063068895.pdf

Documentul descrie condițiile de utilizare a datelor obținute prin API, inclusiv atribuirea sursei și documentarea prelucrărilor.

**Limitare:** raportul utilizat în proiect a fost descărcat din portal în format Excel, nu prin API. Aplicabilitatea exactă a termenilor API la exporturile Excel necesită confirmare.

Datele vor fi utilizate în scop academic, cu indicarea provenienței.

## 6. Limitări

- Datele provin de la o singură stație de monitorizare.
- Există măsurători PM2.5 lipsă.
- Unele zile pot avea mai puțin de 24 de observații valide.
- Convenția orelor `01–24` trebuie verificată înainte de aliniere.
- Rezultatele nu pot fi generalizate automat la întregul București.
- Coordonatele exacte ale stației și metadatele privind calibrarea necesită verificare.

