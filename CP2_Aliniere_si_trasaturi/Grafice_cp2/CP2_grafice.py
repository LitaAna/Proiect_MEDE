
from pathlib import Path
import re
import unicodedata

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ============================================================
# 1. CONFIGURARE
# ============================================================

FOLDER = Path(r"C:\Users\ANA\Desktop\CP2")
EXCEL = FOLDER / "CP2_matrice.xlsx"
OUTPUT = FOLDER / "grafice_CP2"

OUTPUT.mkdir(parents=True, exist_ok=True)

STATII = ["B-12", "B-14", "B-21", "B-26"]
ANOTIMPURI = ["Iarna", "Primavara", "Vara", "Toamna"]
INTERVALE = ["Noapte", "Dimineata", "Dupa-amiaza", "Seara"]

CULORI = {
    "Iarna": "#4779B5",
    "Primavara": "#55A66A",
    "Vara": "#E5A13D",
    "Toamna": "#B86E62"
}

plt.rcParams.update({
    "font.size": 10,
    "axes.titlesize": 13,
    "axes.labelsize": 10,
    "figure.dpi": 120
})


# ============================================================
# 2. FUNCTII AJUTATOARE
# ============================================================

def normalize(text):
    """Elimina diferentele de majuscule, accente si simboluri."""
    text = unicodedata.normalize("NFKD", str(text))
    text = "".join(
        ch for ch in text
        if not unicodedata.combining(ch)
    )
    text = text.lower()
    return re.sub(r"[^a-z0-9]+", "_", text).strip("_")


def find_column(data, candidates):
    normalized = {
        normalize(column): column
        for column in data.columns
    }

    for candidate in candidates:
        key = normalize(candidate)
        if key in normalized:
            return normalized[key]

    raise ValueError(
        "\nNu am gasit coloana cautata.\n"
        f"Variante cautate: {candidates}\n"
        f"Coloane existente: {list(data.columns)}"
    )


def normalize_season(value):
    key = normalize(value)

    mapping = {
        "iarna": "Iarna",
        "primavara": "Primavara",
        "vara": "Vara",
        "toamna": "Toamna",
        "winter": "Iarna",
        "spring": "Primavara",
        "summer": "Vara",
        "autumn": "Toamna",
        "fall": "Toamna"
    }

    return mapping.get(key)


def normalize_interval(value):
    key = normalize(value)

    mapping = {
        "noapte": "Noapte",
        "night": "Noapte",
        "00_05": "Noapte",
        "00_05_59": "Noapte",
        "00_06": "Noapte",

        "dimineata": "Dimineata",
        "morning": "Dimineata",
        "06_11": "Dimineata",
        "06_11_59": "Dimineata",
        "06_12": "Dimineata",

        "dupa_amiaza": "Dupa-amiaza",
        "dupaamiaza": "Dupa-amiaza",
        "afternoon": "Dupa-amiaza",
        "12_17": "Dupa-amiaza",
        "12_17_59": "Dupa-amiaza",
        "12_18": "Dupa-amiaza",

        "seara": "Seara",
        "evening": "Seara",
        "18_23": "Seara",
        "18_23_59": "Seara",
        "18_24": "Seara"
    }

    return mapping.get(key)


def save_figure(filename):
    plt.tight_layout()
    plt.savefig(
        OUTPUT / filename,
        dpi=220,
        bbox_inches="tight"
    )
    plt.close()


def make_table(data, value_column):
    """Tabel 4 anotimpuri x 4 intervale."""
    return data.pivot_table(
        index="Interval",
        columns="Anotimp",
        values=value_column,
        aggfunc="mean"
    ).reindex(
        index=INTERVALE,
        columns=ANOTIMPURI
    )


