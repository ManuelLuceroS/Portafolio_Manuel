"""
Lee los cuatro CSV de ventas y calcula ingresos, ticket, margen y rankings.

El ingreso de una línea es cantidad x precio_unitario.
El costo de una línea es cantidad x costo del producto.
El margen bruto es ingreso menos costo.
El ticket promedio es el ingreso total dividido por el número de ventas.
Un cliente recurrente tiene 3 o más compras en el periodo.
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
    RAIZ / "public" / "datos" / "ventas.json",
    DATOS / "resumen_ventas.json",
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
    return f"{int(round(valor)):,}".replace(",", ".")


def texto_pct(valor):
    return f"{float(valor):.2f}".replace(".", ",")


def porcentaje(parte, total):
    if total == 0:
        raise SystemExit("No se puede dividir por cero.")
    return numero(parte / total * 100)


def main():
    clientes = pd.read_csv(DATOS / "clientes.csv", encoding="utf-8")
    productos = pd.read_csv(DATOS / "productos.csv", encoding="utf-8")
    ventas = pd.read_csv(DATOS / "ventas.csv", encoding="utf-8")
    detalle = pd.read_csv(DATOS / "detalle_ventas.csv", encoding="utf-8")

    if len(clientes) != 300 or len(productos) != 80 or len(ventas) != 1500:
        raise SystemExit("El tamaño de clientes, productos o ventas no es el esperado.")
    if clientes.isna().any().any() or productos.isna().any().any():
        raise SystemExit("Hay nulos en clientes o productos.")
    if ventas.isna().any().any() or detalle.isna().any().any():
        raise SystemExit("Hay nulos en ventas o detalle.")
    if not detalle["id_venta"].isin(ventas["id_venta"]).all():
        raise SystemExit("Hay líneas de detalle sin venta.")
    if not detalle["id_producto"].isin(productos["id_producto"]).all():
        raise SystemExit("Hay líneas con un producto que no existe.")
    if not ventas["id_cliente"].isin(clientes["id_cliente"]).all():
        raise SystemExit("Hay ventas con un cliente que no existe.")
    if (detalle["cantidad"] < 1).any() or (detalle["precio_unitario"] <= 0).any():
        raise SystemExit("Hay cantidades o precios inválidos.")
    if (productos["costo"] < 0).any() or (productos["costo"] >= productos["precio"]).any():
        raise SystemExit("Hay productos con costo inválido.")

    lineas_por_venta = detalle.groupby("id_venta").size()
    if lineas_por_venta.min() < 1 or lineas_por_venta.max() > 5:
        raise SystemExit("Hay ventas fuera del rango de 1 a 5 líneas.")
    if set(lineas_por_venta.index) != set(ventas["id_venta"]):
        raise SystemExit("Hay ventas sin detalle.")

    ventas["fecha_venta"] = pd.to_datetime(ventas["fecha_venta"])
    clientes["fecha_registro"] = pd.to_datetime(clientes["fecha_registro"])
    cruce_fechas = ventas.merge(clientes[["id_cliente", "fecha_registro"]], on="id_cliente")
    if (cruce_fechas["fecha_venta"] < cruce_fechas["fecha_registro"]).any():
        raise SystemExit("Hay una venta anterior al registro del cliente.")

    detalle = detalle.merge(
        productos[["id_producto", "producto", "categoria", "costo"]],
        on="id_producto",
        how="left",
    )
    if (detalle["precio_unitario"] <= detalle["costo"]).any():
        raise SystemExit("Hay precios de venta que no cubren el costo.")

    detalle["ingreso"] = detalle["cantidad"] * detalle["precio_unitario"]
    detalle["costo_total"] = detalle["cantidad"] * detalle["costo"]
    detalle["margen"] = detalle["ingreso"] - detalle["costo_total"]

    ingresos = int(detalle["ingreso"].sum())
    costo_total = int(detalle["costo_total"].sum())
    margen = int(detalle["margen"].sum())
    n_ventas = int(ventas["id_venta"].nunique())
    ticket = int(round(ingresos / n_ventas))
    margen_pct = porcentaje(margen, ingresos)

    venta_ingreso = detalle.groupby("id_venta", as_index=False).agg(ingreso=("ingreso", "sum"))
    ventas = ventas.merge(venta_ingreso, on="id_venta")
    ventas["mes_num"] = ventas["fecha_venta"].dt.month
    ventas["mes"] = ventas["fecha_venta"].dt.strftime("%Y-%m")

    mensual = (
        ventas.groupby(["mes", "mes_num"], as_index=False)
        .agg(ingresos=("ingreso", "sum"), ventas=("id_venta", "nunique"))
        .sort_values("mes")
    )
    mensual["ticket_promedio"] = (mensual["ingresos"] / mensual["ventas"]).round().astype(int)
    mensual["ingresos_acumulados"] = mensual["ingresos"].cumsum()

    productos_rank = (
        detalle.groupby(["producto", "categoria"], as_index=False)
        .agg(cantidad=("cantidad", "sum"), ingresos=("ingreso", "sum"))
        .sort_values(["cantidad", "ingresos"], ascending=False)
    )
    top_cantidad = productos_rank.head(10)
    top_ingreso = productos_rank.sort_values("ingresos", ascending=False).iloc[0]

    categorias = (
        detalle.groupby("categoria", as_index=False)
        .agg(ingresos=("ingreso", "sum"), margen=("margen", "sum"), cantidad=("cantidad", "sum"))
        .sort_values("ingresos", ascending=False)
    )
    categorias["porcentaje_ingresos"] = [
        porcentaje(valor, ingresos) for valor in categorias["ingresos"]
    ]
    categorias["margen_porcentaje"] = [
        porcentaje(fila.margen, fila.ingresos) for fila in categorias.itertuples(index=False)
    ]

    compras = (
        ventas.groupby("id_cliente", as_index=False)
        .agg(compras=("id_venta", "nunique"), ingresos=("ingreso", "sum"))
        .merge(clientes[["id_cliente", "nombre", "ciudad"]], on="id_cliente")
    )
    clientes_con_compra = int(compras["id_cliente"].nunique())
    recurrentes = compras[compras["compras"] >= 3]
    n_recurrentes = int(len(recurrentes))
    top_clientes = compras.sort_values(["ingresos", "compras"], ascending=False).head(8)

    mejor_mes = mensual.sort_values("ingresos", ascending=False).iloc[0]
    categoria_top = categorias.iloc[0]
    categoria_margen = categorias.sort_values("margen_porcentaje", ascending=False).iloc[0]
    producto_top = top_cantidad.iloc[0]

    explicacion = (
        f"Los ingresos se calcularon línea por línea, multiplicando cantidad por precio unitario. "
        f"La suma del periodo es {miles(ingresos)} COP en {miles(n_ventas)} ventas. "
        f"El ticket promedio es {miles(ticket)} COP. "
        f"El margen bruto estimado es {miles(margen)} COP ({texto_pct(margen_pct)} %). "
        f"De {len(clientes)} clientes del maestro, {clientes_con_compra} compraron al menos una vez "
        f"y {n_recurrentes} tuvieron 3 o más compras."
    )

    conclusiones = [
        f"Los ingresos del periodo suman {miles(ingresos)} COP, con un ticket promedio de {miles(ticket)} COP.",
        f"El margen bruto estimado es {texto_pct(margen_pct)} % ({miles(margen)} COP).",
        f"El producto con más unidades fue {producto_top['producto']} ({miles(int(producto_top['cantidad']))} unidades).",
        f"El producto con más ingresos fue {top_ingreso['producto']} ({miles(int(top_ingreso['ingresos']))} COP).",
        f"La categoría con más ingresos fue {categoria_top['categoria']} ({texto_pct(categoria_top['porcentaje_ingresos'])} % de los ingresos).",
        f"La categoría con mayor margen porcentual fue {categoria_margen['categoria']} ({texto_pct(categoria_margen['margen_porcentaje'])} %).",
        f"El mes de mayores ingresos fue {MESES[int(mejor_mes['mes_num'])]} ({miles(int(mejor_mes['ingresos']))} COP).",
        f"{n_recurrentes} clientes compraron 3 veces o más. Son el {texto_pct(porcentaje(n_recurrentes, clientes_con_compra))} % de quienes tuvieron al menos una compra.",
    ]

    resultado = {
        "titulo": "Análisis de ventas y clientes",
        "advertencia": "Demostración con datos ficticios. No corresponde a una tienda real.",
        "semilla": 7,
        "fuente": "Calculado por analisis_ventas.py a partir de los CSV de ventas",
        "kpis": {
            "ingresos": ingresos,
            "ventas": n_ventas,
            "ticket_promedio": ticket,
            "margen_bruto": margen,
            "margen_porcentaje": margen_pct,
            "costo_total": costo_total,
            "clientes_maestro": int(len(clientes)),
            "clientes_con_compra": clientes_con_compra,
            "clientes_recurrentes": n_recurrentes,
        },
        "mensual": [
            {
                "mes": fila.mes,
                "etiqueta": MESES[int(fila.mes_num)],
                "ingresos": int(fila.ingresos),
                "ventas": int(fila.ventas),
                "ticket_promedio": int(fila.ticket_promedio),
                "ingresos_acumulados": int(fila.ingresos_acumulados),
            }
            for fila in mensual.itertuples(index=False)
        ],
        "top_productos": [
            {
                "producto": fila.producto,
                "categoria": fila.categoria,
                "cantidad": int(fila.cantidad),
                "ingresos": int(fila.ingresos),
            }
            for fila in top_cantidad.itertuples(index=False)
        ],
        "por_categoria": [
            {
                "categoria": fila.categoria,
                "ingresos": int(fila.ingresos),
                "margen": int(fila.margen),
                "cantidad": int(fila.cantidad),
                "porcentaje_ingresos": numero(fila.porcentaje_ingresos),
                "margen_porcentaje": numero(fila.margen_porcentaje),
            }
            for fila in categorias.itertuples(index=False)
        ],
        "top_clientes": [
            {
                "nombre": fila.nombre,
                "ciudad": fila.ciudad,
                "compras": int(fila.compras),
                "ingresos": int(fila.ingresos),
            }
            for fila in top_clientes.itertuples(index=False)
        ],
        "definicion_recurrente": "Cliente con 3 o más compras en el periodo.",
        "explicacion": explicacion,
        "conclusiones": conclusiones,
        "formulas": [
            {"nombre": "Ingreso de la línea", "expresion": "cantidad × precio_unitario"},
            {"nombre": "Costo de la línea", "expresion": "cantidad × costo del producto"},
            {"nombre": "Margen bruto", "expresion": "ingresos − costo"},
            {"nombre": "Margen porcentual", "expresion": "margen bruto / ingresos × 100"},
            {"nombre": "Ticket promedio", "expresion": "ingresos / número de ventas"},
            {"nombre": "Cliente recurrente", "expresion": "cliente con 3 o más ventas"},
        ],
        "validacion": {
            "clientes": int(len(clientes)),
            "productos": int(len(productos)),
            "ventas": n_ventas,
            "lineas": int(len(detalle)),
            "ventas_sin_detalle": 0,
            "precios_bajo_costo": 0,
        },
    }

    GRAFICOS.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(mensual["mes_num"].map(MESES), mensual["ingresos"] / 1_000_000, color="#3B82F6")
    ax.set_title("Ingresos mensuales")
    ax.set_ylabel("Millones de COP")
    fig.tight_layout()
    fig.savefig(GRAFICOS / "ventas_mensuales.png", dpi=120)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    grafico = top_cantidad.sort_values("cantidad")
    ax.barh(grafico["producto"], grafico["cantidad"], color="#3B82F6")
    ax.set_title("Top 10 productos por unidades")
    ax.set_xlabel("Unidades")
    fig.tight_layout()
    fig.savefig(GRAFICOS / "top_productos.png", dpi=120)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(categorias["categoria"], categorias["ingresos"] / 1_000_000, color="#22D3EE")
    ax.set_title("Ingresos por categoría")
    ax.set_ylabel("Millones de COP")
    ax.tick_params(axis="x", rotation=15)
    fig.tight_layout()
    fig.savefig(GRAFICOS / "ventas_categoria.png", dpi=120)
    plt.close(fig)

    texto = json.dumps(resultado, ensure_ascii=False, indent=2)
    for ruta in SALIDAS_JSON:
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(texto + "\n", encoding="utf-8")

    lineas = [
        "# Resultados del análisis de ventas",
        "",
        "Estos números los escribió `analisis_ventas.py` después de leer los CSV.",
        "",
        "## Indicadores",
        "",
        f"- Ingresos: {miles(ingresos)} COP",
        f"- Ventas: {miles(n_ventas)}",
        f"- Ticket promedio: {miles(ticket)} COP",
        f"- Margen bruto: {miles(margen)} COP ({texto_pct(margen_pct)} %)",
        f"- Clientes del maestro: {len(clientes)}",
        f"- Clientes con al menos una compra: {clientes_con_compra}",
        f"- Clientes recurrentes (3 o más compras): {n_recurrentes}",
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
            "- Todas las ventas tienen entre 1 y 5 líneas.",
            "- Cada línea apunta a una venta y a un producto existentes.",
            "- Ninguna venta es anterior a la fecha de registro del cliente.",
            "- Ningún precio unitario quedó por debajo del costo.",
            "",
        ]
    )
    (CARPETA / "resultados.md").write_text("\n".join(lineas), encoding="utf-8")

    print(f"Ingresos: {ingresos}")
    print(f"Ticket: {ticket}")
    print(f"Margen %: {margen_pct}")
    print(f"Recurrentes: {n_recurrentes} de {clientes_con_compra}")
    print(f"JSON: {SALIDAS_JSON[0]}")


if __name__ == "__main__":
    main()
