# Guía para armar el dashboard de ventas en Power BI

No hay un archivo `.pbix` en el repositorio. El informe se arma en Power BI Desktop con los cuatro CSV de `datos/`. Las medidas siguen las fórmulas de `scripts/analisis_ventas.py`.

## 1. Importar

Traer, en este orden, estos archivos como CSV:

- `clientes.csv`
- `productos.csv`
- `ventas.csv`
- `detalle_ventas.csv`

En Power Query, dejar las fechas como Fecha y los identificadores, precios, costos y cantidades como número entero.

## 2. Relaciones

En la vista de modelo:

- `Ventas[id_cliente]` hacia `Clientes[id_cliente]`.
- `DetalleVentas[id_venta]` hacia `Ventas[id_venta]`.
- `DetalleVentas[id_producto]` hacia `Productos[id_producto]`.

La dirección útil es de la tabla de catálogo o de la venta hacia el detalle. Cada relación es de uno a varios.

## 3. Calendario

```dax
Calendario =
ADDCOLUMNS (
    CALENDAR ( DATE ( 2025, 1, 1 ), DATE ( 2025, 12, 31 ) ),
    "Año", YEAR ( [Date] ),
    "Mes", MONTH ( [Date] ),
    "Nombre mes", FORMAT ( [Date], "MMM" )
)
```

Relacionar `Calendario[Date]` con `Ventas[fecha_venta]`.

## 4. Medidas DAX

El ingreso no está guardado en una columna. Se calcula en cada línea.

```dax
Ingresos =
SUMX (
    DetalleVentas,
    DetalleVentas[cantidad] * DetalleVentas[precio_unitario]
)

Costo Total =
SUMX (
    DetalleVentas,
    DetalleVentas[cantidad] * RELATED ( Productos[costo] )
)

Margen Bruto = [Ingresos] - [Costo Total]

% Margen = DIVIDE ( [Margen Bruto], [Ingresos] )

Numero Ventas = DISTINCTCOUNT ( Ventas[id_venta] )

Ticket Promedio = DIVIDE ( [Ingresos], [Numero Ventas] )

Clientes con compra = DISTINCTCOUNT ( Ventas[id_cliente] )
```

Cliente recurrente: tres o más ventas. Estas dos columnas van en la tabla Clientes.

```dax
Compras cliente =
CALCULATE ( DISTINCTCOUNT ( Ventas[id_venta] ) )

Es recurrente =
IF ( [Compras cliente] >= 3, 1, 0 )
```

Si el cliente no tiene ventas, `Compras cliente` queda en blanco y la comparación no se cumple, así que `Es recurrente` queda en 0.

```dax
Clientes recurrentes = SUM ( Clientes[Es recurrente] )
```

## 5. Visuales

- Tarjetas: Ingresos, Numero Ventas, Ticket Promedio, % Margen.
- Líneas: mes del calendario e Ingresos.
- Barras: top 10 de `producto` por `SUM(DetalleVentas[cantidad])`. En el filtro del visual, Top N = 10.
- Circular o barras: `categoria` e Ingresos.
- Tabla de clientes: nombre, ciudad, Compras cliente e Ingresos. Ordenar por ingresos y dejar los primeros.
- Tabla de categorías con Ingresos, Margen Bruto y % Margen.

Con la semilla 7, Python obtuvo 118.621.300 COP de ingresos, 1.500 ventas, ticket de 79.081 COP y margen de 36,05 %. El ticket de Power BI puede mostrar decimales; el de la web está redondeado al peso más cercano.
