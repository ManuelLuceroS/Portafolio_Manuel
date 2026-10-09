"""
Lee datos_calidad.csv y calcula los indicadores del dashboard.

El porcentaje de un grupo es la suma de ramos no conformes dividida por la
suma de ramos revisados. No es el promedio de los porcentajes de cada fila.
"""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

CARPETA = Path(__file__).resolve().parents[1]
RAIZ = Path(__file__).resolve().parents[3]
DATOS = CARPETA / "datos" / "datos_calidad.csv"
GRAFICOS = CARPETA / "graficos"
SALIDAS_JSON = [
    RAIZ / "public" / "datos" / "calidad.json",
    CARPETA / "datos" / "resumen_calidad.json",
]

MESES = {
    1: "Ene",
    2: "Feb",
    3: "Mar",
    4: "Abr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Ago",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dic",
}


def numero(valor, decimales=2):
    return float(f"{float(valor):.{decimales}f}")


def miles(valor):
    return f"{int(valor):,}".replace(",", ".")


def texto_pct(valor):
    return f"{float(valor):.2f}".replace(".", ",")


def porcentaje(parte, total):
    if total == 0:
        raise SystemExit("No se puede dividir por cero al calcular el porcentaje.")
    return numero(parte / total * 100)


def validar(df):
    columnas = [
        "id_inspeccion",
        "fecha",
        "finca",
        "variedad",
        "ramos_revisados",
        "ramos_no_conformes",
        "causa_no_conformidad",
        "inspector",
        "semana",
        "anio",
    ]
    if list(df.columns) != columnas:
        raise SystemExit("Las columnas de datos_calidad.csv no coinciden.")
    if len(df) != 3000:
        raise SystemExit(f"Se esperaban 3000 filas y hay {len(df)}.")
    if df.isna().any().any():
        raise SystemExit("Hay valores nulos.")
    if (df["ramos_no_conformes"] > df["ramos_revisados"]).any():
        raise SystemExit("Hay no conformes por encima de los revisados.")
    if (df["ramos_revisados"] <= 0).any() or (df["ramos_no_conformes"] < 0).any():
        raise SystemExit("Hay cantidades inválidas.")

    iso = df["fecha"].dt.isocalendar()
    if not (iso.week.astype(int) == df["semana"].astype(int)).all():
        raise SystemExit("La semana del archivo no coincide con la fecha.")
    if not (iso.year.astype(int) == df["anio"].astype(int)).all():
        raise SystemExit("El año ISO del archivo no coincide con la fecha.")


def resumir(df, columna):
    tabla = (
        df.groupby(columna, as_index=False)
        .agg(
            revisados=("ramos_revisados", "sum"),
            no_conformes=("ramos_no_conformes", "sum"),
        )
        .sort_values("no_conformes", ascending=False)
    )
    tabla["porcentaje"] = [
        porcentaje(nc, rev) for nc, rev in zip(tabla["no_conformes"], tabla["revisados"])
    ]
    return tabla


def guardar_barras(tabla, columna, titulo, archivo):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(tabla[columna], tabla["porcentaje"], color="#3B82F6")
    ax.set_title(titulo)
    ax.set_ylabel("% no conformidad")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    fig.savefig(GRAFICOS / archivo, dpi=120)
    plt.close(fig)


