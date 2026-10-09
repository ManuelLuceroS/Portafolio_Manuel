/*
    Consultas de ventas para SQL Server.
    Suponen que las tablas de base_datos_ventas.sql ya están cargadas.
    Un cliente recurrente es el que tiene 3 o más compras.
*/

/* 1. Ventas mensuales, con el acumulado del año. */
WITH Mensual AS (
    SELECT
        YEAR(v.fecha_venta) AS anio,
        MONTH(v.fecha_venta) AS mes,
        SUM(d.cantidad * d.precio_unitario) AS ingresos,
        COUNT(DISTINCT v.id_venta) AS ventas
    FROM Ventas AS v
    INNER JOIN DetalleVentas AS d
        ON d.id_venta = v.id_venta
    GROUP BY YEAR(v.fecha_venta), MONTH(v.fecha_venta)
)
SELECT
    anio,
    mes,
    ingresos,
    ventas,
    CAST(ingresos AS DECIMAL(18, 2)) / NULLIF(ventas, 0) AS ticket_promedio,
    SUM(ingresos) OVER (ORDER BY anio, mes) AS ingresos_acumulados
FROM Mensual
ORDER BY anio, mes;

/* 2. Top 10 productos por unidades. */
SELECT TOP 10
    p.producto,
    p.categoria,
    SUM(d.cantidad) AS unidades,
    SUM(d.cantidad * d.precio_unitario) AS ingresos
FROM DetalleVentas AS d
INNER JOIN Productos AS p
    ON p.id_producto = d.id_producto
GROUP BY p.producto, p.categoria
ORDER BY unidades DESC, ingresos DESC;

/* 3. Clientes con mayores compras, medidas en ingresos. */
SELECT TOP 10
    c.id_cliente,
    c.nombre,
    c.ciudad,
    COUNT(DISTINCT v.id_venta) AS compras,
    SUM(d.cantidad * d.precio_unitario) AS ingresos
FROM Clientes AS c
INNER JOIN Ventas AS v
    ON v.id_cliente = c.id_cliente
INNER JOIN DetalleVentas AS d
    ON d.id_venta = v.id_venta
GROUP BY c.id_cliente, c.nombre, c.ciudad
ORDER BY ingresos DESC;

/* 4. Ventas por categoría. */
SELECT
    p.categoria,
    SUM(d.cantidad) AS unidades,
    SUM(d.cantidad * d.precio_unitario) AS ingresos,
    SUM(d.cantidad * p.costo) AS costo,
    SUM(d.cantidad * d.precio_unitario) - SUM(d.cantidad * p.costo) AS margen_bruto
FROM DetalleVentas AS d
INNER JOIN Productos AS p
    ON p.id_producto = d.id_producto
GROUP BY p.categoria
ORDER BY ingresos DESC;

/* 5. Ticket promedio del periodo. */
WITH TotalVenta AS (
    SELECT
        id_venta,
        SUM(cantidad * precio_unitario) AS ingreso
    FROM DetalleVentas
    GROUP BY id_venta
)
SELECT
    COUNT(*) AS numero_ventas,
    SUM(ingreso) AS ingresos,
    CAST(SUM(ingreso) AS DECIMAL(18, 2)) / NULLIF(COUNT(*), 0) AS ticket_promedio
FROM TotalVenta;

/* 6. Margen bruto estimado. */
SELECT
    SUM(d.cantidad * d.precio_unitario) AS ingresos,
    SUM(d.cantidad * p.costo) AS costo,
    SUM(d.cantidad * d.precio_unitario) - SUM(d.cantidad * p.costo) AS margen_bruto,
    CAST(
        SUM(d.cantidad * d.precio_unitario) - SUM(d.cantidad * p.costo)
        AS DECIMAL(18, 2)
    ) / NULLIF(SUM(d.cantidad * d.precio_unitario), 0) * 100 AS margen_porcentaje
FROM DetalleVentas AS d
INNER JOIN Productos AS p
    ON p.id_producto = d.id_producto;

/* 7. Clientes recurrentes: 3 o más compras. */
SELECT
    c.id_cliente,
    c.nombre,
    c.ciudad,
    COUNT(DISTINCT v.id_venta) AS compras,
    SUM(d.cantidad * d.precio_unitario) AS ingresos
FROM Clientes AS c
INNER JOIN Ventas AS v
    ON v.id_cliente = c.id_cliente
INNER JOIN DetalleVentas AS d
    ON d.id_venta = v.id_venta
GROUP BY c.id_cliente, c.nombre, c.ciudad
HAVING COUNT(DISTINCT v.id_venta) >= 3
ORDER BY compras DESC, ingresos DESC;

/* Compras anteriores del mismo cliente, con LAG. */
WITH Totales AS (
    SELECT
        v.id_cliente,
        v.id_venta,
        v.fecha_venta,
        SUM(d.cantidad * d.precio_unitario) AS ingreso
    FROM Ventas AS v
    INNER JOIN DetalleVentas AS d
        ON d.id_venta = v.id_venta
    GROUP BY v.id_cliente, v.id_venta, v.fecha_venta
)
SELECT
    id_cliente,
    id_venta,
    fecha_venta,
    ingreso,
    LAG(fecha_venta) OVER (
        PARTITION BY id_cliente
        ORDER BY fecha_venta, id_venta
    ) AS compra_anterior,
    ROW_NUMBER() OVER (
        PARTITION BY id_cliente
        ORDER BY fecha_venta, id_venta
    ) AS numero_compra
FROM Totales
ORDER BY id_cliente, numero_compra;
