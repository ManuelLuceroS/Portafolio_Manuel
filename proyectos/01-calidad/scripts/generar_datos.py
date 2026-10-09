"""
Genera 3000 inspecciones ficticias de calidad en una floricultora.

Semilla: 42. Con la misma semilla el archivo no cambia.

Supuestos:
- Cada fila es una inspección de un día, una finca y una variedad.
- La causa es la causa principal de esa inspección, no el detalle de cada ramo.
- Los ramos no conformes salen de una distribución binomial, así que nunca
  superan a los ramos revisados.
- Febrero, mayo y diciembre tienen más volumen. En esas semanas también sube
  un poco la no conformidad, igual que en las semanas 12 a 14 y 33 a 35.
"""

from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

SEMILLA = 42
rng = np.random.default_rng(SEMILLA)

CARPETA = Path(__file__).resolve().parents[1]
RUTA_DATOS = CARPETA / "datos"

FINCAS = [
    {
        "id_finca": 1,
        "finca": "Las Acacias",
        "zona": "Sabana norte",
        "base_nc": 0.041,
        "volumen": 165,
        "inspectores": ["Ana Ruiz", "Carlos Peña"],
    },
    {
        "id_finca": 2,
        "finca": "La Esperanza",
        "zona": "Sabana norte",
        "base_nc": 0.028,
        "volumen": 150,
        "inspectores": ["Laura Gómez", "Diego Mora"],
    },
    {
        "id_finca": 3,
        "finca": "San José",
        "zona": "Sabana occidente",
        "base_nc": 0.053,
        "volumen": 142,
        "inspectores": ["Marta López", "Julián Castro"],
    },
    {
        "id_finca": 4,
        "finca": "Los Pinos",
        "zona": "Sabana",
        "base_nc": 0.047,
        "volumen": 158,
        "inspectores": ["Sofía Herrera", "Andrés Vega"],
    },
    {
        "id_finca": 5,
        "finca": "El Mirador",
        "zona": "Tequendama",
        "base_nc": 0.081,
        "volumen": 128,
        "inspectores": ["Paola Díaz", "Camilo Ortiz"],
    },
]

VARIEDADES = {
    "Rosa roja": {
        "id_variedad": 1,
        "tipo": "Rosa",
        "ajuste": 0.006,
        "causas": {
            "Flor abierta": 0.32,
            "Tallo corto": 0.16,
            "Manchas": 0.14,
            "Deshidratación": 0.14,
            "Empaque deficiente": 0.10,
            "Plagas": 0.08,
            "Color irregular": 0.06,
        },
    },
    "Rosa blanca": {
        "id_variedad": 2,
        "tipo": "Rosa",
        "ajuste": -0.004,
        "causas": {
            "Flor abierta": 0.22,
            "Tallo corto": 0.18,
            "Manchas": 0.12,
            "Deshidratación": 0.16,
            "Empaque deficiente": 0.12,
            "Plagas": 0.08,
            "Color irregular": 0.12,
        },
    },
    "Clavel": {
        "id_variedad": 3,
        "tipo": "Clavel",
        "ajuste": 0.010,
        "causas": {
            "Flor abierta": 0.12,
            "Tallo corto": 0.34,
            "Manchas": 0.14,
            "Deshidratación": 0.10,
            "Empaque deficiente": 0.12,
            "Plagas": 0.10,
            "Color irregular": 0.08,
        },
    },
    "Crisantemo": {
        "id_variedad": 4,
        "tipo": "Crisantemo",
        "ajuste": 0.002,
        "causas": {
            "Flor abierta": 0.10,
            "Tallo corto": 0.14,
            "Manchas": 0.32,
            "Deshidratación": 0.12,
            "Empaque deficiente": 0.12,
            "Plagas": 0.12,
            "Color irregular": 0.08,
        },
    },
    "Girasol": {
        "id_variedad": 5,
        "tipo": "Girasol",
        "ajuste": 0.014,
        "causas": {
            "Flor abierta": 0.12,
            "Tallo corto": 0.10,
            "Manchas": 0.10,
            "Deshidratación": 0.34,
            "Empaque deficiente": 0.14,
            "Plagas": 0.12,
            "Color irregular": 0.08,
        },
    },
    "Alstroemeria": {
        "id_variedad": 6,
        "tipo": "Alstroemeria",
        "ajuste": 0.0,
        "causas": {
            "Flor abierta": 0.14,
            "Tallo corto": 0.12,
            "Manchas": 0.12,
            "Deshidratación": 0.12,
            "Empaque deficiente": 0.12,
            "Plagas": 0.08,
            "Color irregular": 0.30,
        },
    },
}

NOMBRES_VARIEDAD = list(VARIEDADES)


def dias_habiles(inicio, fin):
    dias = []
    actual = inicio
    while actual <= fin:
        if actual.weekday() < 5:
            dias.append(actual)
        actual += timedelta(days=1)
    return dias


