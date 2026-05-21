# exact-cover

Solución al problema **Exact Cover** mediante *Backtracking* con poda algebraica, implementada en Python puro.

## ¿Qué es el Exact Cover?

Dado un conjunto universo `U` y una familia de subconjuntos `S`, se busca una subcolección `S' ⊆ S` tal que:

- `⋃ S' = U` — cubre todo el universo
- `∀ Sᵢ, Sⱼ ∈ S', i≠j ⟹ Sᵢ ∩ Sⱼ = ∅` — sin solapamientos (partición exacta)

Este problema es **NP-completo**, por lo que la optimización estructural del árbol de búsqueda es fundamental.

---

## Instalación

### Vía pip (recomendado)

```bash
pip install .


### Desde el repositorio

git clone <repo-url>
cd exact_cover_pkg
pip install -e .

### Requisitos

- Python ≥ 3.9
- No tiene dependencias externas (solo biblioteca estándar)

---

## Uso rápido

```python
from solver import solve_exact_cover

universe = [1, 2, 3, 4, 5, 6, 7]
subsets  = [
    {1, 2, 3},
    {4, 5},
    {6, 7},
    {1, 4},
    {2, 5, 6, 7},
    {3, 4, 5, 6, 7},
]

result = solve_exact_cover(universe, subsets)
print(result)  # [(1, 2, 3), (4, 5), (6, 7)]

Si no existe solución:

from exact_cover import solve_exact_cover

universe = [1, 2, 3, 4, 5, 6, 7]
subsets  = [
    {1, 2, 3},
    {4, 5},
    {6, 7},
    {1, 4},
    {2, 5, 6, 7},
    {3, 4, 5, 6, 7},
]

result = solve_exact_cover(universe, subsets)
print(result)  # [(1, 2, 3), (4, 5), (6, 7)]

### Comparar con el algoritmo base (fuerza bruta)

```python
from exact_cover import solve_exact_cover, solve_exact_cover_base

r_base = solve_exact_cover_base(universe, subsets)
r_opti = solve_exact_cover(universe, subsets)

## API

### `solve_exact_cover(universe, subsets)`

Algoritmo **optimizado** con poda algebraica doble:

1. **Filtrado previo** — solo considera subconjuntos `⊆ elementos_faltantes`.
2. **Poda de disjunción** — al elegir un subconjunto, descarta todos los que compartan algún elemento.

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `universe` | `Iterable` | Elementos que deben cubrirse exactamente |
| `subsets` | `Iterable[Iterable]` | Familia de subconjuntos candidatos |

**Retorna:** `list[tuple]` con la cobertura exacta, o `None` si no existe.

### `solve_exact_cover_base(universe, subsets)`

Algoritmo de **fuerza bruta** (Programa 1). Misma interfaz. Incluido para comparativa de rendimiento.

---

## Pruebas

```bash
# Instalar dependencias de desarrollo
pip install -e ".[dev]"

# Ejecutar suite completa (método seguro para entornos virtuales)
python -m pytest tests/ -v

La suite cubre:
- Casos triviales y de validación básica
- Casos de borde (universo vacío, sin solución, elemento único)
- Correctitud matemática (unión = universo, subconjuntos disjuntos)
- Prueba de estrés con 376 subconjuntos ruidosos
- Dataset "envenenado" con 30 000 conjuntos basura

---

## Rendimiento comparativo

| Escenario | `U` | `S` | Prog. 1 | Prog. 2 | Aceleración |
|-----------|-----|-----|---------|---------|-------------|
| Caso Trivial | 7 | 6 | 0.032 ms | 0.023 ms | 1.4× |
| Prueba de Estrés | 30 | 406 | 2.20 ms | 0.40 ms | **5.5×** |
| Dataset Envenenado | 12 | 30 066 | 57.8 ms | 13.0 ms | 4.4× |
| Prueba masiva | 14 | 10 056 | 121.09 s | 67.28 s | 1.8× |

La condición `Sᵢ ∩ Sⱼ = ∅` es el núcleo de la optimización: reduce drásticamente el árbol de búsqueda en situaciones con alta densidad de subconjuntos.

---

## Estructura del proyecto

```
exact-cover/
├── exact_cover/
│   ├── __init__.py          # API pública del paquete
│   ├── solver.py            # Programa 2 — backtracking con poda algebraica
│   └── solver_base.py       # Programa 1 — fuerza bruta (referencia)
├── tests/
│   ├── conftest.py
│   └── test_exact_cover.py  # Suite completa de pruebas unitarias
├── examples/
│   └── exact_cover_demo.ipynb  # Jupyter notebook con ejemplos y benchmarks
├── docs/
│   └── Algoritmos.pdf       # Documento LaTeX con análisis matemático
├── pyproject.toml
└── README.md
```

---

## Referencia

Kreher, D. L., & Stinson, D. R. (1999). *Combinatorial Algorithms: Generation, Enumeration, and Search*. CRC Press. (pp. 118–121).

---

## Historial de versiones

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0.0 | 2026-05-19 | Release inicial con Programa 1, Programa 2 y suite de pruebas |
