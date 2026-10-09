# Guía para armar el dashboard operativo en Power BI

No hay un archivo `.pbix`. Se arma en Power BI Desktop con `datos/datos_operativos.csv` y, si se quiere mostrar la unidad, con `datos/catalogo_actividades.csv`.

Las medidas repiten las definiciones de `scripts/analisis_operativo.py`.

## 1. Importar y transformar

1. Obtener datos desde `datos_operativos.csv`.
2. `fecha` como Fecha.
3. `meta`, `resultado` y `horas_trabajadas` como número entero.
4. Revisar que no haya metas ni horas en cero. El generador no las deja pasar, y el análisis tampoco.

Opcional: importar `catalogo_actividades.csv` y relacionar `Registros[actividad]` con `catalogo_actividades[actividad]`.

## 2. Calendario con año y semana

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

Relacionar `Calendario[Date]` con `Registros[fecha]`. En el gráfico semanal usar `Clave semana`, no solo el número de semana.

## 3. Medidas DAX

Hay dos cumplimientos y no significan lo mismo.

```dax
Cumplimiento Fila =
DIVIDE ( Registros[resultado], Registros[meta] )
```

Esa es una columna calculada. El KPI general es su promedio:

```dax
Cumplimiento Promedio = AVERAGE ( Registros[Cumplimiento Fila] )
```

El cumplimiento del área usa sumas, porque dentro del área la unidad es la misma:

```dax
Cumplimiento Area =
DIVIDE (
    SUM ( Registros[resultado] ),
    SUM ( Registros[meta] )
)
```

```dax
Productividad Area =
DIVIDE (
    SUM ( Registros[resultado] ),
    SUM ( Registros[horas_trabajadas] )
)
```

```dax
Actividades = COUNTROWS ( Registros )

Actividades Cumplidas =
CALCULATE (
    COUNTROWS ( Registros ),
    Registros[estado] = "Cumplida"
)

Horas = SUM ( Registros[horas_trabajadas] )
```

`DIVIDE` devuelve blanco si la meta o las horas fueran cero, en lugar de romper el visual.

## 4. Visuales

- Tarjetas: Actividades, Cumplimiento Promedio, Actividades Cumplidas, Horas.
- Barras por `area` con Cumplimiento Area.
- Líneas por `Clave semana` con Cumplimiento Promedio.
- Columnas por mes con Cumplimiento Promedio.
- Circular por `estado`.
- Tabla por área: unidad, Cumplimiento Area y Productividad Area.

No pongas la productividad de todas las áreas en un solo eje. Ramo por hora y orden por hora no se comparan.

Con la semilla 21, el cumplimiento promedio quedó en 89,24 % y las actividades cumplidas en 164 de 1.500. Mantenimiento es el área más baja, con 79,24 %.
