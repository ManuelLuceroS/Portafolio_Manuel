"""
Genera clientes, productos, ventas y detalle de una tienda ficticia.

Semilla: 7.

Volumen pedido: 300 clientes, 80 productos, 1500 ventas
y entre 1 y 5 líneas por venta.

Supuestos:
- Los precios del detalle salen del catálogo. Un 8 % de las líneas tiene
  10 % de descuento, siempre que el precio siga por encima del costo.
- El ingreso no se guarda en las ventas: se calcula con cantidad x precio.
- Un cliente solo puede comprar desde su fecha de registro.
- Las ventas son de 2025, de lunes a sábado, con más movimiento en noviembre
  y diciembre.
"""

from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

SEMILLA = 7
rng = np.random.default_rng(SEMILLA)

CARPETA = Path(__file__).resolve().parents[1]
RUTA_DATOS = CARPETA / "datos"

NOMBRES = [
    "Laura", "Andrés", "Camila", "Juan", "Valentina", "Santiago", "Mariana",
    "Daniel", "Sofía", "Mateo", "Isabella", "Nicolás", "Gabriela", "Felipe",
    "Natalia", "Alejandro", "Paula", "Sebastián", "Daniela", "David",
    "Catalina", "Julián", "Lucía", "Miguel", "Sara", "Tomás", "Elena",
    "Samuel", "Martina", "Emilio",
]

APELLIDOS = [
    "Gómez", "Rodríguez", "López", "Martínez", "García", "Hernández", "Díaz",
    "Torres", "Ramírez", "Flores", "Rivera", "Morales", "Ortiz", "Castillo",
    "Vargas", "Rojas", "Jiménez", "Herrera", "Castro", "Mendoza", "Guerrero",
    "Romero", "Suárez", "Arias", "Pardo", "León", "Cruz", "Vega", "Rincón",
    "Navarro",
]

CIUDADES = ["Bogotá", "Medellín", "Cali", "Barranquilla", "Bucaramanga", "Pereira", "Manizales"]
PESO_CIUDAD = np.array([0.34, 0.18, 0.14, 0.10, 0.09, 0.08, 0.07], dtype=float)

# nombre, categoría, presentaciones (etiqueta, precio, participación del costo)
CATALOGO = [
    ("Arroz", "Alimentos", [("500 g", 2800, 0.70), ("1000 g", 5100, 0.69), ("2500 g", 11200, 0.68)]),
    ("Frijol", "Alimentos", [("500 g", 4200, 0.71), ("1000 g", 7600, 0.70), ("2500 g", 16800, 0.69)]),
    ("Azúcar", "Alimentos", [("500 g", 2600, 0.72), ("1000 g", 4700, 0.71), ("2500 g", 10500, 0.70)]),
    ("Aceite", "Alimentos", [("500 ml", 8900, 0.74), ("1000 ml", 15200, 0.73), ("3000 ml", 39800, 0.72)]),
    ("Pasta", "Alimentos", [("250 g", 2200, 0.66), ("500 g", 3900, 0.66), ("1000 g", 7100, 0.65)]),
    ("Café", "Alimentos", [("125 g", 6800, 0.64), ("250 g", 11900, 0.63), ("500 g", 21400, 0.62)]),
    ("Lenteja", "Alimentos", [("500 g", 3600, 0.70), ("1000 g", 6500, 0.69)]),
    ("Avena", "Alimentos", [("250 g", 3100, 0.67), ("500 g", 5400, 0.66), ("1000 g", 9800, 0.65)]),
    ("Harina de trigo", "Alimentos", [("500 g", 2400, 0.71), ("1000 g", 4300, 0.70)]),
    ("Atún", "Alimentos", [("170 g", 5900, 0.68), ("3 unidades", 16500, 0.67)]),
    ("Agua", "Bebidas", [("600 ml", 1800, 0.60), ("1500 ml", 2900, 0.58)]),
    ("Gaseosa", "Bebidas", [("400 ml", 2500, 0.62), ("1500 ml", 5200, 0.60)]),
    ("Jugo", "Bebidas", [("250 ml", 2700, 0.61), ("1000 ml", 6900, 0.60)]),
    ("Té", "Bebidas", [("20 sobres", 7400, 0.58), ("50 sobres", 14900, 0.57)]),
    ("Malta", "Bebidas", [("330 ml", 2800, 0.63), ("6 unidades", 14900, 0.62)]),
    ("Leche", "Bebidas", [("1000 ml", 4600, 0.72), ("6 unidades", 25200, 0.71)]),
    ("Jabón en barra", "Aseo", [("3 unidades", 6200, 0.58), ("6 unidades", 10900, 0.57)]),
    ("Detergente", "Aseo", [("500 g", 7800, 0.60), ("2000 g", 21400, 0.58)]),
    ("Blanqueador", "Aseo", [("1000 ml", 4200, 0.57), ("2000 ml", 7300, 0.56)]),
    ("Lavaloza", "Aseo", [("500 ml", 5600, 0.59), ("1000 ml", 9800, 0.58)]),
    ("Papel higiénico", "Aseo", [("4 rollos", 8900, 0.61), ("12 rollos", 22900, 0.60)]),
    ("Limpiavidrios", "Aseo", [("500 ml", 6400, 0.57), ("1000 ml", 10900, 0.56)]),
    ("Champú", "Cuidado personal", [("200 ml", 9800, 0.55), ("400 ml", 16200, 0.54)]),
    ("Crema dental", "Cuidado personal", [("75 ml", 5400, 0.56), ("3 unidades", 13900, 0.55)]),
    ("Desodorante", "Cuidado personal", [("50 g", 8900, 0.54), ("2 unidades", 15900, 0.53)]),
    ("Jabón tocador", "Cuidado personal", [("3 unidades", 7200, 0.58), ("6 unidades", 12800, 0.57)]),
    ("Toallas húmedas", "Cuidado personal", [("50 unidades", 6900, 0.56), ("100 unidades", 11900, 0.55)]),
    ("Crema corporal", "Cuidado personal", [("200 ml", 12400, 0.52), ("400 ml", 19800, 0.51)]),
    ("Bombillo LED", "Hogar", [("9 W", 8900, 0.60), ("12 W", 11200, 0.59)]),
    ("Pila AA", "Hogar", [("2 unidades", 5400, 0.62), ("8 unidades", 16900, 0.61)]),
    ("Escoba", "Hogar", [("unidad", 12900, 0.60)]),
    ("Trapero", "Hogar", [("unidad", 15600, 0.61)]),
    ("Bolsa de basura", "Hogar", [("10 unidades", 4800, 0.63), ("30 unidades", 11200, 0.62)]),
    ("Servilleta", "Hogar", [("100 unidades", 3900, 0.64), ("300 unidades", 8900, 0.63)]),
    ("Vela", "Hogar", [("4 unidades", 6200, 0.58), ("12 unidades", 14900, 0.57)]),
    ("Encendedor", "Hogar", [("unidad", 2500, 0.55)]),
    ("Ambientador", "Hogar", [("unidad", 7800, 0.57), ("3 unidades", 19800, 0.56)]),
    ("Cinta adhesiva", "Hogar", [("unidad", 4300, 0.60)]),
    ("Fósforos", "Hogar", [("10 cajas", 3600, 0.62)]),
]

