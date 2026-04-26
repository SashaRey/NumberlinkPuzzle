import io
import unittest
from contextlib import redirect_stdout

from numberlink.domain.position import Position
from numberlink.domain.puzzle import Puzzle
from numberlink import render as render_module


class TestRender(unittest.TestCase):
    def test_render_solution_prints_grid(self):
        puzzle = Puzzle(
            cells={
                Position(0, 0): "A",
                Position(0, 1): ".",
                Position(1, 0): ".",
                Position(1, 1): "A",
            },
            height=2,
            width=2,
            geometry_type="hex",
        )

        solution = {
            "A": [Position(0, 0), Position(0, 1), Position(1, 1)],
        }

        stream = io.StringIO()
        with redirect_stdout(stream):
            render_module.render_solution(puzzle, solution)

        output_lines = stream.getvalue().strip().splitlines()
        self.assertEqual(output_lines[0], "A a")
        self.assertEqual(output_lines[1], " . A")

    def test_render_solution_with_color_contains_ansi(self):
        puzzle = Puzzle(
            cells={
                Position(0, 0): "A",
                Position(0, 1): ".",
            },
            height=1,
            width=2,
            geometry_type="hex",
        )
        solution = {"A": [Position(0, 0), Position(0, 1)]}

        stream = io.StringIO()
        with redirect_stdout(stream):
            render_module.render_solution(puzzle, solution, color=True)

        output = stream.getvalue()
        self.assertIn("\033[", output)

    def test_render_graph_solution_draws_path_and_wall(self):
        p00 = Position(0, 0)
        p01 = Position(0, 1)
        p10 = Position(1, 0)
        p11 = Position(1, 1)
        wall = frozenset({p01, p11})

        puzzle = Puzzle(
            cells={
                p00: "A",
                p01: ".",
                p10: ".",
                p11: "A",
            },
            height=2,
            width=2,
            geometry_type="hex",
            walls=frozenset({wall}),
        )
        solution = {"A": [p00, p01, p10]}

        stream = io.StringIO()
        with redirect_stdout(stream):
            render_module.render_graph_solution(puzzle, solution)

        output = stream.getvalue()
        self.assertIn("[A]", output)
        self.assertIn("===", output)
        self.assertIn("X", output)

    def test_horizontal_and_diagonal_helpers_cover_all_branches(self):
        p1 = Position(0, 0)
        p2 = Position(0, 1)
        edge = frozenset({p1, p2})
        color_map = {"A": "\\033[92m"}

        text_path = render_module._horizontal_edge_text(
            edge,
            {edge},
            {edge: "A"},
            set(),
            False,
            color_map,
        )
        self.assertEqual(text_path, "=== ")

        text_wall = render_module._horizontal_edge_text(
            edge,
            set(),
            {},
            {edge},
            False,
            color_map,
        )
        self.assertEqual(text_wall, " X  ")

        text_empty = render_module._horizontal_edge_text(
            edge,
            set(),
            {},
            set(),
            False,
            color_map,
        )
        self.assertEqual(text_empty, "    ")

        diag_short = render_module._diagonal_edge_text(
            frozenset({p1}),
            set(),
            {},
            set(),
            False,
            color_map,
            "/",
        )
        self.assertEqual(diag_short, " ")

        diag_path = render_module._diagonal_edge_text(
            edge,
            {edge},
            {edge: "A"},
            set(),
            False,
            color_map,
            "/",
        )
        self.assertEqual(diag_path, "/")

        diag_wall = render_module._diagonal_edge_text(
            edge,
            set(),
            {},
            {edge},
            False,
            color_map,
            "/",
        )
        self.assertEqual(diag_wall, "X")


if __name__ == "__main__":
    unittest.main()
