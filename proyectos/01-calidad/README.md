# Análisis de calidad y no conformidades

Demostración con datos ficticios de una floricultora. No usa información de una empresa real.

## Problema de negocio

Hace falta saber si la no conformidad está concentrada en alguna finca, en alguna variedad o en unas semanas concretas, y cuál es la causa que más ramos afecta.

## Objetivo

Calcular el porcentaje de no conformidad y compararlo por finca, variedad, semana y mes.

## Dataset

`datos/datos_calidad.csv` tiene 3.000 inspecciones, generadas con la semilla 42.

| Columna | Qué representa |
| --- | --- |
| id_inspeccion | Identificador de la inspección |
| fecha | Día de la inspección, entre el 2 de enero y el 26 de diciembre de 2025 |
| finca | Una de cinco fincas ficticias |
| variedad | Rosa roja, rosa blanca, clavel, crisantemo, girasol o alstroemeria |
| ramos_revisados | Ramos que se revisaron en esa inspección |
| ramos_no_conformes | Ramos que no cumplieron el criterio. Nunca supera a los revisados |
| causa_no_conformidad | Causa principal. Si no hubo defectos, queda "Sin no conformidad" |
| inspector | Persona que hizo la inspección, asociada a la finca |
| semana | Semana ISO de la fecha |
| anio | Año ISO de la fecha |

También están `fincas.csv` y `variedades.csv`, para relacionar la zona y el tipo de flor en SQL.

El generador está en `scripts/generar_datos.py`. No es un sorteo independiente por columna: el volumen sube en febrero, mayo y diciembre, y la tasa de no conformidad sube en las semanas 12 a 14, 33 a 35 y en los meses de más volumen. Cada inspección guarda una sola causa principal.

## Herramientas

Python, Pandas, Matplotlib, SQL Server y Power BI. La página del portafolio lee el JSON que produce el análisis.

## Proceso de análisis

```bash
python scripts/generar_datos.py
python scripts/analisis_calidad.py
```

El segundo script valida el archivo, calcula los indicadores, guarda gráficos en `graficos/` y escribe `resultados.md`, `datos/resumen_calidad.json` y `public/datos/calidad.json`.

## Indicadores

- Porcentaje de no conformidad = suma de ramos no conformes / suma de ramos revisados × 100.
- El mismo cálculo se repite dentro de cada finca, variedad, semana y mes.
- No se promedian los porcentajes de cada inspección.

## Resultados calculados

Cifras de la semilla 42. El detalle regenerado está en `resultados.md`.

- Inspecciones: 3.000
- Ramos revisados: 462.553
- Ramos no conformes: 27.284
- Porcentaje de no conformidad: 5,90 %

## Conclusiones

- El Mirador tuvo el porcentaje más alto (9,01 %) y La Esperanza el más bajo (3,84 %).
- Girasol fue la variedad con mayor no conformidad (6,76 %).
- La causa con más ramos fue deshidratación: 4.824 ramos, 17,68 % de los no conformes.
- Marzo tuvo el porcentaje más alto (6,94 %) y julio el más bajo (5,29 %).

## Limitaciones

- La causa es una por inspección, no el detalle de cada ramo.
- La semana 1 tiene menos días porque el archivo empieza el 2 de enero. El porcentaje sigue siendo comparable; el volumen no.
- Los nombres de fincas, inspectores y las tasas de partida son supuestos del generador.
- No se puede hablar de un resultado de negocio real.

## Posibles mejoras

- Registrar varias causas por inspección, con los ramos de cada una.
- Separar el efecto de la finca y el de la variedad con un corte cruzado.
- Agregar la meta de no conformidad y marcar las semanas que la superan.
