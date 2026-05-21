"""
solver_base.py — Brute-force algorithm for Exact Cover (Programa 1).

Implements brute force with simple backtracking:
  - Iterates linearly over all available subsets.
  - Verifies there is no overlap with already covered elements.
  - No pre-filtering.
Included as a baseline to compare performance against Programa 2.
"""

from __future__ import annotations
from typing import Collection, Hashable, Optional


def solve_exact_cover_base(
    universe: Collection[Hashable],
    subsets: Collection[Collection[Hashable]],
) -> Optional[list[tuple]]:
    """
    Solves the Exact Cover problem using brute force.
    """
    universo_set = set(universe)
    subconjuntos_sets = [set(s) for s in subsets]

    def backtrack(
        elementos_faltantes: set,
        subconjuntos_disponibles: list[set],
        solucion_actual: list[set],
    ) -> Optional[list[set]]:
     
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

    
    if solucion_final:
        
        return [tuple(sorted(list(s))) for s in solucion_final]
    else:
        return None  
