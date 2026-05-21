"""
solver.py — Optimized Exact Cover algorithm (Programa 2).

Implements double algebraic pruning:
  1. Pre-filtering    : only considers subsets ⊆ missing_elements.
  2. Disjoint pruning : upon selecting a subset, it discards all others
     that share at least one element with it (Si ∩ Sj = ∅).
"""

from __future__ import annotations
from typing import Collection, Hashable, Optional


def solve_exact_cover(
    universe: Collection[Hashable],
    subsets: Collection[Collection[Hashable]],
) -> Optional[list[tuple]]:
    """
    Solves the Exact Cover problem using backtracking and pruning via set intersection.
    """
    universe_set = set(universe)
    subset_sets = [set(s) for s in subsets]

    def backtrack(
        missing_elements: set,
        available_subsets: list[set],
        current_solution: list[set],
    ) -> Optional[list[set]]:
        # Base case: all elements have already been covered
        if not missing_elements:
            return current_solution

        for i, sub in enumerate(available_subsets):
            
            if sub.issubset(missing_elements):
                new_solution = current_solution + [sub]
                new_missing = missing_elements - sub

                
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
