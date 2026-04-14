# import sys
# from numberlink.io.loader import load_text
# from numberlink.io.parser import parse_puzzle
# from numberlink.validation import validate_puzzle
# from numberlink.geometry.factory import create_geometry
# from numberlink.solver.backtracking import BacktrackingSolver
# from render import render_solution

# def main():
#     path = sys.argv[1] if len(sys.argv) > 1 else "puzzle.txt"

#     text = load_text(path)
#     puzzle = parse_puzzle(text)
#     validate_puzzle(puzzle)
#     geometry = create_geometry(puzzle)

#     solver = BacktrackingSolver()
#     solutions = solver.solve_all(puzzle, geometry)

#     if not solutions:
#         print("Решений не найдено")
#     else:
#         print(f"Найдено {len(solutions)} решений:")
#         for i, solution in enumerate(solutions, start=1):
#             print(f"Решение {i}:")
#             render_solution(puzzle, solution)
