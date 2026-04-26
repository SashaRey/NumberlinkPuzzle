import unittest

from numberlink.domain.position import Position
from numberlink.file_io.parser import parse_puzzle
from numberlink.geometry.factory import create_geometry
from numberlink.solver.backtracking import BacktrackingSolver


class TestSolver(unittest.TestCase):
    def _solve(self, text):
        puzzle = parse_puzzle(text)
        geometry = create_geometry(puzzle)
        solver = BacktrackingSolver()
        return solver.solve_all(puzzle, geometry)

    def test_solver_finds_at_least_one_solution_for_simple_puzzle(self):
        text = """hex
A . .
. B .
A . B
"""
        solutions = self._solve(text)
        self.assertGreaterEqual(len(solutions), 1)

    def test_solver_returns_list(self):
        text = """hex
A . .
. B .
A . B
"""
        solutions = self._solve(text)
        self.assertIsInstance(solutions, list)

    def test_every_solution_contains_correct_endpoints(self):
        text = """hex
A . .
. B .
A . B
"""
        solutions = self._solve(text)

        self.assertTrue(solutions)
        for solution in solutions:
            self.assertIn("A", solution)
            self.assertIn("B", solution)

            self.assertEqual(solution["A"][0], Position(0, 0))
            self.assertEqual(solution["A"][-1], Position(2, 0))

            self.assertEqual(solution["B"][0], Position(1, 1))
            self.assertEqual(solution["B"][-1], Position(2, 2))

    def test_solver_returns_empty_list_for_unsolvable_puzzle(self):
        text = """hex
A B
B A
"""
        solutions = self._solve(text)
        self.assertEqual(solutions, [])


if __name__ == "__main__":
    unittest.main()