def grouped_bar(table, title, filename):
    """Grafic cu 4 intervale si cate 4 bare pentru anotimpuri."""

    fig, ax = plt.subplots(figsize=(11, 6))

    x = np.arange(len(INTERVALE))
    width = 0.19

    for index, anotimp in enumerate(ANOTIMPURI):
        offset = (index - 1.5) * width

        ax.bar(
            x + offset,
            table[anotimp],
            width=width,
            label=anotimp,
            color=CULORI[anotimp]
        )

    ax.set_xticks(x)
    ax.set_xticklabels([
        "Noapte",
        "Dimineata",
        "Dupa-amiaza",
        "Seara"
    ])

    ax.set_title(title)
    ax.set_xlabel("Intervalul zilei")
    ax.set_ylabel("Concentratia medie PM2.5 (µg/m³)")
    ax.legend(title="Anotimp", ncol=4)
    ax.grid(axis="y", alpha=0.2)
    ax.set_axisbelow(True)

    save_figure(filename)


def heatmap(table, title, filename):
    """Heatmap 4 anotimpuri x 4 intervale."""

    values = table.T.to_numpy(dtype=float)

    fig, ax = plt.subplots(figsize=(10, 5.5))

    masked = np.ma.masked_invalid(values)

    image = ax.imshow(
        masked,
        cmap="YlOrRd",
        aspect="auto"
    )

    ax.set_xticks(range(len(INTERVALE)))
    ax.set_xticklabels(INTERVALE)

    ax.set_yticks(range(len(ANOTIMPURI)))
    ax.set_yticklabels(ANOTIMPURI)

    ax.set_xlabel("Intervalul zilei")
    ax.set_ylabel("Anotimp")
    ax.set_title(title)

    for i in range(len(ANOTIMPURI)):
        for j in range(len(INTERVALE)):
            value = values[i, j]

            if np.isfinite(value):
                ax.text(
                    j, i,
                    f"{value:.1f}",
                    ha="center",
                    va="center",
                    fontsize=11
                )
            else:
                ax.text(
                    j, i,
                    "N/A",
                    ha="center",
                    va="center"
                )

    fig.colorbar(
        image,
        ax=ax,
        label="PM2.5 mediu (µg/m³)"
    )

    save_figure(filename)


# ============================================================
# 3. CITIREA MATRICEI
# ============================================================

if not EXCEL.exists():
    raise FileNotFoundError(
        f"Nu exista fisierul:\n{EXCEL}"
    )

df = pd.read_excel(
    EXCEL,
    sheet_name="Matrice_CP2"
)

print("Coloanele gasite in Excel:")
for column in df.columns:
    print(" -", column)

COL_STATIE = find_column(df, [
    "Statie",
    "Stație"
])

COL_DATA = find_column(df, [
    "Data",
    "Date"
])

COL_ANOTIMP = find_column(df, [
    "Anotimp",
    "Sezon"
])

COL_INTERVAL = find_column(df, [
    "Interval 6h",
    "Interval_6h",
    "Interval",
    "Perioada zilei"
])

COL_PM = find_column(df, [
    "RNMCA | PM2.5 mediu (µg/m³)",
    "PM2.5 mediu (µg/m³)",
    "PM25_mediu_ug_m3",
    "PM25_medie",
    "PM25_ug_m3",
    "PM25_mean"
])

COL_STATUS = find_column(df, [
    "Status interval",
    "Status_interval",
    "Completitudine",
    "Interval complet"
])


# ============================================================
# 4. PREGATIREA DATELOR
# ============================================================

df = df.rename(columns={
    COL_STATIE: "Statie",
    COL_DATA: "Data",
    COL_ANOTIMP: "Anotimp",
    COL_INTERVAL: "Interval",
    COL_PM: "PM25",
    COL_STATUS: "Status"
})

df["Data"] = pd.to_datetime(
    df["Data"],
    errors="coerce"
).dt.normalize()

df["Statie"] = (
    df["Statie"]
    .astype(str)
    .str.strip()
    .str.upper()
)

df["Anotimp"] = df["Anotimp"].apply(
    normalize_season
)