PESO_CATEGORIA = {
    "Alimentos": 3.2,
    "Bebidas": 2.4,
    "Aseo": 1.6,
    "Cuidado personal": 1.3,
    "Hogar": 1.0,
}

FACTOR_MES = {
    1: 0.90,
    2: 0.86,
    3: 0.94,
    4: 1.00,
    5: 1.05,
    6: 1.00,
    7: 0.96,
    8: 1.00,
    9: 1.04,
    10: 1.10,
    11: 1.28,
    12: 1.46,
}


def fecha_aleatoria(inicio, fin):
    dias = (fin - inicio).days
    return inicio + timedelta(days=int(rng.integers(0, dias + 1)))


def crear_clientes():
    combos = [f"{nombre} {apellido}" for nombre in NOMBRES for apellido in APELLIDOS]
    rng.shuffle(combos)
    elegidos = combos[:300]

    pesos = np.ones(300, dtype=float)
    pesos[:45] = 8
    pesos[45:130] = 3
    rng.shuffle(pesos)

    filas = []
    for i, nombre in enumerate(elegidos, start=1):
        if rng.random() < 0.7:
            registro = fecha_aleatoria(datetime(2023, 3, 1), datetime(2024, 12, 31))
        else:
            registro = fecha_aleatoria(datetime(2025, 1, 6), datetime(2025, 9, 30))
        ciudad = CIUDADES[int(rng.choice(len(CIUDADES), p=PESO_CIUDAD))]
        filas.append(
            {
                "id_cliente": i,
                "nombre": nombre,
                "ciudad": ciudad,
                "fecha_registro": registro,
                "peso": float(pesos[i - 1]),
            }
        )
    return filas


def crear_productos():
    filas = []
    for nombre, categoria, presentaciones in CATALOGO:
        for etiqueta, precio, ratio in presentaciones:
            costo = int(round(precio * ratio))
            if costo >= precio:
                costo = precio - 1
            peso = PESO_CATEGORIA[categoria]
            if precio < 5000:
                peso *= 1.35
            elif precio > 30000:
                peso *= 0.75
            filas.append(
                {
                    "producto": f"{nombre} {etiqueta}",
                    "categoria": categoria,
                    "precio": int(precio),
                    "costo": costo,
                    "peso": peso,
                }
            )

    if len(filas) != 80:
        raise SystemExit(f"Se esperaban 80 productos y hay {len(filas)}.")

    for i, fila in enumerate(filas, start=1):
        fila["id_producto"] = i
    return filas


