# Portafolio de Manuel Lucero

Sitio personal de Manuel Enrique Lucero Suárez, analista de datos y Business Intelligence. Incluye la página del portafolio y tres proyectos con datos ficticios: calidad, ventas e indicadores operativos.

Cada dashboard muestra cifras calculadas con Python. Esas cifras viven en `public/datos` y la aplicación de React solo las presenta.

## Herramientas

- React, JavaScript y Vite
- CSS
- Recharts y Lucide React
- Python, Pandas, NumPy y Matplotlib
- SQL pensado para SQL Server
- Guías para repetir los informes en Power BI Desktop

No hay un archivo `.pbix` en el repositorio. Las guías están en la carpeta `powerbi` de cada proyecto.

## Cómo ejecutar la web

Hace falta Node.js.

```bash
npm install
npm run dev
```

La dirección local suele ser `http://localhost:5173`.

Para generar la carpeta de publicación:

```bash
npm run build
npm run preview
```

## Cómo generar los datasets

Hace falta Python 3. En esta carpeta ya se puede crear un entorno así:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python proyectos/actualizar_todo.py
```

Ese comando regenera los tres CSV, los gráficos, `resultados.md` y los JSON de `public/datos`. Las semillas están fijas: 42 para calidad, 7 para ventas y 21 para operaciones. Si no se cambian, el resultado se repite.

También se puede correr por proyecto:

```bash
python proyectos/01-calidad/scripts/generar_datos.py
python proyectos/01-calidad/scripts/analisis_calidad.py
```

Lo mismo con `02-ventas` y `03-operaciones`. El script de análisis se llama `analisis_ventas.py` o `analisis_operativo.py`.

Con el entorno ya creado, `npm run datos` llama a `.venv/bin/python`.

## Cómo actualizar los dashboards

1. Cambiar el generador o la semilla si hace falta.
2. Ejecutar `python proyectos/actualizar_todo.py`.
3. Recargar la web.

React no tiene los totales escritos en el código. Si el JSON cambia, las tarjetas y las gráficas cambian con él. Los README de cada proyecto copian las cifras de la semilla original; si cambias la semilla, vuelve a leer `resultados.md`.

## Proyectos

- [Calidad](proyectos/01-calidad/README.md): no conformidad de ramos, por finca, variedad, causa y semana.
- [Ventas](proyectos/02-ventas/README.md): ingresos, ticket, margen, productos y clientes.
- [Operaciones](proyectos/03-operaciones/README.md): cumplimiento de metas por área, semana y mes.

GitHub y LinkedIn se pegan en `src/data/portfolio.js`. Si esas cadenas están vacías, el sitio no muestra enlaces.

## Publicar en Vercel

1. Subir el repositorio a GitHub.
2. Importarlo en Vercel.
3. Framework: Vite. El comando de build es `npm run build` y la carpeta de salida es `dist`.
4. `vercel.json` reescribe las rutas del sitio para que funcionen `/proyectos/calidad`, `/proyectos/ventas` y `/proyectos/operaciones`.

Python no se ejecuta en Vercel. Hay que dejar los JSON ya generados dentro de `public/datos` antes de publicar.
