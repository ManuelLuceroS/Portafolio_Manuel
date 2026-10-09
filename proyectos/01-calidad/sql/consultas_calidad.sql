/*
    Análisis de calidad para SQL Server.
    Los datos son ficticios y salen de los CSV de la carpeta datos.

    Orden de carga:
    1. Fincas
    2. Variedades
    3. Inspecciones, desde datos_calidad.csv

    En Power BI o en SSMS se puede usar el asistente de importación.
    Conviene traer el CSV como UTF-8 para conservar tildes.
*/

CREATE TABLE Fincas (
    id_finca INT NOT NULL PRIMARY KEY,
    finca NVARCHAR(80) NOT NULL,
    zona NVARCHAR(80) NOT NULL,
    CONSTRAINT UQ_Fincas_Nombre UNIQUE (finca)
);

CREATE TABLE Variedades (
    id_variedad INT NOT NULL PRIMARY KEY,
    variedad NVARCHAR(80) NOT NULL,
    tipo NVARCHAR(40) NOT NULL,
    CONSTRAINT UQ_Variedades_Nombre UNIQUE (variedad)
);

CREATE TABLE Inspecciones (
    id_inspeccion INT NOT NULL PRIMARY KEY,
    fecha DATE NOT NULL,
    finca NVARCHAR(80) NOT NULL,
    variedad NVARCHAR(80) NOT NULL,
    ramos_revisados INT NOT NULL,
    ramos_no_conformes INT NOT NULL,
    causa_no_conformidad NVARCHAR(80) NOT NULL,
    inspector NVARCHAR(80) NOT NULL,
    semana INT NOT NULL,
    anio INT NOT NULL,
    CONSTRAINT FK_Inspecciones_Fincas
        FOREIGN KEY (finca) REFERENCES Fincas (finca),
    CONSTRAINT FK_Inspecciones_Variedades
        FOREIGN KEY (variedad) REFERENCES Variedades (variedad),
    CONSTRAINT CK_Inspecciones_Cantidades
        CHECK (
            ramos_revisados > 0
            AND ramos_no_conformes >= 0
            AND ramos_no_conformes <= ramos_revisados
        )
);

CREATE INDEX IX_Inspecciones_Fecha ON Inspecciones (fecha);

INSERT INTO Fincas (id_finca, finca, zona) VALUES
    (1, N'Las Acacias', N'Sabana norte'),
    (2, N'La Esperanza', N'Sabana norte'),
    (3, N'San José', N'Sabana occidente'),
    (4, N'Los Pinos', N'Sabana'),
    (5, N'El Mirador', N'Tequendama');

INSERT INTO Variedades (id_variedad, variedad, tipo) VALUES
    (1, N'Rosa roja', N'Rosa'),
    (2, N'Rosa blanca', N'Rosa'),
    (3, N'Clavel', N'Clavel'),
    (4, N'Crisantemo', N'Crisantemo'),
    (5, N'Girasol', N'Girasol'),
    (6, N'Alstroemeria', N'Alstroemeria');

/* Total de ramos y porcentaje general. */
SELECT
    SUM(ramos_revisados) AS ramos_revisados,
    SUM(ramos_no_conformes) AS ramos_no_conformes,
    CAST(SUM(ramos_no_conformes) AS DECIMAL(18, 2))
        / NULLIF(SUM(ramos_revisados), 0) * 100 AS porcentaje_no_conformidad
FROM Inspecciones;

/* Inspecciones con no conformidad en una finca. */
SELECT TOP 50
    id_inspeccion,
    fecha,
    variedad,
    ramos_revisados,
    ramos_no_conformes,
    causa_no_conformidad
FROM Inspecciones
WHERE finca = N'El Mirador'
  AND ramos_no_conformes > 0
ORDER BY fecha, id_inspeccion;

/* No conformidad por finca. */
SELECT
    finca,
    SUM(ramos_revisados) AS ramos_revisados,
    SUM(ramos_no_conformes) AS ramos_no_conformes,
    CAST(SUM(ramos_no_conformes) AS DECIMAL(18, 2))
        / NULLIF(SUM(ramos_revisados), 0) * 100 AS porcentaje_no_conformidad
FROM Inspecciones
GROUP BY finca
ORDER BY porcentaje_no_conformidad DESC;

/* No conformidad por variedad. */
SELECT
    variedad,
    SUM(ramos_revisados) AS ramos_revisados,
    SUM(ramos_no_conformes) AS ramos_no_conformes,
    CAST(SUM(ramos_no_conformes) AS DECIMAL(18, 2))
        / NULLIF(SUM(ramos_revisados), 0) * 100 AS porcentaje_no_conformidad
FROM Inspecciones
GROUP BY variedad
ORDER BY porcentaje_no_conformidad DESC;

/* Causas, sin contar las inspecciones que no tuvieron defecto. */
SELECT
    causa_no_conformidad,
    SUM(ramos_no_conformes) AS ramos,
    CAST(SUM(ramos_no_conformes) AS DECIMAL(18, 2))
        / NULLIF(
            (SELECT SUM(ramos_no_conformes) FROM Inspecciones),
            0
        ) * 100 AS porcentaje
FROM Inspecciones
WHERE ramos_no_conformes > 0
GROUP BY causa_no_conformidad
ORDER BY ramos DESC;

/* Evolución semanal. La semana ya viene calculada con calendario ISO. */
WITH ResumenSemana AS (
    SELECT
        anio,
        semana,
        SUM(ramos_revisados) AS ramos_revisados,
        SUM(ramos_no_conformes) AS ramos_no_conformes
    FROM Inspecciones
    GROUP BY anio, semana
)
SELECT
    anio,
    semana,
    ramos_revisados,
    ramos_no_conformes,
    CAST(ramos_no_conformes AS DECIMAL(18, 2))
        / NULLIF(ramos_revisados, 0) * 100 AS porcentaje_no_conformidad
FROM ResumenSemana
ORDER BY anio, semana;

/* Comparación mensual. */
SELECT
    YEAR(fecha) AS anio,
    MONTH(fecha) AS mes,
    SUM(ramos_revisados) AS ramos_revisados,
    SUM(ramos_no_conformes) AS ramos_no_conformes,
    CAST(SUM(ramos_no_conformes) AS DECIMAL(18, 2))
        / NULLIF(SUM(ramos_revisados), 0) * 100 AS porcentaje_no_conformidad
FROM Inspecciones
GROUP BY YEAR(fecha), MONTH(fecha)
ORDER BY anio, mes;

/* Las dos rosas se leen juntas usando la tabla de variedades. */
SELECT
    v.tipo,
    SUM(i.ramos_revisados) AS ramos_revisados,
    SUM(i.ramos_no_conformes) AS ramos_no_conformes,
    CAST(SUM(i.ramos_no_conformes) AS DECIMAL(18, 2))
        / NULLIF(SUM(i.ramos_revisados), 0) * 100 AS porcentaje_no_conformidad
FROM Inspecciones AS i
INNER JOIN Variedades AS v
    ON v.variedad = i.variedad
GROUP BY v.tipo
ORDER BY porcentaje_no_conformidad DESC;
