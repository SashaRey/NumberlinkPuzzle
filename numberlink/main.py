import argparse

from numberlink.io.loader import load_text
from numberlink.io.parser import parse_puzzle
from numberlink.validation import validate_puzzle
from numberlink.geometry.factory import create_geometry
from numberlink.solver.backtracking import BacktrackingSolver
from numberlink.render import render_solution
from numberlink.exceptions import NumberlinkError


def build_parser():
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

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        text = load_text(args.path)
        puzzle = parse_puzzle(text)
        validate_puzzle(puzzle)

        geometry = create_geometry(puzzle)

        solver = BacktrackingSolver()
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
                render_solution(puzzle, solution)

    except FileNotFoundError:
        print(f"Ошибка: файл '{args.path}' не найден.")
    except NumberlinkError as error:
        print(f"Ошибка: {error}")
    except Exception as error:
        if args.debug:
            raise
        print(f"Непредвиденная ошибка: {error}")


if __name__ == "__main__":
    main()