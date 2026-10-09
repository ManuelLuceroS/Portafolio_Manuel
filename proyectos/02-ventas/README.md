# Análisis de ventas y clientes

Demostración con datos ficticios de una tienda. No corresponde a ventas reales.

## Problema de negocio

La tienda necesita ver qué productos salen más, qué categorías dejan más margen, cómo se mueven los ingresos en el año y qué clientes compran seguido.

## Objetivo

Calcular ingresos, ticket promedio, margen bruto, ranking de productos y clientes recurrentes a partir del detalle de cada venta.

## Dataset

Generado con la semilla 7, en `scripts/generar_datos.py`.

| Archivo | Filas | Contenido |
| --- | ---: | --- |
| clientes.csv | 300 | id_cliente, nombre, ciudad, fecha_registro |
| productos.csv | 80 | id_producto, producto, categoria, precio, costo |
| ventas.csv | 1.500 | id_venta, id_cliente, fecha_venta |
| detalle_ventas.csv | 4.437 | id_detalle, id_venta, id_producto, cantidad, precio_unitario |

Las ventas son de 2025, de lunes a sábado. Noviembre y diciembre tienen más peso. Un cliente solo puede comprar desde su fecha de registro. Cada venta tiene entre 1 y 5 productos. El precio de la línea es el del catálogo; cerca del 8 % de las líneas tiene 10 % de descuento, siempre por encima del costo.

El costo guardado en el producto es un supuesto: alimentos con menos margen y cuidado personal con más. El análisis no inventa ese margen después; lo calcula con esos costos.

## Herramientas

SQL Server, Python, Pandas, Matplotlib y Power BI.

## Proceso de análisis

```bash
python scripts/generar_datos.py
python scripts/analisis_ventas.py
```

El análisis comprueba las llaves, que ninguna venta sea anterior al registro del cliente y que ningún precio quede por debajo del costo. Después escribe `resultados.md` y `public/datos/ventas.json`.

Las consultas están en `sql/base_datos_ventas.sql` y `sql/consultas_ventas.sql`.

## Indicadores

- Ingreso de la línea = cantidad × precio_unitario.
- Costo de la línea = cantidad × costo del producto.
- Margen bruto = ingresos − costo.
- Margen porcentual = margen bruto / ingresos × 100.
- Ticket promedio = ingresos / número de ventas.
- Cliente recurrente = cliente con 3 o más ventas.

## Resultados calculados

Cifras de la semilla 7.

- Ingresos: 118.621.300 COP
- Ventas: 1.500
- Ticket promedio: 79.081 COP
- Margen bruto: 42.766.457 COP (36,05 %)
- Clientes con al menos una compra: 261 de 300
- Clientes recurrentes: 165

## Conclusiones

- El producto con más unidades fue Azúcar 500 g (405). El de más ingresos fue Aceite 3000 ml (5.977.960 COP). No son el mismo.
- Alimentos concentró 47,40 % de los ingresos.
- El mayor margen porcentual fue el de cuidado personal, 45,27 %.
- Diciembre fue el mes de mayores ingresos: 14.342.190 COP.
- El 63,22 % de los clientes que compraron lo hizo tres veces o más. Con 1.500 ventas y 300 clientes en el maestro, esa proporción es alta y hay que leerla dentro de ese tamaño.

## Limitaciones

- El descuento y el costo son reglas del generador, no una política comercial observada.
- 39 clientes del maestro no compraron en 2025.
- El ticket de la web está redondeado al peso. SQL puede mostrar los decimales.
- No hay devoluciones ni medios de pago.

## Posibles mejoras

- Medir la distancia entre compras con la consulta que usa `LAG`.
- Separar clientes nuevos y clientes que ya venían de 2024.
- Agregar una meta de ventas por mes.
