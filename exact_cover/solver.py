"""
solver.py — Algoritmo optimizado para Exact Cover (Programa 2).

Implementa poda algebraica doble:
  1. Filtrado previo  : solo considera subconjuntos ⊆ elementos_faltantes.
  2. Poda de disjunción: al elegir un subconjunto, descarta todos los demás
     que compartan al menos un elemento con él (Si ∩ Sj = ∅).
"""

from __future__ import annotations
from typing import Collection, Hashable, Optional


def solve_exact_cover(
    universe: Collection[Hashable],
    subsets: Collection[Collection[Hashable]],
) -> Optional[list[tuple]]:
    """
    Resuelve el problema Exact Cover con backtracking y poda algebraica.

    Dado un universo U y una familia de subconjuntos S, encuentra una
    subcolección S' ⊆ S tal que:
      - ⋃ S' = U   (cubre todo el universo)
      - ∀ Si,Sj ∈ S', i≠j ⟹ Si ∩ Sj = ∅  (partición exacta)

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
    >>> subsets  = [{1,2,3}, {4,5}, {6,7}, {1,4}, {2,5,6,7}, {3,4,5,6,7}]
    >>> solve_exact_cover(universe, subsets)
    [(1, 2, 3), (4, 5), (6, 7)]

    >>> solve_exact_cover([1, 2, 3], [{1}, {2}])   # sin solución
    """
    universe_set = set(universe)
    subset_sets = [set(s) for s in subsets]

    def backtrack(
        missing_elements: set,
        available_subsets: list[set],
        current_solution: list[set],
    ) -> Optional[list[set]]:
        # Caso base: todos los elementos ya fueron cubiertos
        if not missing_elements:
            return current_solution

        for i, sub in enumerate(available_subsets):
            # Poda 1 — Filtrado previo: S ⊆ elementos_faltantes
            if sub.issubset(missing_elements):
                new_solution = current_solution + [sub]
                new_missing = missing_elements - sub

                # Poda 2 — Disjunción: descartar subconjuntos con intersección
                new_available = [
                    s for s in available_subsets[i + 1 :]
                    if s.isdisjoint(sub)
                ]

                result = backtrack(new_missing, new_available, new_solution)
                if result is not None:
                    return result

        return None

    final_solution = backtrack(universe_set, subset_sets, [])

    if final_solution is not None:
        return [tuple(sorted(s)) for s in final_solution]
    return None