def dias_venta():
    dias = []
    actual = datetime(2025, 1, 2)
    fin = datetime(2025, 12, 30)
    while actual <= fin:
        if actual.weekday() < 6:
            dias.append(actual)
        actual += timedelta(days=1)
    return dias


def elegir_fechas(dias):
    pesos = []
    for dia in dias:
        peso = FACTOR_MES[dia.month]
        if dia.weekday() == 5:
            peso *= 1.12
        pesos.append(peso)
    valores = np.array(pesos, dtype=float)
    valores = valores / valores.sum()
    indices = rng.choice(len(dias), size=1500, replace=True, p=valores)
    return [dias[int(i)] for i in indices]


def elegir_cliente(fecha, clientes):
    elegibles = [c for c in clientes if c["fecha_registro"] <= fecha]
    if not elegibles:
        raise SystemExit(f"No hay clientes registrados al {fecha:%Y-%m-%d}.")
    pesos = np.array([c["peso"] for c in elegibles], dtype=float)
    pesos = pesos / pesos.sum()
    indice = int(rng.choice(len(elegibles), p=pesos))
    return elegibles[indice]


def cantidad_para(precio):
    if precio >= 40000:
        return int(rng.integers(1, 3))
    if precio >= 15000:
        return int(rng.integers(1, 5))
    return int(rng.integers(1, 7))


def main():
    clientes = crear_clientes()
    productos = crear_productos()
    pesos_producto = np.array([p["peso"] for p in productos], dtype=float)
    pesos_producto = pesos_producto / pesos_producto.sum()

    fechas = sorted(elegir_fechas(dias_venta()))
    ventas = []
    detalle = []
    id_detalle = 1

    for id_venta, fecha in enumerate(fechas, start=1):
        cliente = elegir_cliente(fecha, clientes)
        ventas.append(
            {
                "id_venta": id_venta,
                "id_cliente": cliente["id_cliente"],
                "fecha_venta": fecha.strftime("%Y-%m-%d"),
            }
        )

        n_items = int(rng.integers(1, 6))
        indices = rng.choice(len(productos), size=n_items, replace=False, p=pesos_producto)
        for indice in indices:
            producto = productos[int(indice)]
            precio = producto["precio"]
            costo = producto["costo"]
            precio_unitario = precio
            if rng.random() < 0.08:
                con_descuento = int(round(precio * 0.9))
                if con_descuento > costo:
                    precio_unitario = con_descuento

            detalle.append(
                {
                    "id_detalle": id_detalle,
                    "id_venta": id_venta,
                    "id_producto": producto["id_producto"],
                    "cantidad": cantidad_para(precio),
                    "precio_unitario": precio_unitario,
                }
            )
            id_detalle += 1

    df_clientes = pd.DataFrame(clientes).drop(columns=["peso"])
    df_clientes["fecha_registro"] = pd.to_datetime(df_clientes["fecha_registro"]).dt.strftime("%Y-%m-%d")
    df_productos = pd.DataFrame(productos)[
        ["id_producto", "producto", "categoria", "precio", "costo"]
    ]
    df_ventas = pd.DataFrame(ventas)
    df_detalle = pd.DataFrame(detalle)

    if not df_ventas["id_cliente"].isin(df_clientes["id_cliente"]).all():
        raise SystemExit("Hay ventas con un cliente que no existe.")
    if not df_detalle["id_venta"].isin(df_ventas["id_venta"]).all():
        raise SystemExit("Hay detalle sin venta.")
    if not df_detalle["id_producto"].isin(df_productos["id_producto"]).all():
        raise SystemExit("Hay detalle sin producto.")
    if (df_detalle["cantidad"] < 1).any():
        raise SystemExit("Hay cantidades menores que 1.")
    if df_detalle.groupby("id_venta").size().max() > 5:
        raise SystemExit("Hay una venta con más de 5 líneas.")
    if df_detalle.groupby("id_venta").size().min() < 1:
        raise SystemExit("Hay una venta sin detalle.")

    cruce = df_detalle.merge(df_productos, on="id_producto")
    if (cruce["precio_unitario"] <= cruce["costo"]).any():
        raise SystemExit("Hay un precio de venta menor o igual al costo.")

    RUTA_DATOS.mkdir(parents=True, exist_ok=True)
    df_clientes.to_csv(RUTA_DATOS / "clientes.csv", index=False, encoding="utf-8")
    df_productos.to_csv(RUTA_DATOS / "productos.csv", index=False, encoding="utf-8")
    df_ventas.to_csv(RUTA_DATOS / "ventas.csv", index=False, encoding="utf-8")
    df_detalle.to_csv(RUTA_DATOS / "detalle_ventas.csv", index=False, encoding="utf-8")

    print(f"Clientes: {len(df_clientes)}")
    print(f"Productos: {len(df_productos)}")
    print(f"Ventas: {len(df_ventas)}")
    print(f"Detalle: {len(df_detalle)}")
    print(f"Carpeta: {RUTA_DATOS}")


if __name__ == "__main__":
    main()