def main():
    df = pd.read_csv(DATOS, encoding="utf-8")
    df["fecha"] = pd.to_datetime(df["fecha"])
    validar(df)

    total_revisados = int(df["ramos_revisados"].sum())
    total_nc = int(df["ramos_no_conformes"].sum())
    pct_general = porcentaje(total_nc, total_revisados)

    por_finca = resumir(df, "finca").sort_values("porcentaje", ascending=False)
    por_variedad = resumir(df, "variedad").sort_values("porcentaje", ascending=False)

    causas = (
        df[df["ramos_no_conformes"] > 0]
        .groupby("causa_no_conformidad", as_index=False)
        .agg(ramos=("ramos_no_conformes", "sum"))
        .sort_values("ramos", ascending=False)
    )
    causas["porcentaje"] = [porcentaje(valor, total_nc) for valor in causas["ramos"]]

    semanal = (
        df.groupby(["anio", "semana"], as_index=False)
        .agg(
            revisados=("ramos_revisados", "sum"),
            no_conformes=("ramos_no_conformes", "sum"),
        )
        .sort_values(["anio", "semana"])
    )
    semanal["porcentaje"] = [
        porcentaje(nc, rev) for nc, rev in zip(semanal["no_conformes"], semanal["revisados"])
    ]

    df["mes_num"] = df["fecha"].dt.month
    df["mes"] = df["fecha"].dt.strftime("%Y-%m")
    mensual = (
        df.groupby(["mes", "mes_num"], as_index=False)
        .agg(
            revisados=("ramos_revisados", "sum"),
            no_conformes=("ramos_no_conformes", "sum"),
        )
        .sort_values("mes")
    )
    mensual["porcentaje"] = [
        porcentaje(nc, rev) for nc, rev in zip(mensual["no_conformes"], mensual["revisados"])
    ]

    peor_finca = por_finca.iloc[0]
    mejor_finca = por_finca.iloc[-1]
    peor_variedad = por_variedad.iloc[0]
    causa_principal = causas.iloc[0]
    peor_mes = mensual.sort_values("porcentaje", ascending=False).iloc[0]
    mejor_mes = mensual.sort_values("porcentaje", ascending=True).iloc[0]

    explicacion = (
        f"Se sumaron los ramos revisados y los ramos no conformes de las {len(df)} inspecciones. "
        f"El porcentaje general es {texto_pct(pct_general)} % "
        f"({miles(total_nc)} de {miles(total_revisados)} ramos). "
        f"{peor_finca['finca']} concentra el porcentaje más alto "
        f"({texto_pct(peor_finca['porcentaje'])} %) y {mejor_finca['finca']} el más bajo "
        f"({texto_pct(mejor_finca['porcentaje'])} %). "
        f"La causa principal, contada en ramos, es {causa_principal['causa_no_conformidad']}."
    )

    conclusiones = [
        f"De {miles(total_revisados)} ramos revisados, {miles(total_nc)} quedaron no conformes ({texto_pct(pct_general)} %).",
        f"La finca con mayor no conformidad fue {peor_finca['finca']} ({texto_pct(peor_finca['porcentaje'])} %) y la de menor fue {mejor_finca['finca']} ({texto_pct(mejor_finca['porcentaje'])} %).",
        f"La variedad con mayor no conformidad fue {peor_variedad['variedad']} ({texto_pct(peor_variedad['porcentaje'])} %).",
        f"La causa más frecuente fue {causa_principal['causa_no_conformidad']}, con {miles(int(causa_principal['ramos']))} ramos ({texto_pct(causa_principal['porcentaje'])} % de los no conformes).",
        f"El mes con mayor porcentaje fue {MESES[int(peor_mes['mes_num'])]} ({texto_pct(peor_mes['porcentaje'])} %) y el de menor fue {MESES[int(mejor_mes['mes_num'])]} ({texto_pct(mejor_mes['porcentaje'])} %).",
    ]

    resultado = {
        "titulo": "Análisis de calidad y no conformidades",
        "advertencia": "Demostración con datos ficticios. No corresponde a una empresa real.",
        "semilla": 42,
        "fuente": "Calculado por analisis_calidad.py a partir de datos_calidad.csv",
        "registros": int(len(df)),
        "kpis": {
            "ramos_revisados": total_revisados,
            "ramos_no_conformes": total_nc,
            "porcentaje_no_conformidad": pct_general,
            "inspecciones": int(len(df)),
        },
        "evolucion_semanal": [
            {
                "anio": int(fila.anio),
                "semana": int(fila.semana),
                "etiqueta": f"S{int(fila.semana):02d}",
                "clave": f"{int(fila.anio)}-S{int(fila.semana):02d}",
                "revisados": int(fila.revisados),
                "no_conformes": int(fila.no_conformes),
                "porcentaje": numero(fila.porcentaje),
            }
            for fila in semanal.itertuples(index=False)
        ],
        "por_finca": [
            {
                "finca": fila.finca,
                "revisados": int(fila.revisados),
                "no_conformes": int(fila.no_conformes),
                "porcentaje": numero(fila.porcentaje),
            }
            for fila in por_finca.itertuples(index=False)
        ],
        "por_variedad": [
            {
                "variedad": fila.variedad,
                "revisados": int(fila.revisados),
                "no_conformes": int(fila.no_conformes),
                "porcentaje": numero(fila.porcentaje),
            }
            for fila in por_variedad.itertuples(index=False)
        ],
        "causas": [
            {
                "causa": fila.causa_no_conformidad,
                "ramos": int(fila.ramos),
                "porcentaje": numero(fila.porcentaje),
            }
            for fila in causas.itertuples(index=False)
        ],
        "comparacion_mensual": [
            {
                "mes": fila.mes,
                "etiqueta": MESES[int(fila.mes_num)],
                "revisados": int(fila.revisados),
                "no_conformes": int(fila.no_conformes),
                "porcentaje": numero(fila.porcentaje),
            }
            for fila in mensual.itertuples(index=False)
        ],
        "explicacion": explicacion,
        "conclusiones": conclusiones,
        "formulas": [
            {
                "nombre": "Porcentaje de no conformidad",
                "expresion": "suma de ramos no conformes / suma de ramos revisados × 100",
            },
            {
                "nombre": "No conformidad por finca, variedad, semana o mes",
                "expresion": "la misma fórmula, calculada dentro de cada grupo",
            },
        ],
        "validacion": {
            "filas": int(len(df)),
            "filas_con_nc_mayor_que_revisados": 0,
            "valores_nulos": 0,
        },
    }

    GRAFICOS.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(semanal["semana"], semanal["porcentaje"], color="#22D3EE", linewidth=2)
    ax.set_title("No conformidad por semana")
    ax.set_xlabel("Semana ISO 2025")
    ax.set_ylabel("% no conformidad")
    fig.tight_layout()
    fig.savefig(GRAFICOS / "no_conformidad_semanal.png", dpi=120)
    plt.close(fig)

    guardar_barras(por_finca, "finca", "No conformidad por finca", "no_conformidad_finca.png")
    guardar_barras(
        por_variedad,
        "variedad",
        "No conformidad por variedad",
        "no_conformidad_variedad.png",
    )

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.barh(causas["causa_no_conformidad"], causas["ramos"], color="#3B82F6")
    ax.invert_yaxis()
    ax.set_title("Ramos no conformes por causa")
    ax.set_xlabel("Ramos")
    fig.tight_layout()
    fig.savefig(GRAFICOS / "causas.png", dpi=120)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(mensual["mes_num"].map(MESES), mensual["porcentaje"], color="#3B82F6")
    ax.set_title("No conformidad por mes")
    ax.set_ylabel("% no conformidad")
    fig.tight_layout()
    fig.savefig(GRAFICOS / "no_conformidad_mensual.png", dpi=120)
    plt.close(fig)

    texto = json.dumps(resultado, ensure_ascii=False, indent=2)
    for ruta in SALIDAS_JSON:
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(texto + "\n", encoding="utf-8")

    lineas = [
        "# Resultados del análisis de calidad",
        "",
        "Estos números los escribió `analisis_calidad.py` después de leer el CSV.",
        "Si cambias la semilla, vuelve a ejecutar el script para actualizar este archivo y el dashboard.",
        "",
        "## Indicadores",
        "",
        f"- Inspecciones: {miles(len(df))}",
        f"- Ramos revisados: {miles(total_revisados)}",
        f"- Ramos no conformes: {miles(total_nc)}",
        f"- Porcentaje de no conformidad: {texto_pct(pct_general)} %",
        "",
        "## Conclusiones",
        "",
    ]
    lineas.extend(f"- {texto_conclusion}" for texto_conclusion in conclusiones)
    lineas.extend(
        [
            "",
            "## Validación",
            "",
            "- 3000 filas.",
            "- Ningún registro tiene más ramos no conformes que revisados.",
            "- La semana y el año del archivo coinciden con la fecha ISO.",
            "",
        ]
    )
    (CARPETA / "resultados.md").write_text("\n".join(lineas), encoding="utf-8")

    print(f"Revisados: {total_revisados}")
    print(f"No conformes: {total_nc}")
    print(f"Porcentaje: {pct_general}")
    print(f"JSON: {SALIDAS_JSON[0]}")


if __name__ == "__main__":
    main()
