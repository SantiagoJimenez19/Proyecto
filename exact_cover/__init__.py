"""
exact_cover
===========
Solución al problema Exact Cover mediante Backtracking.

Uso rápido
----------
>>> from exact_cover import solve_exact_cover, solve_exact_cover_base
>>> universe = [1, 2, 3, 4, 5, 6, 7]
>>> subsets  = [{1,2,3}, {4,5}, {6,7}, {1,4}, {2,5,6,7}, {3,4,5,6,7}]
>>> solve_exact_cover(universe, subsets)
[(1, 2, 3), (4, 5), (6, 7)]
"""

from .solver import solve_exact_cover
from .solver_base import solve_exact_cover_base

__all__ = ["solve_exact_cover", "solve_exact_cover_base"]
__version__ = "1.0.0"
__author__ = "Santiago Emmanuel Jimenez Perez"
