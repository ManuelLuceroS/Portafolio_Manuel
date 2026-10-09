# Resultados del análisis operativo

Estos números los escribió `analisis_operativo.py` después de leer el CSV.

## Indicadores

- Actividades: 1.500
- Cumplimiento promedio: 89,24 %
- Actividades cumplidas: 164 (10,93 %)
- Horas trabajadas: 10.780

## Por área

| Área | Unidad | Cumplimiento | Productividad |
| --- | --- | ---: | ---: |
| Calidad | lotes | 97,55 % | 3,57 |
| Producción | ramos | 93,38 % | 35,19 |
| Empaque | cajas | 89,02 % | 16,00 |
| Logística | despachos | 88,74 % | 1,43 |
| Mantenimiento | órdenes | 79,24 % | 0,80 |

## Conclusiones

- Se registraron 1.500 actividades. El cumplimiento promedio fue 89,24 %.
- 164 actividades alcanzaron o superaron la meta (10,93 %).
- El área con mayor cumplimiento fue Calidad (97,55 %) y la de menor fue Mantenimiento (79,24 %).
- En Mantenimiento la productividad fue 0,80 órdenes por hora. Esa cifra no se compara con otras áreas porque la unidad es distinta.
- El mes con mayor cumplimiento promedio fue Nov (93,08 %) y el de menor fue Feb (85,07 %).
- Las horas registradas suman 10.780.

## Validación

- 1500 filas, sin metas ni horas en cero.
- El estado de cada fila coincide con la regla de 80 % y 100 %.
- Cada área tiene una sola unidad de medida.
