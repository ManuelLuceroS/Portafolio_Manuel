/*
    Indicadores operativos para SQL Server.
    Los registros salen de datos/datos_operativos.csv.
    La unidad de cada actividad está en datos/catalogo_actividades.csv.

    Cumplimiento de una fila: resultado / meta.
    Cumplimiento de un área: suma de resultados / suma de metas.
    La semana se arma con el año ISO y la semana ISO.
*/

CREATE TABLE Areas (
    area NVARCHAR(80) NOT NULL PRIMARY KEY
);

CREATE TABLE Actividades (
    actividad NVARCHAR(120) NOT NULL PRIMARY KEY,
    area NVARCHAR(80) NOT NULL,
    unidad NVARCHAR(40) NOT NULL,
    CONSTRAINT FK_Actividades_Areas
        FOREIGN KEY (area) REFERENCES Areas (area)
);

CREATE TABLE Registros (
    id_registro INT NOT NULL PRIMARY KEY,
    fecha DATE NOT NULL,
    area NVARCHAR(80) NOT NULL,
    responsable NVARCHAR(80) NOT NULL,
    actividad NVARCHAR(120) NOT NULL,
    meta INT NOT NULL,
    resultado INT NOT NULL,
    horas_trabajadas INT NOT NULL,
    estado NVARCHAR(20) NOT NULL,
    CONSTRAINT FK_Registros_Actividades
        FOREIGN KEY (actividad) REFERENCES Actividades (actividad),
    CONSTRAINT CK_Registros_Valores
        CHECK (meta > 0 AND resultado >= 0 AND horas_trabajadas > 0)
);

CREATE INDEX IX_Registros_Fecha ON Registros (fecha);

INSERT INTO Areas (area) VALUES
    (N'Producción'),
    (N'Calidad'),
    (N'Logística'),
    (N'Empaque'),
    (N'Mantenimiento');

INSERT INTO Actividades (actividad, area, unidad) VALUES
    (N'Corte en cultivo', N'Producción', N'ramos'),
    (N'Preparación de ramos', N'Producción', N'ramos'),
    (N'Inspección de lote', N'Calidad', N'lotes'),
    (N'Reinspección de lote', N'Calidad', N'lotes'),
    (N'Despacho urbano', N'Logística', N'despachos'),
    (N'Despacho regional', N'Logística', N'despachos'),
    (N'Armado de cajas', N'Empaque', N'cajas'),
    (N'Etiquetado', N'Empaque', N'cajas'),
    (N'Revisión de equipos', N'Mantenimiento', N'órdenes'),
    (N'Mantenimiento preventivo', N'Mantenimiento', N'órdenes');

/* Cumplimiento promedio y actividades que llegaron a la meta. */
SELECT
    COUNT(*) AS actividades,
    AVG(CAST(resultado AS DECIMAL(18, 4)) / meta) * 100 AS cumplimiento_promedio,
    SUM(CASE WHEN estado = N'Cumplida' THEN 1 ELSE 0 END) AS actividades_cumplidas,
    SUM(horas_trabajadas) AS horas_trabajadas
FROM Registros;

/* Cumplimiento y productividad por área. La unidad sale del catálogo. */
SELECT
    r.area,
    a.unidad,
    COUNT(*) AS actividades,
    SUM(r.resultado) AS resultado,
    SUM(r.meta) AS meta,
    CAST(SUM(r.resultado) AS DECIMAL(18, 2))
        / NULLIF(SUM(r.meta), 0) * 100 AS cumplimiento,
    CAST(SUM(r.resultado) AS DECIMAL(18, 2))
        / NULLIF(SUM(r.horas_trabajadas), 0) AS productividad
FROM Registros AS r
INNER JOIN Actividades AS a
    ON a.actividad = r.actividad
WHERE r.meta > 0
  AND r.horas_trabajadas > 0
GROUP BY r.area, a.unidad
ORDER BY cumplimiento;

/* Áreas por debajo de 90 % de cumplimiento. */
WITH CumplimientoArea AS (
    SELECT
        area,
        CAST(SUM(resultado) AS DECIMAL(18, 2)) / NULLIF(SUM(meta), 0) * 100 AS cumplimiento
    FROM Registros
    GROUP BY area
)
SELECT
    area,
    cumplimiento
FROM CumplimientoArea
WHERE cumplimiento < 90
ORDER BY cumplimiento;

/* Tendencia semanal. Año ISO y semana ISO van juntos. */
WITH Marcadas AS (
    SELECT
        fecha,
        CAST(resultado AS DECIMAL(18, 4)) / NULLIF(meta, 0) * 100 AS cumplimiento,
        DATEPART(ISO_WEEK, fecha) AS semana_iso,
        YEAR(DATEADD(DAY, 26 - DATEPART(ISO_WEEK, fecha), fecha)) AS anio_iso
    FROM Registros
    WHERE meta > 0
)
SELECT
    anio_iso,
    semana_iso,
    AVG(cumplimiento) AS cumplimiento_promedio,
    COUNT(*) AS actividades
FROM Marcadas
GROUP BY anio_iso, semana_iso
ORDER BY anio_iso, semana_iso;

/* Comparación mensual. */
SELECT
    YEAR(fecha) AS anio,
    MONTH(fecha) AS mes,
    AVG(CAST(resultado AS DECIMAL(18, 4)) / meta) * 100 AS cumplimiento_promedio,
    COUNT(*) AS actividades
FROM Registros
WHERE meta > 0
GROUP BY YEAR(fecha), MONTH(fecha)
ORDER BY anio, mes;

/* Actividades que no alcanzaron el 80 % de la meta. */
SELECT
    id_registro,
    fecha,
    area,
    actividad,
    meta,
    resultado,
    estado
FROM Registros
WHERE resultado * 5 < meta * 4
ORDER BY fecha, area;
