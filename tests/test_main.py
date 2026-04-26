import io
import types
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from numberlink import main as main_module
from numberlink.exceptions import NumberlinkError


class DummySolverWithSolution:
    def solve_all(self, puzzle, geometry):
        """Возвращает фиктивное решение для тестирования."""
        return [{"A": ["dummy-path"]}]


class DummySolverWithoutSolution:
    def solve_all(self, puzzle, geometry):
        """Возвращает пустой список, имитируя отсутствие решений."""
        return []


class DummyParser:
    def __init__(
        self,
        path,
        debug=False,
        gui=False,
        graph_view=False,
        color=False,
        max_solutions=None,
        cache=False,
    ):
        self._path = path
        self._debug = debug
        self._gui = gui
        self._graph_view = graph_view
        self._color = color
        self._max_solutions = max_solutions
        self._cache = cache

    def parse_args(self):
        return type(
            "Args",
            (),
            {
                "path": self._path,
                "debug": self._debug,
                "gui": self._gui,
                "graph_view": self._graph_view,
                "color": self._color,
                "max_solutions": self._max_solutions,
                "cache": self._cache,
            },
        )()


class DummyIterOnlySolver:
    def iter_solutions(self, puzzle, geometry, max_solutions=None):
        yield {"A": ["iter-path"]}


class DummyCachedSolverWithSolveAll:
    def solve_all(self, puzzle, geometry):
        return [{"A": ["cached"]}]