df["Interval"] = df["Interval"].apply(
    normalize_interval
)

df["PM25"] = pd.to_numeric(
    df["PM25"],
    errors="coerce"
)

status = (
    df["Status"]
    .astype(str)
    .str.strip()
    .str.lower()
)

complete = status.isin([
    "complet",
    "completa",
    "complete",
    "true",
    "1",
    "da"
])

total_initial = len(df)

df = df.loc[complete].copy()

df = df.dropna(subset=[
    "Data",
    "Anotimp",
    "Interval",
    "PM25"
])

df = df[df["Statie"].isin(STATII)].copy()

print("\nRanduri initiale:", total_initial)
print("Randuri complete si valide:", len(df))
print("Anotimpuri:", sorted(df["Anotimp"].unique()))
print("Intervale:", sorted(df["Interval"].unique()))
print("Statii:", sorted(df["Statie"].unique()))

if df.empty:
    raise ValueError(
        "Nu au ramas date valide dupa filtrare. "
        "Verifica valorile din coloanele Status si Interval."
    )

# Verificam unicitatea: o statie / zi / interval
keys = ["Statie", "Data", "Interval"]

duplicates = df.duplicated(keys, keep=False)

if duplicates.any():
    raise ValueError(
        "Exista combinatii duplicate Statie-Data-Interval. "
        "Verifica matricea inainte de calcul."
    )


# ============================================================
# 5. GRAFICE INDIVIDUALE PENTRU FIECARE STATIE
# ============================================================

for statie in STATII:

    subset = df[df["Statie"] == statie]

    if subset.empty:
        print(f"Atentie: nu exista date pentru {statie}")
        continue

    table = make_table(
        subset,
        "PM25"
    )

    print(f"\nMedii pentru {statie}:")
    print(table.round(2))

    grouped_bar(
        table,
        f"PM2.5 - intervalele zilei in fiecare anotimp | {statie}",
        f"01_bare_{statie}.png"
    )

    heatmap(
        table,
        f"PM2.5 - anotimp x interval | {statie}",
        f"02_heatmap_{statie}.png"
    )


# ============================================================
# 6. MEDIA CELOR PATRU STATII
# ============================================================

# O valoare medie pentru fiecare zi si interval.
# Folosim doar combinatiile cu toate cele 4 statii.

general = (
    df.groupby(
        ["Data", "Interval"],
        as_index=False
    )
    .agg(
        PM25_general=("PM25", "mean"),
        N_statii=("Statie", "nunique")
    )
)

general = general[
    general["N_statii"] == 4
].copy()

# Determinam anotimpul din matrice, pentru aceleasi date.
season_lookup = (
    df[["Data", "Anotimp"]]
    .drop_duplicates()
)

general = general.merge(
    season_lookup,
    on="Data",
    how="left",
    validate="many_to_one"
)

if general.empty:
    raise ValueError(
        "Nu exista intervale comune complete pentru toate "
        "cele patru statii."
    )

print(
    "\nIntervale complete comune celor 4 statii:",
    len(general)
)

# Media celor patru statii pentru fiecare combinatie
# anotimp x interval al zilei.

table_general = make_table(
    general,
    "PM25_general"
)

print("\nMEDIA GENERALA A CELOR PATRU STATII:")
print(table_general.round(2))

grouped_bar(
    table_general,
    "PM2.5 - media celor 4 statii | intervale in fiecare anotimp",
    "03_bare_MEDIA_BUCURESTI.png"
)

heatmap(
    table_general,
    "PM2.5 - media celor 4 statii | anotimp x interval",
    "04_heatmap_MEDIA_BUCURESTI.png"
)


# ============================================================
# 7. REZULTAT FINAL
# ============================================================

print("\nGATA!")
print("Graficele au fost salvate in:")
print(OUTPUT)

print("\nTotal asteptat: 10 imagini PNG.")
print("Nu au fost create fisiere CSV suplimentare.")
