"""
Lee datos_operativos.csv y calcula cumplimiento, productividad y tendencias.

Definiciones:
- Cumplimiento de una fila = resultado / meta × 100. La meta siempre es mayor que cero.
- Cumplimiento promedio = media de los cumplimientos de cada fila.
- Cumplimiento de un área = suma de resultados / suma de metas × 100.
  Dentro de cada área la unidad es la misma, así que esa suma sí se puede hacer.
- Productividad del área = suma de resultados / suma de horas.
  No se compara entre áreas porque la unidad cambia.
- La semana se toma del calendario ISO, junto con el año ISO, para no mezclar
  la semana 1 de un año con la de otro.

Estado, la misma regla del generador:
- Cumplida: resultado >= meta
- Parcial: resultado / meta >= 80 %, comparado con enteros
- No cumplida: el resto
"""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

CARPETA = Path(__file__).resolve().parents[1]
RAIZ = Path(__file__).resolve().parents[3]
DATOS = CARPETA / "datos"
GRAFICOS = CARPETA / "graficos"
SALIDAS_JSON = [
    RAIZ / "public" / "datos" / "operaciones.json",
    DATOS / "resumen_operaciones.json",
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

ORDEN_ESTADO = ["Cumplida", "Parcial", "No cumplida"]


def numero(valor, decimales=2):
    return float(f"{float(valor):.{decimales}f}")


def miles(valor):
    return f"{int(round(valor)):,}".replace(",", ".")


def texto_pct(valor):
    return f"{float(valor):.2f}".replace(".", ",")


def texto_decimal(valor):
    return f"{float(valor):.2f}".replace(".", ",")


def porcentaje(parte, total):
    if total == 0:
        raise SystemExit("No se puede dividir por cero.")
    return numero(parte / total * 100)


def estado_esperado(resultado, meta):
    if resultado >= meta:
        return "Cumplida"
    if resultado * 5 >= meta * 4:
        return "Parcial"
    return "No cumplida"


def main():
    df = pd.read_csv(DATOS / "datos_operativos.csv", encoding="utf-8")
    catalogo = pd.read_csv(DATOS / "catalogo_actividades.csv", encoding="utf-8")
    df["fecha"] = pd.to_datetime(df["fecha"])

    columnas = [
        "id_registro",
        "fecha",
        "area",
        "responsable",
        "actividad",
        "meta",
        "resultado",
        "horas_trabajadas",
        "estado",
    ]
    if list(df.columns) != columnas:
        raise SystemExit("Las columnas de datos_operativos.csv no coinciden.")
    if len(df) != 1500:
        raise SystemExit(f"Se esperaban 1500 filas y hay {len(df)}.")
    if df.isna().any().any():
        raise SystemExit("Hay valores nulos.")
    if (df["meta"] <= 0).any() or (df["horas_trabajadas"] <= 0).any():
        raise SystemExit("Hay metas u horas en cero.")
    if (df["resultado"] < 0).any():
        raise SystemExit("Hay resultados negativos.")

    esperado = [
        estado_esperado(int(resultado), int(meta))
        for resultado, meta in zip(df["resultado"], df["meta"])
    ]
    if esperado != df["estado"].tolist():
        raise SystemExit("Hay estados que no coinciden con la regla de cumplimiento.")

    df = df.merge(catalogo, on=["actividad", "area"], how="left")
    if df["unidad"].isna().any():
        raise SystemExit("Hay actividades sin unidad en el catálogo.")
    if (df.groupby("area")["unidad"].nunique() != 1).any():
        raise SystemExit("Hay un área con más de una unidad de medida.")

    df["cumplimiento"] = df["resultado"] / df["meta"] * 100
    iso = df["fecha"].dt.isocalendar()
    df["anio"] = iso.year.astype(int)
    df["semana"] = iso.week.astype(int)
    df["mes_num"] = df["fecha"].dt.month
    df["mes"] = df["fecha"].dt.strftime("%Y-%m")

    cumplimiento_promedio = numero(df["cumplimiento"].mean())
    cumplidas = int((df["estado"] == "Cumplida").sum())
    horas = int(df["horas_trabajadas"].sum())
    pct_cumplidas = porcentaje(cumplidas, len(df))

    por_area = (
        df.groupby(["area", "unidad"], as_index=False)
        .agg(
            actividades=("id_registro", "count"),
            meta=("meta", "sum"),
            resultado=("resultado", "sum"),
            horas=("horas_trabajadas", "sum"),
        )
        .sort_values("area")
    )
    por_area["cumplimiento"] = [
        porcentaje(resultado, meta)
        for resultado, meta in zip(por_area["resultado"], por_area["meta"])
    ]
    por_area["productividad"] = [
        numero(resultado / horas_area)
        for resultado, horas_area in zip(por_area["resultado"], por_area["horas"])
    ]
    por_area = por_area.sort_values("cumplimiento", ascending=False)

    semanal = (
        df.groupby(["anio", "semana"], as_index=False)
        .agg(cumplimiento=("cumplimiento", "mean"), actividades=("id_registro", "count"))
        .sort_values(["anio", "semana"])
    )
    semanal["cumplimiento"] = semanal["cumplimiento"].map(lambda valor: numero(valor))

    mensual = (
        df.groupby(["mes", "mes_num"], as_index=False)
        .agg(cumplimiento=("cumplimiento", "mean"), actividades=("id_registro", "count"))
        .sort_values("mes")
    )
    mensual["cumplimiento"] = mensual["cumplimiento"].map(lambda valor: numero(valor))

    conteo = df["estado"].value_counts().to_dict()
    por_estado = []
    for estado in ORDEN_ESTADO:
        actividades = int(conteo.get(estado, 0))
        por_estado.append(
            {
                "estado": estado,
                "actividades": actividades,
                "porcentaje": porcentaje(actividades, len(df)),
            }
        )

    area_alta = por_area.iloc[0]
    area_baja = por_area.iloc[-1]
    mes_alto = mensual.sort_values("cumplimiento", ascending=False).iloc[0]
    mes_bajo = mensual.sort_values("cumplimiento", ascending=True).iloc[0]

    explicacion = (
        f"El cumplimiento promedio es la media de resultado / meta de cada actividad: "
        f"{texto_pct(cumplimiento_promedio)} %. "
        f"Ese número no es igual al porcentaje de actividades en estado Cumplida "
        f"({texto_pct(pct_cumplidas)} %), porque una actividad puede quedar cerca de la meta "
        f"y aun así no alcanzarla. "
        f"Por área se usa la suma de resultados sobre la suma de metas. "
        f"{area_alta['area']} quedó con el cumplimiento más alto "
        f"({texto_pct(area_alta['cumplimiento'])} %) y {area_baja['area']} con el más bajo "
        f"({texto_pct(area_baja['cumplimiento'])} %)."
    )

    conclusiones = [
        f"Se registraron {miles(len(df))} actividades. El cumplimiento promedio fue {texto_pct(cumplimiento_promedio)} %.",
        f"{miles(cumplidas)} actividades alcanzaron o superaron la meta ({texto_pct(pct_cumplidas)} %).",
        f"El área con mayor cumplimiento fue {area_alta['area']} ({texto_pct(area_alta['cumplimiento'])} %) y la de menor fue {area_baja['area']} ({texto_pct(area_baja['cumplimiento'])} %).",
        f"En {area_baja['area']} la productividad fue {texto_decimal(area_baja['productividad'])} {area_baja['unidad']} por hora. Esa cifra no se compara con otras áreas porque la unidad es distinta.",
        f"El mes con mayor cumplimiento promedio fue {MESES[int(mes_alto['mes_num'])]} ({texto_pct(mes_alto['cumplimiento'])} %) y el de menor fue {MESES[int(mes_bajo['mes_num'])]} ({texto_pct(mes_bajo['cumplimiento'])} %).",
        f"Las horas registradas suman {miles(horas)}.",
    ]

    resultado = {
        "titulo": "Análisis de indicadores operativos",
        "advertencia": "Demostración con datos ficticios. No corresponde a una operación real.",
        "semilla": 21,
        "fuente": "Calculado por analisis_operativo.py a partir de datos_operativos.csv",
        "kpis": {
            "actividades": int(len(df)),
            "cumplimiento_promedio": cumplimiento_promedio,
            "actividades_cumplidas": cumplidas,
            "porcentaje_cumplidas": pct_cumplidas,
            "horas_trabajadas": horas,
        },
        "por_area": [
            {
                "area": fila.area,
                "unidad": fila.unidad,
                "actividades": int(fila.actividades),
                "meta": int(fila.meta),
                "resultado": int(fila.resultado),
                "horas": int(fila.horas),
                "cumplimiento": numero(fila.cumplimiento),
                "productividad": numero(fila.productividad),
            }
            for fila in por_area.itertuples(index=False)
        ],
        "evolucion_semanal": [
            {
                "anio": int(fila.anio),
                "semana": int(fila.semana),
                "etiqueta": f"S{int(fila.semana):02d}",
                "clave": f"{int(fila.anio)}-S{int(fila.semana):02d}",
                "cumplimiento": numero(fila.cumplimiento),
                "actividades": int(fila.actividades),
            }
            for fila in semanal.itertuples(index=False)
        ],
        "comparacion_mensual": [
            {
                "mes": fila.mes,
                "etiqueta": MESES[int(fila.mes_num)],
                "cumplimiento": numero(fila.cumplimiento),
                "actividades": int(fila.actividades),
            }
            for fila in mensual.itertuples(index=False)
        ],
        "por_estado": por_estado,
        "nota_productividad": "La productividad se calcula dentro de cada área porque la unidad de medida cambia. No se debe comparar, por ejemplo, ramos por hora con órdenes por hora.",
        "explicacion": explicacion,
        "conclusiones": conclusiones,
        "formulas": [
            {
                "nombre": "Cumplimiento de la actividad",
                "expresion": "resultado / meta × 100, con meta mayor que cero",
            },
            {
                "nombre": "Cumplimiento promedio",
                "expresion": "promedio del cumplimiento de cada actividad",
            },
            {
                "nombre": "Cumplimiento del área",
                "expresion": "suma de resultados / suma de metas × 100",
            },
            {
                "nombre": "Productividad del área",
                "expresion": "suma de resultados / suma de horas trabajadas",
            },
            {
                "nombre": "Estado Cumplida",
                "expresion": "resultado mayor o igual que la meta",
            },
            {
                "nombre": "Estado Parcial",
                "expresion": "resultado de al menos el 80 % de la meta, sin llegar a 100 %",
            },
            {
                "nombre": "Semana",
                "expresion": "año ISO y semana ISO de la fecha",
            },
        ],
        "validacion": {
            "filas": int(len(df)),
            "metas_en_cero": 0,
            "horas_en_cero": 0,
            "estados_inconsistentes": 0,
        },
    }

    GRAFICOS.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(por_area["area"], por_area["cumplimiento"], color="#3B82F6")
    ax.set_title("Cumplimiento por área")
    ax.set_ylabel("% cumplimiento")
    ax.tick_params(axis="x", rotation=15)
    fig.tight_layout()
    fig.savefig(GRAFICOS / "cumplimiento_area.png", dpi=120)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(range(len(semanal)), semanal["cumplimiento"], color="#22D3EE", linewidth=2)
    ax.set_title("Cumplimiento promedio por semana ISO")
    ax.set_ylabel("% cumplimiento")
    ax.set_xlabel("Orden de las semanas del periodo")
    fig.tight_layout()
    fig.savefig(GRAFICOS / "cumplimiento_semanal.png", dpi=120)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(mensual["mes_num"].map(MESES), mensual["cumplimiento"], color="#3B82F6")
    ax.set_title("Cumplimiento promedio por mes")
    ax.set_ylabel("% cumplimiento")
    fig.tight_layout()
    fig.savefig(GRAFICOS / "cumplimiento_mensual.png", dpi=120)
    plt.close(fig)

    texto = json.dumps(resultado, ensure_ascii=False, indent=2)
    for ruta in SALIDAS_JSON:
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(texto + "\n", encoding="utf-8")

    lineas = [
        "# Resultados del análisis operativo",
        "",
        "Estos números los escribió `analisis_operativo.py` después de leer el CSV.",
        "",
        "## Indicadores",
        "",
        f"- Actividades: {miles(len(df))}",
        f"- Cumplimiento promedio: {texto_pct(cumplimiento_promedio)} %",
        f"- Actividades cumplidas: {miles(cumplidas)} ({texto_pct(pct_cumplidas)} %)",
        f"- Horas trabajadas: {miles(horas)}",
        "",
        "## Por área",
        "",
        "| Área | Unidad | Cumplimiento | Productividad |",
        "| --- | --- | ---: | ---: |",
    ]
    for fila in por_area.itertuples(index=False):
        lineas.append(
            f"| {fila.area} | {fila.unidad} | {texto_pct(fila.cumplimiento)} % | {texto_decimal(fila.productividad)} |"
        )
    lineas.extend(["", "## Conclusiones", ""])
    lineas.extend(f"- {texto_conclusion}" for texto_conclusion in conclusiones)
    lineas.extend(
        [
            "",
            "## Validación",
            "",
            "- 1500 filas, sin metas ni horas en cero.",
            "- El estado de cada fila coincide con la regla de 80 % y 100 %.",
            "- Cada área tiene una sola unidad de medida.",
            "",
        ]
    )
    (CARPETA / "resultados.md").write_text("\n".join(lineas), encoding="utf-8")

    print(f"Cumplimiento promedio: {cumplimiento_promedio}")
    print(f"Cumplidas: {cumplidas}")
    print(por_area[["area", "cumplimiento", "productividad"]].to_string(index=False))
    print(f"JSON: {SALIDAS_JSON[0]}")


if __name__ == "__main__":
    main()
