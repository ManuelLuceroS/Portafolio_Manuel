"""
Genera 1500 registros ficticios de seguimiento operativo.

Semilla: 21.

Cada fila es una actividad de un día. La meta y el resultado usan la misma
unidad dentro del área, para que el cumplimiento del área tenga sentido.

Regla del estado:
- Cumplida: resultado >= meta
- Parcial: resultado >= 80 % de la meta y menor que la meta
- No cumplida: resultado < 80 % de la meta

Febrero baja un poco el cumplimiento. Noviembre queda un poco mejor.
Mantenimiento parte de una base más baja que el resto de áreas.
"""

from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

SEMILLA = 21
rng = np.random.default_rng(SEMILLA)

CARPETA = Path(__file__).resolve().parents[1]
RUTA_DATOS = CARPETA / "datos"

ACTIVIDADES = [
    {"area": "Producción", "actividad": "Corte en cultivo", "unidad": "ramos", "meta_media": 360, "horas_media": 8, "base": 0.95},
    {"area": "Producción", "actividad": "Preparación de ramos", "unidad": "ramos", "meta_media": 240, "horas_media": 8, "base": 0.92},
    {"area": "Calidad", "actividad": "Inspección de lote", "unidad": "lotes", "meta_media": 30, "horas_media": 7, "base": 0.99},
    {"area": "Calidad", "actividad": "Reinspección de lote", "unidad": "lotes", "meta_media": 18, "horas_media": 6, "base": 0.97},
    {"area": "Logística", "actividad": "Despacho urbano", "unidad": "despachos", "meta_media": 16, "horas_media": 8, "base": 0.90},
    {"area": "Logística", "actividad": "Despacho regional", "unidad": "despachos", "meta_media": 8, "horas_media": 7, "base": 0.86},
    {"area": "Empaque", "actividad": "Armado de cajas", "unidad": "cajas", "meta_media": 130, "horas_media": 8, "base": 0.91},
    {"area": "Empaque", "actividad": "Etiquetado", "unidad": "cajas", "meta_media": 140, "horas_media": 7, "base": 0.88},
    {"area": "Mantenimiento", "actividad": "Revisión de equipos", "unidad": "órdenes", "meta_media": 8, "horas_media": 7, "base": 0.82},
    {"area": "Mantenimiento", "actividad": "Mantenimiento preventivo", "unidad": "órdenes", "meta_media": 5, "horas_media": 6, "base": 0.74},
]

RESPONSABLES = {
    "Producción": ["Helena Cruz", "Mario Pineda"],
    "Calidad": ["Natalia Ríos", "Esteban Gil"],
    "Logística": ["Valentina León", "Oscar Duarte"],
    "Empaque": ["Camila Torres", "Felipe Rojas"],
    "Mantenimiento": ["Ricardo Salazar", "Diana Pardo"],
}

FACTOR_MES = {
    1: 0.98,
    2: 0.94,
    3: 0.97,
    4: 1.00,
    5: 1.01,
    6: 0.99,
    7: 0.98,
    8: 1.00,
    9: 1.01,
    10: 1.02,
    11: 1.03,
    12: 0.97,
}


def dias_habiles():
    dias = []
    actual = datetime(2025, 1, 2)
    fin = datetime(2025, 12, 26)
    while actual <= fin:
        if actual.weekday() < 5:
            dias.append(actual)
        actual += timedelta(days=1)
    return dias


def estado_de(resultado, meta):
    # 80 % se compara con enteros: resultado / meta >= 0.8
    if resultado >= meta:
        return "Cumplida"
    if resultado * 5 >= meta * 4:
        return "Parcial"
    return "No cumplida"


def main():
    dias = dias_habiles()
    filas = []
    indice = 0

    for dia in dias:
        for _ in range(6):
            if len(filas) >= 1500:
                break
            actividad = ACTIVIDADES[indice % len(ACTIVIDADES)]
            indice += 1

            meta = int(round(rng.normal(actividad["meta_media"], actividad["meta_media"] * 0.08)))
            meta = max(1, meta)

            tasa = actividad["base"] * FACTOR_MES[dia.month]
            tasa += float(rng.normal(0, 0.035))
            tasa = min(1.15, max(0.50, tasa))
            resultado = max(0, int(round(meta * tasa)))

            horas = int(round(rng.normal(actividad["horas_media"], 0.7)))
            horas = min(12, max(1, horas))

            filas.append(
                {
                    "fecha": dia,
                    "area": actividad["area"],
                    "responsable": str(rng.choice(RESPONSABLES[actividad["area"]])),
                    "actividad": actividad["actividad"],
                    "meta": meta,
                    "resultado": resultado,
                    "horas_trabajadas": horas,
                    "estado": estado_de(resultado, meta),
                }
            )
        if len(filas) >= 1500:
            break

    if len(filas) != 1500:
        raise SystemExit(f"Se generaron {len(filas)} registros, se esperaban 1500.")

    df = pd.DataFrame(filas)
    df = df.sort_values(["fecha", "area", "actividad"]).reset_index(drop=True)
    df.insert(0, "id_registro", df.index + 1)
    df["fecha"] = pd.to_datetime(df["fecha"]).dt.strftime("%Y-%m-%d")

    if (df["meta"] <= 0).any() or (df["horas_trabajadas"] <= 0).any():
        raise SystemExit("Hay metas u horas en cero. No se puede calcular el indicador.")
    if (df["resultado"] < 0).any():
        raise SystemExit("Hay resultados negativos.")

    catalogo = pd.DataFrame(ACTIVIDADES)[["actividad", "area", "unidad"]]

    RUTA_DATOS.mkdir(parents=True, exist_ok=True)
    df.to_csv(RUTA_DATOS / "datos_operativos.csv", index=False, encoding="utf-8")
    catalogo.to_csv(RUTA_DATOS / "catalogo_actividades.csv", index=False, encoding="utf-8")

    print(f"Registros: {len(df)}")
    print(f"Rango: {df['fecha'].min()} a {df['fecha'].max()}")
    print(df["estado"].value_counts().to_string())
    print(f"Archivo: {RUTA_DATOS / 'datos_operativos.csv'}")


if __name__ == "__main__":
    main()
