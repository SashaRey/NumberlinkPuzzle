from numberlink.io.loader import load_text
from numberlink.io.parser import parse_puzzle
from numberlink.validation import validate_puzzle
from numberlink.geometry.factory import create_geometry
from numberlink.solver.backtracking import BacktrackingSolver

def main():
    text = load_text("puzzle.txt")

    puzzle = parse_puzzle(text)
    validate_puzzle(puzzle)

    geometry = create_geometry(puzzle)

    solver = BacktrackingSolver()
    solutions = solver.solve_all(puzzle, geometry)

    if not solutions:
        print("Решений не найдено")
    else:
        print(f"Найдено {len(solutions)} решений:")
        for solution in solutions:
            print(solution)

if __name__ == "__main__":    main()