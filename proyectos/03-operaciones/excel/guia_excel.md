# Cómo revisar los indicadores en Excel

El archivo es `datos/datos_operativos.csv`. Estas pruebas sirven para contrastar el dashboard, no para reemplazar la definición del análisis.

## Abrir los datos

1. Datos, Desde texto o CSV.
2. Elegir el archivo y confirmar que la fecha se reconozca como fecha.
3. Cargar en una hoja y convertir el rango en tabla. En este ejemplo la tabla se llama `Operaciones`.

## Columna de cumplimiento

Agregar una columna:

```excel
=SI([@meta]=0;NA();[@resultado]/[@meta])
```

Si Excel está en inglés, los separadores cambian:

```excel
=IF([@meta]=0,NA(),[@resultado]/[@meta])
```

`NA()` evita dividir cuando la meta es cero. En este dataset la meta siempre es mayor que cero, pero la fórmula deja la protección escrita.

Dar a la columna formato de porcentaje.

Esta columna es el cumplimiento de cada fila. Su promedio es el KPI general del dashboard: con estos datos, 89,24 %.

## Tabla dinámica por área

1. Insertar, Tabla dinámica.
2. Filas: `area`.
3. Valores: suma de `resultado`, suma de `meta`, promedio de la columna de cumplimiento.

El promedio de la columna no es el mismo número que usa el gráfico de áreas. Ese gráfico usa:

```text
suma de resultado / suma de meta
```

En la tabla dinámica se puede agregar un campo calculado:

```text
CumplimientoArea = resultado / meta
```

Excel suma primero cada campo y después divide, así que el campo calculado se comporta como suma de resultados sobre suma de metas. Ese es el cumplimiento por área del dashboard.

## Lectura

- Calidad debería quedar cerca de 97,55 %.
- Mantenimiento debería quedar cerca de 79,24 %.

Si los porcentajes salen muy distintos, revisa que la tabla dinámica no tenga un filtro de fecha activo y que `resultado` y `meta` sean números, no texto.

La productividad por área es la suma de `resultado` dividida por la suma de `horas_trabajadas`. Conviene verla junto a la unidad del catálogo (`ramos`, `lotes`, `despachos`, `cajas` u `órdenes`) y no compararla entre áreas.
