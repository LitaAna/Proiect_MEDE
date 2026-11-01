#!/usr/bin/env python3
"""
Pipeline U12 - Validarea si alinierea datelor RNMCA si Open-Meteo.

Statii RNMCA: B-12, B-14, B-21, B-26
Variabile: PM2.5, temperatura, viteza vantului

Rulare:
    python pipeline_U12.py

Biblioteci:
    python -m pip install pandas openpyxl xlrd

"""

from pathlib import Path
import argparse
import json
import pandas as pd

#  CONFIGURARE


DEFAULT_FOLDER = Path(r"C:\Users\ANA\Desktop\CP2")

STATIONS = {
    "B-12": 4,
    "B-14": 10,
    "B-21": 16,
    "B-26": 22,
}



# IDENTIFICAREA FISIERELOR

def find_source(folder, pattern):
    """Gaseste automat fisierul original."""

    matches = sorted(folder.glob(pattern))

    if not matches:
        raise FileNotFoundError(
            f"Nu am gasit fisierul {pattern} in {folder}"
        )

    return matches[0]


# 3. INCARCAREA SI VALIDAREA DATELOR RNMCA


def load_rnmca(path):
    """Citeste concentratiile PM2.5 pentru cele patru statii."""

    raw = pd.read_excel(
        path,
        header=None,
        dtype=str
    )

    stamps = raw.iloc[:, 0].astype("string").str.strip()

    mask = stamps.str.fullmatch(
        r"\d{4}-\d{2}-\d{2} (?:0[1-9]|1\d|2[0-4])",
        na=False
    )

    if not mask.any():
        raise ValueError(
            "Nu am gasit randuri RNMCA de forma YYYY-MM-DD 01 ... 24."
        )

    rows = raw.loc[mask].copy()
    labels = stamps.loc[mask]

    dates = pd.to_datetime(
        labels.str.slice(0, 10)
    )

    hours = labels.str.slice(-2).astype(int)

    pieces = []

    for station, col in STATIONS.items():

        values = pd.to_numeric(
            rows.iloc[:, col]
            .astype("string")
            .str.replace(",", ".", regex=False)
            .str.strip(),
            errors="coerce"
        )

        # Valorile negative nu sunt concentratii valide.
        values = values.mask(values < 0)

        part = pd.DataFrame({
            "statie": station,
            "data_locala": dates.dt.strftime(
                "%Y-%m-%d"
            ).to_numpy(),
            "ora_locala_provizorie": (
                hours - 1
            ).map(
                lambda x: f"{x:02d}:00"
            ).to_numpy(),
            "ora_eticheta_rnmca": hours.to_numpy(),
            "pm25_ug_m3": values.to_numpy(),
        })

        pieces.append(part)

    result = pd.concat(
        pieces,
        ignore_index=True
    )

    result = result.sort_values([
        "data_locala",
        "ora_eticheta_rnmca",
        "statie"
    ]).reset_index(drop=True)

    return result


#  INCARCAREA SI VALIDAREA DATELOR OPEN-METEO


def load_meteo(path):
    """Citeste temperatura si viteza vantului."""

    with path.open(encoding="utf-8-sig") as handle:
        header = handle.readline().strip().split(",")
        vals = handle.readline().strip().split(",")

    metadata = (
        dict(zip(header, vals))
        if header and header[0] == "latitude"
        else {}
    )

    # Primele trei randuri contin antet si metadate.
    raw = pd.read_csv(
        path,
        skiprows=3,
        encoding="utf-8-sig"
    )

    raw.columns = [
        str(c).strip()
        for c in raw.columns
    ]

    time_col = next(
        (
            c for c in raw.columns
            if c.lower() == "time"
        ),
        None
    )

    temp_col = next(
        (
            c for c in raw.columns
            if c.startswith("temperature_2m")
        ),
        None
    )

    wind_col = next(
        (
            c for c in raw.columns
            if c.startswith("wind_speed_10m")
        ),
        None
    )

    if not all((time_col, temp_col, wind_col)):
        raise ValueError(
            f"Coloane Open-Meteo neasteptate: "
            f"{list(raw.columns)}"
        )

    # Conversie din UTC in ora locala Bucuresti.
    utc = pd.to_datetime(
        raw[time_col],
        errors="coerce",
        utc=True
    )

    good = utc.notna()

    local = utc.loc[good].dt.tz_convert(
        "Europe/Bucharest"
    )

    result = pd.DataFrame({
        "data_locala": local.dt.strftime(
            "%Y-%m-%d"
        ).to_numpy(),

        "ora_locala": local.dt.strftime(
            "%H:00"
        ).to_numpy(),

        "temperatura_c": pd.to_numeric(
            raw.loc[good, temp_col],
            errors="coerce"
        ).to_numpy(),

        "vant_kmh": pd.to_numeric(
            raw.loc[good, wind_col],
            errors="coerce"
        ).to_numpy(),

        "timestamp_utc": utc.loc[good].dt.strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ).to_numpy(),
    })

    # Identificarea orelor repetate la schimbarea orei.
    counts = result.groupby(
        ["data_locala", "ora_locala"],
        dropna=False
    ).size().rename(
        "numar_inregistrari_pentru_ora"
    )

    result = result.merge(
        counts.reset_index(),
        on=["data_locala", "ora_locala"],
        how="left"
    )

    return result, metadata



#  PIPELINE PRINCIPAL


