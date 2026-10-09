# Resultados del análisis de calidad

Estos números los escribió `analisis_calidad.py` después de leer el CSV.
Si cambias la semilla, vuelve a ejecutar el script para actualizar este archivo y el dashboard.

## Indicadores

- Inspecciones: 3.000
- Ramos revisados: 462.553
- Ramos no conformes: 27.284
- Porcentaje de no conformidad: 5,90 %

## Conclusiones

- De 462.553 ramos revisados, 27.284 quedaron no conformes (5,90 %).
- La finca con mayor no conformidad fue El Mirador (9,01 %) y la de menor fue La Esperanza (3,84 %).
- La variedad con mayor no conformidad fue Girasol (6,76 %).
- La causa más frecuente fue Deshidratación, con 4.824 ramos (17,68 % de los no conformes).
- El mes con mayor porcentaje fue Mar (6,94 %) y el de menor fue Jul (5,29 %).

## Validación

- 3000 filas.
- Ningún registro tiene más ramos no conformes que revisados.
- La semana y el año del archivo coinciden con la fecha ISO.
