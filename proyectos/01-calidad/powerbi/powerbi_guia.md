# Guía para armar el dashboard en Power BI

Esta guía no incluye un archivo `.pbix`. El dashboard se construye en Power BI Desktop a partir de `datos/datos_calidad.csv`. Las medidas usan la misma definición que `scripts/analisis_calidad.py`.

## 1. Importar el CSV

1. Abrir Power BI Desktop.
2. Inicio, Obtener datos, Texto o CSV.
3. Elegir `datos/datos_calidad.csv`.
4. Comprobar que la codificación se vea bien (las tildes de San José y de los nombres).
5. Cargar.

## 2. Transformar en Power Query

En Transformar datos:

- `fecha`: tipo Fecha.
- `ramos_revisados`, `ramos_no_conformes`, `semana` y `anio`: número entero.
- `id_inspeccion`: número entero.

Para revisar la regla de negocio, se puede agregar una columna condicional o filtrar las filas donde `ramos_no_conformes` sea mayor que `ramos_revisados`. En el archivo generado no debería aparecer ninguna.

Cerrar y aplicar.

Si se quieren usar la zona y el tipo de flor, importar también `fincas.csv` y `variedades.csv`. La relación es `Inspecciones[finca]` con `fincas[finca]`, y `Inspecciones[variedad]` con `variedades[variedad]`. En ambos casos la tabla de catálogo queda del lado uno.

## 3. Tabla calendario

Crear una tabla con esta expresión DAX:

```dax
Calendario =
ADDCOLUMNS (
    CALENDAR ( DATE ( 2025, 1, 1 ), DATE ( 2025, 12, 31 ) ),
    "Año", YEAR ( [Date] ),
    "Mes", MONTH ( [Date] ),
    "Nombre mes", FORMAT ( [Date], "MMM" ),
    "Semana ISO", WEEKNUM ( [Date], 21 )
)
```

`WEEKNUM` con el argumento 21 devuelve la semana ISO. Relacionar `Calendario[Date]` con `Inspecciones[fecha]`, del lado uno hacia las inspecciones.

Para no mezclar la semana 1 de dos años distintos, la clave de la semana debe llevar el año. En este archivo las fechas van del 2 de enero al 26 de diciembre de 2025, así que el año calendario y el año ISO coinciden. Aun así, esta columna deja la clave explícita:

```dax
Clave semana =
VAR Semana = WEEKNUM ( Calendario[Date], 21 )
VAR AnioBase = YEAR ( Calendario[Date] )
VAR AnioISO =
    IF (
        Semana = 1 && MONTH ( Calendario[Date] ) = 12,
        AnioBase + 1,
        IF (
            Semana >= 52 && MONTH ( Calendario[Date] ) = 1,
            AnioBase - 1,
            AnioBase
        )
    )
RETURN
    AnioISO & "-S" & FORMAT ( Semana, "00" )
```

## 4. Medidas DAX

El porcentaje no es el promedio de cada inspección. Es el total de no conformes dividido por el total de revisados.

```dax
Ramos Revisados = SUM ( Inspecciones[ramos_revisados] )

Ramos No Conformes = SUM ( Inspecciones[ramos_no_conformes] )

% No Conformidad =
DIVIDE ( [Ramos No Conformes], [Ramos Revisados] )
```

Para las causas, una medida filtrada evita contar la etiqueta "Sin no conformidad":

```dax
Ramos con causa =
CALCULATE (
    [Ramos No Conformes],
    Inspecciones[ramos_no_conformes] > 0
)
```

## 5. Armar el informe

Una página alcanza:

- Tarjetas: Ramos Revisados, Ramos No Conformes, % No Conformidad.
- Gráfico de líneas: eje `Clave semana`, valor `% No Conformidad`.
- Barras: eje `finca`, valor `% No Conformidad`.
- Barras o circular: eje `causa_no_conformidad`, valor `Ramos con causa`.
- Barras: eje `variedad`, valor `% No Conformidad`.
- Tabla: finca, revisados, no conformes y porcentaje.
- Segmentación de datos por mes, usando la tabla calendario.

Formato de `% No Conformidad` en porcentaje, con dos decimales.

El archivo de Python ya calculó el resultado de esta carga: 462.553 ramos revisados, 27.284 no conformes y 5,90 %. Si el informe no se acerca a esas cifras, conviene revisar el tipo de las columnas o un filtro activo.
