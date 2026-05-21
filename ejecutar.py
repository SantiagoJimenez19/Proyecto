import time
from exact_cover import solve_exact_cover, solve_exact_cover_base

# Definimos un caso de prueba (El caso trivial)
universo = [1, 2, 3, 4, 5, 6, 7]
subsets = [
    {1, 2, 3},
    {4, 5},
    {6, 7},
    {1, 4},
    {2, 5, 6, 7},
    {3, 4, 5, 6, 7}
]

print("=" * 50)
print("  EJECUTANDO ALGORITMOS PARA EXACT COVER")
print("=" * 50)

# 1. Probar Programa 1 (Base)
inicio = time.perf_counter()
solucion_base = solve_exact_cover_base(universo, subsets)
fin = time.perf_counter()
print(f"Prog 1 (Base) - Solución: {solucion_base}")
print(f"Prog 1 (Base) - Tiempo:   {(fin - inicio) * 1000:.4f} ms\n")

# 2. Probar Programa 2 (Optimizado con Poda Algebraica)
inicio = time.perf_counter()
solucion_opti = solve_exact_cover(universo, subsets)
fin = time.perf_counter()
print(f"Prog 2 (Opti) - Solución: {solucion_opti}")
print(f"Prog 2 (Opti) - Tiempo:   {(fin - inicio) * 1000:.4f} ms")
print("=" * 50)