"""
solver_base.py — Algoritmo base para Exact Cover (Programa 1).

Implementa fuerza bruta con backtracking simple:
  - Itera linealmente sobre todos los subconjuntos disponibles.
  - Verifica que no haya solapamiento con los elementos ya cubiertos.
  - Sin filtrado previo ni poda algebraica.

Se incluye como referencia para comparar rendimiento con el Programa 2.
"""

from __future__ import annotations
from typing import Collection, Hashable, Optional


def solve_exact_cover_base(
    universe: Collection[Hashable],
    subsets: Collection[Collection[Hashable]],
) -> Optional[list[tuple]]:
    """
    Resuelve el problema Exact Cover con backtracking de fuerza bruta.

    Parameters
    ----------
    universe : iterable
        Colección de elementos que deben ser cubiertos exactamente.
    subsets : iterable de iterables
        Familia de subconjuntos candidatos.

    Returns
    -------
    list[tuple] | None
        Lista de tuplas (ordenadas) que forman la cobertura exacta,
        o ``None`` si no existe solución.

    Examples
    --------
    >>> universe = [1, 2, 3, 4, 5, 6, 7]
    >>> subsets  = [{1,2,3}, {4,5}, {6,7}]
    >>> solve_exact_cover_base(universe, subsets)
    [(1, 2, 3), (4, 5), (6, 7)]
    """
    universo_set = set(universe)
    subconjuntos_sets = [set(s) for s in subsets]

    def backtrack(
        elementos_faltantes: set,
        subconjuntos_disponibles: list[set],
        solucion_actual: list[set],
    ) -> Optional[list[set]]:
        # CASO BASE: todos los elementos cubiertos
        if not elementos_faltantes:
            return solucion_actual

        for i, sub in enumerate(subconjuntos_disponibles):
            es_valido = True
            for numero in sub:
                if numero not in elementos_faltantes:
                    es_valido = False
                    break

            if es_valido:
                nueva_solucion = solucion_actual + [sub]
                nuevos_faltantes = elementos_faltantes - sub
                nuevos_disponibles = subconjuntos_disponibles[i + 1 :]

                resultado = backtrack(nuevos_faltantes, nuevos_disponibles, nueva_solucion)
                if resultado is not None:
                    return resultado

        return None

    solucion_final = backtrack(universo_set, subconjuntos_sets, [])

    # Formateamos el resultado para que se vea ordenado al imprimirlo
    if solucion_final:
        # Convertimos los sets de vuelta a listas/tuplas ordenadas
        return [tuple(sorted(list(s))) for s in solucion_final]
    else:
        return None  # <--- Cambia el string por None
