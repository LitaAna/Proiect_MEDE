# MEDE — Analiza calității aerului la stația B-12 din București

## Descrierea generală a proiectului

Acest proiect urmărește analiza relației dintre concentrația particulelor fine în suspensie (PM2.5) și condițiile meteorologice din București, folosind date de la stația de monitorizare a calității aerului B-12.

Scopul proiectului este de a explora modul în care temperatura aerului și viteza vântului sunt asociate cu variațiile concentrației PM2.5 și de a identifica eventuale tipare temporale sau episoade cu valori ridicate ale poluării.

**Întrebarea de cercetare:**

*Cum variază concentrația medie zilnică de PM2.5 la stația B-12 din București în funcție de temperatura medie și viteza medie a vântului?*

### Unitatea de analiză

**U12 — Senzor de calitate a aerului (stație × zi)**

Fiecare observație din setul de date final va reprezenta o zi calendaristică pentru stația B-12, împreună cu valorile zilnice ale concentrației PM2.5 și ale variabilelor meteorologice.

### Sursele de date

Pentru realizarea analizei sunt utilizate două surse complementare:

1. **RNMCA — Rețeaua Națională de Monitorizare a Calității Aerului:** furnizează concentrațiile de PM2.5 măsurate la stația B-12 din București.
2. **Open-Meteo Historical Weather:** furnizează temperatura aerului la 2 metri și viteza vântului la 10 metri pentru coordonatele geografice selectate din București.

Ambele seturi de date acoperă perioada **13 octombrie 2025 – 11 octombrie 2026**, la rezoluție temporală orară.

Datele vor fi agregate și aliniate la nivel zilnic pentru a permite compararea variabilelor.

### Obiectivele proiectului

- Pregătirea unui set de date comun, care integrează informațiile despre calitatea aerului și condițiile meteorologice.
- Explorarea evoluției temporale a concentrației PM2.5.
- Analizarea relației dintre PM2.5, temperatura medie și viteza medie a vântului.
- Identificarea unor posibile tipare și episoade cu concentrații ridicate de particule fine.
- Realizarea unei analize reproductibile, folosind metode de preprocesare, explorare și vizualizare a datelor.

---

## CP1 — Alinierea și pregătirea datelor

### Scopul etapei

Etapa CP1 are ca obiectiv pregătirea și alinierea celor două surse de date, astfel încât acestea să poată fi utilizate împreună în analiza ulterioară.

Datele RNMCA și Open-Meteo provin din sisteme diferite, motiv pentru care este necesară verificarea structurii, a unităților de măsură, a rezoluției temporale și a valorilor lipsă.

### Etapele procesului de aliniere

1. **Încărcarea datelor:** citirea fișierului Excel RNMCA și a fișierului CSV Open-Meteo.
2. **Verificarea datelor:** identificarea coloanelor relevante, a valorilor lipsă și a eventualelor neconcordanțe temporale.
3. **Standardizarea temporală:** verificarea fusurilor orare și a modului de reprezentare a intervalelor orare.
4. **Agregarea zilnică:** calcularea mediilor zilnice pentru PM2.5, temperatură și viteza vântului.
5. **Alinierea surselor:** combinarea observațiilor după data calendaristică.
6. **Evaluarea acoperirii:** determinarea numărului de zile comune, a observațiilor valide și a valorilor lipsă.

### Structura setului de date aliniat

Tabelul final va conține următoarele variabile:

| Variabilă | Descriere | Unitate |
|---|---|---|
| `date` | Data calendaristică | YYYY-MM-DD |
| `station_id` | Identificatorul stației | B-12 |
| `pm25_mean` | Concentrația medie zilnică PM2.5 | µg/m³ |
| `temperature_mean` | Temperatura medie zilnică | °C |
| `wind_speed_mean` | Viteza medie zilnică a vântului | km/h |
| `pm25_valid_hours` | Numărul de măsurători PM2.5 valide într-o zi | Număr |

### Rezultatul urmărit pentru CP1

Rezultatul acestei etape va fi un set de date aliniat la nivel zilnic, însoțit de un raport de acoperire care documentează perioada comună, numărul de observații disponibile și valorile lipsă.

Acest set de date va constitui baza pentru etapele următoare ale proiectului, dedicate explorării, vizualizării și interpretării relației dintre poluarea atmosferică și condițiile meteorologice.

**Stadiul actual:** sursele au fost descărcate și documentate prin Data Card-uri. Procesarea și alinierea finală a datelor sunt în curs de pregătire.
