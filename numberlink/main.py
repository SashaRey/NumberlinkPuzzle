from __future__ import annotations

import argparse

from numberlink.io.loader import load_text
from numberlink.io.parser import parse_puzzle
from numberlink.validation import validate_puzzle
from numberlink.geometry.factory import create_geometry
from numberlink.solver.backtracking import BacktrackingSolver
from numberlink.solver.cache import CachedSolver
from numberlink.render import render_solution, render_graph_solution
from numberlink.exceptions import NumberlinkError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Решатель головоломки Numberlink на шестиугольном поле."
    )

    parser.add_argument(
        "path",
        nargs="?",
        default="puzzle.txt",
        help="Путь к входному файлу с головоломкой (по умолчанию: puzzle.txt)",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Показывать подробный traceback при ошибках",
    )

    parser.add_argument(
        "--graph-view",
        action="store_true",
        help="Показывать решение как граф клеток и рёбер",
    )

    parser.add_argument(
        "--color",
        action="store_true",
        help="Включить цветной вывод",
    )

    parser.add_argument(
        "--max-solutions",
        type=int,
        default=None,
        help="Ограничить максимальное число найденных решений",
    )

    parser.add_argument(
        "--cache",
        action="store_true",
        help="Использовать кэширование решений",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        max_solutions = getattr(args, "max_solutions", None)
        graph_view = getattr(args, "graph_view", False)
        color = getattr(args, "color", False)
        use_cache = getattr(args, "cache", False)

        if max_solutions is not None and max_solutions <= 0:
            raise NumberlinkError(
                "Параметр --max-solutions должен быть положительным числом."
            )

        text = load_text(args.path)
        puzzle = parse_puzzle(text)
        validate_puzzle(puzzle)

        geometry = create_geometry(puzzle)
        solver = BacktrackingSolver()

        if use_cache:
            solver = CachedSolver(solver)

        render_fn = render_graph_solution if graph_view else render_solution

        # Совместимость со старым API и существующими тестовыми заглушками.
        if hasattr(solver, "solve_all") and max_solutions is None:
            solutions = solver.solve_all(puzzle, geometry)

            if not solutions:
                print("Решений не найдено")
            else:
                count = len(solutions)
                if count == 1:
                    print("Найдено 1 решение:")
                else:
                    print(f"Найдено {count} решений:")

                for i, solution in enumerate(solutions, start=1):
                    print(f"Решение {i}:")
                    try:
                        render_fn(puzzle, solution, color=color)
                    except TypeError:
                        render_fn(puzzle, solution)
            return

        printed_count = 0
        for printed_count, solution in enumerate(
            solver.iter_solutions(
                puzzle,
                geometry,
                max_solutions=max_solutions,
            ),
            start=1,
        ):
            if printed_count == 1:
                if max_solutions is None:
                    print("Найдены решения:")
                else:
                    max_sol = max_solutions
                    print(f"Найдены решения (показано не более {max_sol}):")

            print(f"Решение {printed_count}:")
            try:
                render_fn(puzzle, solution, color=color)
            except TypeError:
                render_fn(puzzle, solution)

        if printed_count == 0:
            print("Решений не найдено")
        else:
            print(f"Всего выведено решений: {printed_count}")

    except FileNotFoundError:
        print(f"Ошибка: файл '{args.path}' не найден.")
    except NumberlinkError as error:
        print(f"Ошибка: {error}")
    except Exception as error:
        if getattr(args, "debug", False):
            raise
        print(f"Непредвиденная ошибка: {error}")


if __name__ == "__main__":
    main()