def main():

    parser = argparse.ArgumentParser(
        description=(
            "Valideaza si aliniaza datele "
            "RNMCA PM2.5 si Open-Meteo."
        )
    )

    parser.add_argument(
        "--folder",
        type=Path,
        default=DEFAULT_FOLDER
    )

    parser.add_argument(
        "--rnmca",
        type=Path,
        default=None
    )

    parser.add_argument(
        "--meteo",
        type=Path,
        default=None
    )

    args = parser.parse_args()

    folder = args.folder.expanduser()

    if not folder.exists():
        raise FileNotFoundError(
            f"Folderul nu exista: {folder}"
        )

    rnmca_path = (
        args.rnmca
        or find_source(
            folder,
            "B12_B14_B21_B26*.xls*"
        )
    )

    meteo_path = (
        args.meteo
        or find_source(
            folder,
            "meteo_13.10.2025_01.11.2026*.csv"
        )
    )

    print("Pornire pipeline U12...", flush=True)
    print("RNMCA:", rnmca_path, flush=True)
    print("Meteo:", meteo_path, flush=True)


    #  CITIRE SI VALIDARE
    

    rn = load_rnmca(rnmca_path)

    print(
        "RNMCA citit:",
        len(rn),
        "randuri",
        flush=True
    )

    met, metadata = load_meteo(meteo_path)

    print(
        "Open-Meteo citit:",
        len(met),
        "randuri",
        flush=True
    )

    
    # IDENTIFICAREA ORELOR METEO


    counts = met.groupby(
        ["data_locala", "ora_locala"],
        as_index=False
    ).size().rename(
        columns={"size": "nr_meteo"}
    )

    
    unique_met = met.loc[
        met["numar_inregistrari_pentru_ora"] == 1
    ].copy()

    
    #  ALINIEREA DATELOR
    

    joined = rn.merge(
        counts,
        left_on=[
            "data_locala",
            "ora_locala_provizorie"
        ],
        right_on=[
            "data_locala",
            "ora_locala"
        ],
        how="left"
    )

    joined = joined.drop(
        columns=["ora_locala"]
    )

    joined = joined.merge(
        unique_met.drop(
            columns=[
                "numar_inregistrari_pentru_ora"
            ]
        ),
        left_on=[
            "data_locala",
            "ora_locala_provizorie"
        ],
        right_on=[
            "data_locala",
            "ora_locala"
        ],
        how="left"
    )

    joined = joined.drop(
        columns=["ora_locala"]
    )


    # STATUSUL ALINIERII
    joined["status_aliniere"] = "aliniat"

    joined.loc[
        joined["nr_meteo"].isna(),
        "status_aliniere"
    ] = "meteo_lipsa"

    joined.loc[
        joined["nr_meteo"].fillna(0) > 1,
        "status_aliniere"
    ] = "ambiguu_DST"

    joined["pm25_prezent"] = (
        joined["pm25_ug_m3"].notna()
    )

    joined["meteo_complet"] = (
        joined["temperatura_c"].notna()
        & joined["vant_kmh"].notna()
    )

    joined = joined.drop(
        columns=["nr_meteo"]
    )

    # EXPORTUL DATELOR VALIDATE


    validated_path = (
        folder / "date_validate_RNMCA_OpenMeteo.xlsx"
    )

    with pd.ExcelWriter(
        validated_path,
        engine="openpyxl"
    ) as writer:

        rn.to_excel(
            writer,
            sheet_name="RNMCA_validate",
            index=False
        )

        met.to_excel(
            writer,
            sheet_name="OpenMeteo_validate",
            index=False
        )
    #  EXPORTUL DATELOR ALINIATE
   

    aligned_path = (
        folder / "date_aliniate_RNMCA_meteo.xlsx"
    )

    with pd.ExcelWriter(
        aligned_path,
        engine="openpyxl"
    ) as writer:

        joined.to_excel(
            writer,
            sheet_name="Date_aliniate",
            index=False
        )

    #  RAPORTUL DE VALIDARE
  

    missing = rn.groupby("statie")[
        "pm25_ug_m3"
    ].apply(
        lambda x: x.isna().sum()
    )

    report = {
        "fisier_rnmca": rnmca_path.name,
        "fisier_meteo": meteo_path.name,
        "inregistrari_rnmca": len(rn),
        "inregistrari_meteo": len(met),
        "pm25_lipsa_pe_statie": {
            str(k): int(v)
            for k, v in missing.items()
        },
        "randuri_aliniate": len(joined),
        "status_aliniere": {
            str(k): int(v)
            for k, v in joined[
                "status_aliniere"
            ].value_counts().items()
        },
        "metadata_meteo": metadata,
        "avertismente": [
            "Orele RNMCA 01-24 sunt "
            "interpretate provizoriu ca 00-23.",
            "Orele ambigue DST nu sunt "
            "aliniate automat.",
            "Verificati coordonatele meteo "
            "pentru 01.11.2026.",
            "Valorile lipsa nu au fost "
            "interpolate."
        ]
    }

    report_path = (
        folder / "raport_validare_CP1.json"
    )

    report_path.write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    # AFISAREA REZULTATELOR

    print("\nFisiere generate:")
    print(validated_path)
    print(aligned_path)
    print(report_path)

    print(
        "\nInregistrari:",
        len(joined)
    )

    print(
        "Status aliniere:",
        report["status_aliniere"]
    )


if __name__ == "__main__":
    main()