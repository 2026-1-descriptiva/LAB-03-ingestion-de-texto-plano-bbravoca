"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel
import re
import pandas as pd


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
    with open("files/input/clusters_report.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    data_lines = lines[4:]

    records = []
    current = None

    for line in data_lines:
        stripped = line.strip()
        if not stripped:
            continue

        match = re.match(
            r'^\s{1,8}(\d{1,2})\s{2,}(\d+)\s{2,}([\d,]+\s*%)\s{2,}(.+)$',
            line.rstrip(),
        )
        if match:
            if current:
                records.append(current)
            current = {
                "cluster": int(match.group(1)),
                "cantidad_de_palabras_clave": int(match.group(2)),
                "porcentaje_de_palabras_clave": match.group(3).strip(),
                "principales_palabras_clave": match.group(4).strip(),
            }
        elif current is not None:
            current["principales_palabras_clave"] += " " + stripped

    if current:
        records.append(current)

    df = pd.DataFrame(records)

    df["porcentaje_de_palabras_clave"] = (
        df["porcentaje_de_palabras_clave"]
        .str.replace(" %", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    df["principales_palabras_clave"] = df["principales_palabras_clave"].str.replace(
        r"\s+", " ", regex=True
    )
    df["principales_palabras_clave"] = df["principales_palabras_clave"].str.replace(
        r"\s*,\s*", ", ", regex=True
    )
    df["principales_palabras_clave"] = df["principales_palabras_clave"].str.replace(
        r"\.\s*$", "", regex=True
    )

    return df
