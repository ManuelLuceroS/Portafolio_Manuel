"""Genera los tres datasets y actualiza los JSON que consume la web."""

import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

PASOS = [
    "proyectos/01-calidad/scripts/generar_datos.py",
    "proyectos/01-calidad/scripts/analisis_calidad.py",
    "proyectos/02-ventas/scripts/generar_datos.py",
    "proyectos/02-ventas/scripts/analisis_ventas.py",
    "proyectos/03-operaciones/scripts/generar_datos.py",
    "proyectos/03-operaciones/scripts/analisis_operativo.py",
]


def main():
    for paso in PASOS:
        ruta = RAIZ / paso
        print(f"\n=== {paso} ===")
        subprocess.check_call([sys.executable, str(ruta)])
    print("\nListo. Los dashboards leen public/datos/*.json.")


if __name__ == "__main__":
    main()
