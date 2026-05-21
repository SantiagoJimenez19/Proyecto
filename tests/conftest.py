# conftest.py — Configuración de pytest
# Permite importar el paquete desde la raíz del proyecto sin instalarlo.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
