# Análisis de indicadores operativos

Demostración con datos ficticios. Sirve para comparar áreas y semanas, no para describir una operación real.

## Problema de negocio

Hay que seguir si las áreas cumplen la meta y cómo cambia ese cumplimiento a lo largo del año. También hace falta no mezclar indicadores que usan unidades distintas.

## Objetivo

Calcular el cumplimiento, la productividad por área y la evolución semanal y mensual.

## Dataset

`datos/datos_operativos.csv` tiene 1.500 registros, semilla 21. Van del 2 de enero al 17 de diciembre de 2025. El archivo se detiene al llegar a 1.500 filas, por eso diciembre no está completo.

| Columna | Qué representa |
| --- | --- |
| id_registro | Identificador |
| fecha | Día del registro |
| area | Producción, Calidad, Logística, Empaque o Mantenimiento |
| responsable | Persona del área |
| actividad | Actividad registrada ese día |
| meta | Meta del día, siempre mayor que cero |
| resultado | Lo que se logró, en la misma unidad de la meta |
| horas_trabajadas | Horas del registro, siempre mayores que cero |
| estado | Cumplida, Parcial o No cumplida |

`datos/catalogo_actividades.csv` dice la unidad de cada actividad. Dentro de un área la unidad no cambia: ramos, lotes, despachos, cajas u órdenes.

El generador deja a Mantenimiento con una base más baja y a febrero un poco por debajo del resto del año. Es un supuesto, y el resultado se lee después de calcular.

## Herramientas

Python, SQL Server, Power BI y Excel. Hay una guía corta en `excel/guia_excel.md` y otra en `powerbi/powerbi_guia.md`.

## Proceso de análisis

```bash
python scripts/generar_datos.py
python scripts/analisis_operativo.py
```

El análisis vuelve a calcular el estado y compara con el archivo. Si no coincide, se detiene. También rechaza metas u horas en cero.

La semana del dashboard es la semana ISO junto con su año ISO.

## Indicadores

- Cumplimiento de la actividad = resultado / meta × 100.
- Cumplimiento promedio = media de esos porcentajes. Es el KPI general.
- Cumplimiento del área = suma de resultados / suma de metas × 100.
- Productividad del área = suma de resultados / suma de horas. Solo se interpreta dentro de su unidad.
- Cumplida: resultado mayor o igual que la meta.
- Parcial: al menos el 80 % de la meta, sin llegar al 100 %. La comparación usa enteros (`resultado * 5 >= meta * 4`) para no depender de decimales.
- No cumplida: por debajo del 80 %.

El porcentaje de actividades cumplidas no es el cumplimiento promedio. Una actividad en 95 % sigue en estado Parcial.

## Resultados calculados

Cifras de la semilla 21.

- Actividades: 1.500
- Cumplimiento promedio: 89,24 %
- Actividades cumplidas: 164 (10,93 %)
- Horas: 10.780

| Área | Unidad | Cumplimiento | Productividad |
| --- | --- | ---: | ---: |
| Calidad | lotes | 97,55 % | 3,57 |
| Producción | ramos | 93,38 % | 35,19 |
| Empaque | cajas | 89,02 % | 16,00 |
| Logística | despachos | 88,74 % | 1,43 |
| Mantenimiento | órdenes | 79,24 % | 0,80 |

## Conclusiones

- El cumplimiento promedio está en 89,24 %, pero solo 164 actividades llegaron a la meta.
- Calidad quedó arriba (97,55 %) y Mantenimiento abajo (79,24 %).
- Noviembre tuvo el cumplimiento promedio más alto (93,08 %) y febrero el más bajo (85,07 %).
- La productividad de Mantenimiento es 0,80 órdenes por hora. No se compara con los ramos por hora de Producción.

## Limitaciones

- Diciembre termina el 17, así que tiene menos registros. El cumplimiento del mes sigue siendo un promedio de filas; el conteo de actividades no es comparable con un mes completo.
- Las metas y las bases de cumplimiento son supuestos del generador.
- No hay costo, retrabajo ni tiempo de espera. Las horas son las registradas en la fila.

## Posibles mejoras

- Definir una meta de cumplimiento por área y marcar las semanas que quedan debajo.
- Separar el promedio de filas y el cumplimiento por sumas también en el KPI general, para ver los dos lados.
- Completar diciembre si se amplía el archivo por encima de 1.500 filas.
