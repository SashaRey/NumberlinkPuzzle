import json
import tempfile
import unittest
from pathlib import Path

from numberlink.domain.position import Position
from numberlink.domain.puzzle import Puzzle
from numberlink.solver.cache import CachedSolver


class DummyIterSolver:
    def __init__(self, solutions):
        self._solutions = solutions
        self.calls = 0

    def iter_solutions(self, puzzle, geometry, max_solutions=None):
        self.calls += 1
        for index, solution in enumerate(self._solutions):
            if max_solutions is not None and index >= max_solutions:
                return
            yield solution


class TestCachedSolver(unittest.TestCase):
    def setUp(self):
        self.puzzle = Puzzle(
            cells={
                Position(0, 0): "A",
                Position(0, 1): "A",
            },
            height=1,
            width=2,
            geometry_type="hex",
        )
        self.geometry = object()
        self.solutions = [
            {"A": [Position(0, 0), Position(0, 1)]},
            {"A": [Position(0, 0), Position(0, 1)]},
        ]

    def test_iter_solutions_uses_cache_on_second_call(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            inner = DummyIterSolver(self.solutions)
            solver = CachedSolver(inner, cache_dir=temp_dir)

            first = list(solver.iter_solutions(self.puzzle, self.geometry))
            second = list(solver.iter_solutions(self.puzzle, self.geometry))

            self.assertEqual(first, self.solutions)
            self.assertEqual(second, self.solutions)
            self.assertEqual(inner.calls, 1)

    def test_iter_solutions_respects_max_solutions(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            inner = DummyIterSolver(self.solutions)
            solver = CachedSolver(inner, cache_dir=temp_dir)

            result = list(
                solver.iter_solutions(
                    self.puzzle,
                    self.geometry,
                    max_solutions=1,
                )
            )

            self.assertEqual(len(result), 1)

    def test_cache_file_contains_finished_marker_for_full_run(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            inner = DummyIterSolver(self.solutions)
            solver = CachedSolver(inner, cache_dir=temp_dir)

            list(solver.iter_solutions(self.puzzle, self.geometry))

            cache_key = solver._puzzle_key(self.puzzle)
            cache_path = Path(temp_dir) / f"{cache_key}.jsonl"
            lines = cache_path.read_text(encoding="utf-8").splitlines()

            self.assertTrue(lines)
            marker = json.loads(lines[-1])
            self.assertEqual(marker, {"__finished__": True})

    def test_solve_all_collects_results(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            inner = DummyIterSolver(self.solutions)
            solver = CachedSolver(inner, cache_dir=temp_dir)

            result = solver.solve_all(self.puzzle, self.geometry)

            self.assertEqual(result, self.solutions)


if __name__ == "__main__":
    unittest.main()