def elegir_causa(variedad, semana, mes):
    pesos = dict(VARIEDADES[variedad]["causas"])
    if semana in (12, 13, 14):
        pesos["Plagas"] += 0.28
    if mes in (8, 9) and variedad in ("Rosa roja", "Girasol"):
        pesos["Deshidratación"] += 0.22
    if mes == 12:
        pesos["Empaque deficiente"] += 0.16
    if mes in (2, 5) and variedad == "Rosa roja":
        pesos["Flor abierta"] += 0.18

    etiquetas = list(pesos)
    valores = np.array([pesos[causa] for causa in etiquetas], dtype=float)
    valores = valores / valores.sum()
    indice = int(rng.choice(len(etiquetas), p=valores))
    return etiquetas[indice]


def armar_plan(dias):
    """Dos inspecciones por finca y día, y una tercera repartida en el año."""
    plan = []
    indice = 0
    for dia in dias:
        for finca in FINCAS:
            cantidad = 3 if indice % 3 == 0 else 2
            indice += 1
            for _ in range(cantidad):
                plan.append((dia, finca))

    if len(plan) > 3000:
        return plan[:3000]
    if len(plan) < 3000:
        faltan = 3000 - len(plan)
        for dia in reversed(dias):
            for finca in FINCAS:
                if faltan == 0:
                    return plan
                plan.append((dia, finca))
                faltan -= 1
    return plan


def crear_registro(dia, finca, variedad):
    iso = dia.isocalendar()
    mes = dia.month
    semana = iso.week

    media = finca["volumen"]
    if dia.weekday() == 0:
        media *= 1.06
    if mes in (2, 5, 12):
        media *= 1.12

    revisados = int(round(rng.normal(media, 16)))
    revisados = min(260, max(70, revisados))

    choque = 0.0
    if semana in (12, 13, 14):
        choque += 0.030
    if semana in (33, 34, 35):
        choque += 0.020
    if mes in (2, 5, 12):
        choque += 0.010
    if mes in (3, 4) and variedad == "Rosa roja":
        choque += 0.008

    tasa = finca["base_nc"] + VARIEDADES[variedad]["ajuste"] + choque
    tasa += float(rng.normal(0, 0.005))
    tasa = min(0.25, max(0.008, tasa))

    no_conformes = int(rng.binomial(revisados, tasa))
    if no_conformes == 0:
        causa = "Sin no conformidad"
    else:
        causa = elegir_causa(variedad, semana, mes)

    inspector = str(rng.choice(finca["inspectores"]))
    return {
        "fecha": dia,
        "finca": finca["finca"],
        "variedad": variedad,
        "ramos_revisados": revisados,
        "ramos_no_conformes": no_conformes,
        "causa_no_conformidad": causa,
        "inspector": inspector,
        "semana": semana,
        "anio": iso.year,
    }


def main():
    dias = dias_habiles(datetime(2025, 1, 2), datetime(2025, 12, 26))
    plan = armar_plan(dias)
    if len(plan) != 3000:
        raise SystemExit(f"El plan quedó con {len(plan)} registros, se esperaban 3000.")

    cursor = 0
    filas = []
    for dia, finca in plan:
        variedad = NOMBRES_VARIEDAD[cursor % len(NOMBRES_VARIEDAD)]
        cursor += 1
        filas.append(crear_registro(dia, finca, variedad))

    df = pd.DataFrame(filas)
    df = df.sort_values(["fecha", "finca", "variedad"]).reset_index(drop=True)
    df.insert(0, "id_inspeccion", df.index + 1)
    df["fecha"] = pd.to_datetime(df["fecha"]).dt.strftime("%Y-%m-%d")

    if (df["ramos_no_conformes"] > df["ramos_revisados"]).any():
        raise SystemExit("Hay ramos no conformes por encima de los revisados.")
    if (df["ramos_revisados"] <= 0).any() or (df["ramos_no_conformes"] < 0).any():
        raise SystemExit("Hay cantidades negativas o revisados en cero.")
    if df["fecha"].nunique() < 150:
        raise SystemExit("Las fechas quedaron demasiado concentradas.")

    RUTA_DATOS.mkdir(parents=True, exist_ok=True)
    df.to_csv(RUTA_DATOS / "datos_calidad.csv", index=False, encoding="utf-8")

    fincas = pd.DataFrame(
        [
            {"id_finca": f["id_finca"], "finca": f["finca"], "zona": f["zona"]}
            for f in FINCAS
        ]
    )
    variedades = pd.DataFrame(
        [
            {
                "id_variedad": datos["id_variedad"],
                "variedad": nombre,
                "tipo": datos["tipo"],
            }
            for nombre, datos in VARIEDADES.items()
        ]
    )
    fincas.to_csv(RUTA_DATOS / "fincas.csv", index=False, encoding="utf-8")
    variedades.to_csv(RUTA_DATOS / "variedades.csv", index=False, encoding="utf-8")

    print(f"Registros: {len(df)}")
    print(f"Rango: {df['fecha'].min()} a {df['fecha'].max()}")
    print(f"Archivo: {RUTA_DATOS / 'datos_calidad.csv'}")


if __name__ == "__main__":
    main()
