"""
tests/test_exact_cover.py
=========================
Suite de pruebas unitarias para los algoritmos Exact Cover.

Cubre:
  - Casos base / triviales
  - Casos de borde (universo vacío, sin solución, subconjunto único)
  - Casos de estrés moderado
  - Validación de resultados (correctitud matemática)
  - Equivalencia entre Programa 1 y Programa 2

Ejecutar con:
    pytest tests/ -v
"""

import pytest
from exact_cover import solve_exact_cover, solve_exact_cover_base

# Utilidad de validación

def is_valid_exact_cover(universe, solution):
    """Verifica matemáticamente que la solución es una partición exacta."""
    if solution is None:
        return False
    covered = []
    for subset in solution:
        covered.extend(subset)
    return sorted(covered) == sorted(universe)


# Caso Trivial

class TestTrivialCase:
    """Caso pequeño """

    universe = [1, 2, 3, 4, 5, 6, 7]
    subsets  = [{1, 2, 3}, {4, 5}, {6, 7}, {1, 4}, {2, 5, 6, 7}, {3, 4, 5, 6, 7}]
    expected = [(1, 2, 3), (4, 5), (6, 7)]

    def test_optimized_finds_solution(self):
        result = solve_exact_cover(self.universe, self.subsets)
        assert result is not None, "Debe encontrar solución en el caso trivial"

    def test_optimized_result_is_correct(self):
        result = solve_exact_cover(self.universe, self.subsets)
        assert is_valid_exact_cover(self.universe, result)

    def test_base_finds_solution(self):
        result = solve_exact_cover_base(self.universe, self.subsets)
        assert result is not None

    def test_base_result_is_correct(self):
        result = solve_exact_cover_base(self.universe, self.subsets)
        assert is_valid_exact_cover(self.universe, result)

    def test_both_programs_agree(self):
        r1 = solve_exact_cover_base(self.universe, self.subsets)
        r2 = solve_exact_cover(self.universe, self.subsets)
        assert is_valid_exact_cover(self.universe, r1)
        assert is_valid_exact_cover(self.universe, r2)

# Casos de borde

class TestEdgeCases:

    def test_empty_universe(self):
        """Un universo vacío ya está cubierto la solución es la lista vacía."""
        result = solve_exact_cover([], [])
        assert result == []

    def test_single_subset_solution(self):
        """Un único subconjunto que es igual al universo."""
        result = solve_exact_cover([1, 2, 3], [{1, 2, 3}])
        assert is_valid_exact_cover([1, 2, 3], result)

    def test_no_solution_exists(self):
        """Cuando no existe cobertura exacta, debe regresar None."""
        result = solve_exact_cover([1, 2, 3], [{1, 2}, {2, 3}])
        assert result is None

    def test_no_solution_base(self):
        result = solve_exact_cover_base([1, 2, 3], [{1, 2}, {2, 3}])
        assert result is None

    def test_incomplete_coverage(self):
        """Subconjuntos que no cubren todo el universo."""
        result = solve_exact_cover([1, 2, 3], [{1}, {2}])
        assert result is None

    def test_overlapping_only(self):
        """Todos los subconjuntos se solapan no hay solución."""
        result = solve_exact_cover([1, 2, 3], [{1, 2}, {1}])
        assert result is None

    def test_single_element_universe(self):
        result = solve_exact_cover([42], [{42}])
        assert is_valid_exact_cover([42], result)

    def test_returns_sorted_tuples(self):
        """El resultado debe ser una lista de tuplas ordenadas."""
        result = solve_exact_cover([1, 2, 3], [{3, 1, 2}])
        assert result == [(1, 2, 3)]

# Validación de resultados (correctitud matemática)

class TestMathematicalCorrectness:
    """Verifica las propiedades formales de la cobertura exacta."""

    def test_union_equals_universe(self):
        universe = list(range(1, 11))
        subsets  = [{1,2,3,4,5}, {6,7,8,9,10}]
        result   = solve_exact_cover(universe, subsets)
        assert result is not None
        covered = set()
        for s in result:
            covered |= set(s)
        assert covered == set(universe)

    def test_pairwise_disjoint(self):
        universe = list(range(1, 11))
        subsets  = [{1,2,3,4,5}, {6,7,8,9,10}]
        result   = solve_exact_cover(universe, subsets)
        assert result is not None
        for i in range(len(result)):
            for j in range(i + 1, len(result)):
                assert set(result[i]).isdisjoint(set(result[j])), \
                    f"Subconjuntos {result[i]} y {result[j]} se solapan"

    def test_exact_3_cover_small(self):
        """Exact 3-Cover: cada subconjunto tiene exactamente 3 elementos."""
        universe = [1, 2, 3, 4, 5, 6]
        subsets  = [{1,2,3}, {4,5,6}, {1,4,7}, {2,5,6}]
        result   = solve_exact_cover(universe, subsets)
        if result is not None:
            assert is_valid_exact_cover(universe, result)


# Prueba de estrés moderada

class TestStressCase:
    """Base de datos moderado para medir capacidad de respuesta."""

    def test_stress_with_solution(self):
        """30 subconjuntos, universo de tamaño 30, con solución garantizada."""
        import random
        random.seed(42)
        universe = list(range(30))
        # Solución conocida: grupos de 5
        known_solution = [set(range(i, i + 5)) for i in range(0, 30, 5)]
        # Subconjuntos adicionales que se solapan (ruido)
        noise = [set(random.sample(universe, 3)) for _ in range(376)]
        subsets = known_solution + noise
        random.shuffle(subsets)

        result = solve_exact_cover(universe, subsets)
        assert result is not None
        assert is_valid_exact_cover(universe, result)

    def test_poisoned_dataset_no_solution(self):
        """30 000 conjuntos 'basura' que no forman cobertura exacta."""
        import random
        random.seed(7)
        universe = list(range(1, 13))
        # Generamos subconjuntos que siempre se solapan entre sí
        subsets = []
        for _ in range(30_000):
            size = random.randint(2, 4)
            subsets.append(set(random.sample(universe, size)))
        # Nos aseguramos de que no exista solución quitando el elemento 12
        subsets = [s - {12} for s in subsets]

        result = solve_exact_cover(universe, subsets)
        # Con el elemento 12 faltante, no puede existir cobertura exacta
        assert result is None