class TestMain(unittest.TestCase):
    def test_build_parser_parses_optional_flags(self):
        parser = main_module.build_parser()

        args = parser.parse_args(
            [
                "input.txt",
                "--debug",
                "--graph-view",
                "--color",
                "--max-solutions",
                "2",
                "--cache",
            ]
        )

        self.assertEqual(args.path, "input.txt")
        self.assertTrue(args.debug)
        self.assertTrue(args.graph_view)
        self.assertTrue(args.color)
        self.assertEqual(args.max_solutions, 2)
        self.assertTrue(args.cache)

    def test_main_prints_found_solution(self):
        with (
            patch.object(main_module, "load_text", lambda path: "text"),
            patch.object(main_module, "parse_puzzle", lambda text: "puzzle"),
            patch.object(
                main_module,
                "validate_puzzle",
                lambda puzzle: None,
            ),
            patch.object(
                main_module,
                "create_geometry",
                lambda puzzle: "geometry",
            ),
            patch.object(
                main_module,
                "BacktrackingSolver",
                lambda: DummySolverWithSolution(),
            ),
            patch.object(
                main_module,
                "render_solution",
                lambda puzzle, solution: print("RENDERED"),
            ),
            patch.object(
                main_module,
                "build_parser",
                lambda: DummyParser("puzzle.txt"),
            ),
        ):
            stream = io.StringIO()
            with redirect_stdout(stream):
                main_module.main()

        output = stream.getvalue()
        self.assertIn("Найдено 1 решение", output)
        self.assertIn("Решение 1:", output)
        self.assertIn("RENDERED", output)

    def test_main_prints_no_solution(self):
        with (
            patch.object(main_module, "load_text", lambda path: "text"),
            patch.object(main_module, "parse_puzzle", lambda text: "puzzle"),
            patch.object(
                main_module,
                "validate_puzzle",
                lambda puzzle: None,
            ),
            patch.object(
                main_module,
                "create_geometry",
                lambda puzzle: "geometry",
            ),
            patch.object(
                main_module,
                "BacktrackingSolver",
                lambda: DummySolverWithoutSolution(),
            ),
            patch.object(
                main_module,
                "render_solution",
                lambda puzzle, solution: None,
            ),
            patch.object(
                main_module,
                "build_parser",
                lambda: DummyParser("puzzle.txt"),
            ),
        ):
            stream = io.StringIO()
            with redirect_stdout(stream):
                main_module.main()

        output = stream.getvalue()
        self.assertIn("Решений не найдено", output)

    def test_main_handles_file_not_found(self):
        def raise_file_not_found(path):
            raise FileNotFoundError

        with (
            patch.object(main_module, "load_text", raise_file_not_found),
            patch.object(
                main_module,
                "build_parser",
                lambda: DummyParser("missing.txt"),
            ),
        ):
            stream = io.StringIO()
            with redirect_stdout(stream):
                main_module.main()

        output = stream.getvalue()
        self.assertIn("не найден", output)

    def test_main_handles_numberlink_error(self):
        def raise_numberlink_error(text):
            raise NumberlinkError("bad puzzle")

        with (
            patch.object(main_module, "load_text", lambda path: "text"),
            patch.object(main_module, "parse_puzzle", raise_numberlink_error),
            patch.object(
                main_module,
                "build_parser",
                lambda: DummyParser("puzzle.txt"),
            ),
        ):
            stream = io.StringIO()
            with redirect_stdout(stream):
                main_module.main()

        output = stream.getvalue()
        self.assertIn("Ошибка: bad puzzle", output)

    def test_main_rejects_non_positive_max_solutions(self):
        with patch.object(
            main_module,
            "build_parser",
            lambda: DummyParser("puzzle.txt", max_solutions=0),
        ):
            stream = io.StringIO()
            with redirect_stdout(stream):
                main_module.main()

        output = stream.getvalue()
        self.assertIn("должен быть положительным", output)

    def test_main_uses_iter_solutions_when_max_solutions_is_set(self):
        with (
            patch.object(main_module, "load_text", lambda path: "text"),
            patch.object(main_module, "parse_puzzle", lambda text: "puzzle"),
            patch.object(main_module, "validate_puzzle", lambda puzzle: None),
            patch.object(
                main_module,
                "create_geometry",
                lambda puzzle: "geometry",
            ),
            patch.object(
                main_module,
                "BacktrackingSolver",
                lambda: DummyIterOnlySolver(),
            ),
            patch.object(
                main_module,
                "render_solution",
                lambda puzzle, solution, color=False: None,
            ),
            patch.object(
                main_module,
                "build_parser",
                lambda: DummyParser("puzzle.txt", max_solutions=1),
            ),
        ):
            stream = io.StringIO()
            with redirect_stdout(stream):
                main_module.main()

        output = stream.getvalue()
        self.assertIn("показано не более 1", output)
        self.assertIn("Всего выведено решений: 1", output)

    def test_main_uses_cached_solver_when_cache_flag_set(self):
        with (
            patch.object(main_module, "load_text", lambda path: "text"),
            patch.object(main_module, "parse_puzzle", lambda text: "puzzle"),
            patch.object(main_module, "validate_puzzle", lambda puzzle: None),
            patch.object(
                main_module,
                "create_geometry",
                lambda puzzle: "geometry",
            ),
            patch.object(
                main_module,
                "BacktrackingSolver",
                lambda: DummySolverWithSolution(),
            ),
            patch.object(
                main_module,
                "CachedSolver",
                lambda solver: DummyCachedSolverWithSolveAll(),
            ),
            patch.object(
                main_module,
                "render_solution",
                lambda puzzle, solution: print("CACHED"),
            ),
            patch.object(
                main_module,
                "build_parser",
                lambda: DummyParser("puzzle.txt", cache=True),
            ),
        ):
            stream = io.StringIO()
            with redirect_stdout(stream):
                main_module.main()

        output = stream.getvalue()
        self.assertIn("CACHED", output)

    def test_main_uses_graph_renderer_and_falls_back_without_color_kw(self):
        def graph_renderer_without_color(puzzle, solution):
            print("GRAPH")

        with (
            patch.object(main_module, "load_text", lambda path: "text"),
            patch.object(main_module, "parse_puzzle", lambda text: "puzzle"),
            patch.object(main_module, "validate_puzzle", lambda puzzle: None),
            patch.object(
                main_module,
                "create_geometry",
                lambda puzzle: "geometry",
            ),
            patch.object(
                main_module,
                "BacktrackingSolver",
                lambda: DummySolverWithSolution(),
            ),
            patch.object(
                main_module,
                "render_graph_solution",
                graph_renderer_without_color,
            ),
            patch.object(
                main_module,
                "build_parser",
                lambda: DummyParser(
                    "puzzle.txt",
                    graph_view=True,
                    color=True,
                ),
            ),
        ):
            stream = io.StringIO()
            with redirect_stdout(stream):
                main_module.main()

        output = stream.getvalue()
        self.assertIn("GRAPH", output)

    def test_main_gui_mode_runs_app(self):
        fake_module = types.ModuleType("numberlink.gui.app")
        fake_module.run = lambda: "GUI_OK"

        with (
            patch.dict("sys.modules", {"numberlink.gui.app": fake_module}),
            patch.object(
                main_module,
                "build_parser",
                lambda: DummyParser("puzzle.txt", gui=True),
            ),
        ):
            result = main_module.main()

        self.assertEqual(result, "GUI_OK")

    def test_main_gui_mode_prints_message_on_import_error(self):
        original_import = __import__

        def import_with_error(name, *args, **kwargs):
            if name == "numberlink.gui.app":
                raise ImportError("No module named PyQt6")
            return original_import(name, *args, **kwargs)

        with (
            patch("builtins.__import__", side_effect=import_with_error),
            patch.object(
                main_module,
                "build_parser",
                lambda: DummyParser("puzzle.txt", gui=True),
            ),
        ):
            stream = io.StringIO()
            with redirect_stdout(stream):
                main_module.main()

        output = stream.getvalue()
        self.assertIn("PyQt6", output)

    def test_main_raises_unexpected_error_in_debug_mode(self):
        with (
            patch.object(
                main_module,
                "load_text",
                lambda path: (_ for _ in ()).throw(RuntimeError("boom")),
            ),
            patch.object(
                main_module,
                "build_parser",
                lambda: DummyParser("puzzle.txt", debug=True),
            ),
        ):
            with self.assertRaises(RuntimeError):
                main_module.main()

    def test_main_prints_unexpected_error_in_non_debug_mode(self):
        with (
            patch.object(
                main_module,
                "load_text",
                lambda path: (_ for _ in ()).throw(RuntimeError("boom")),
            ),
            patch.object(
                main_module,
                "build_parser",
                lambda: DummyParser("puzzle.txt", debug=False),
            ),
        ):
            stream = io.StringIO()
            with redirect_stdout(stream):
                main_module.main()

        output = stream.getvalue()
        self.assertIn("Непредвиденная ошибка", output)


if __name__ == "__main__":
    unittest.main()
