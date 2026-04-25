from numberlink.domain.position import Position
from numberlink.file_io.parser import parse_puzzle
from numberlink.geometry.factory import create_geometry
from numberlink.solver.backtracking import BacktrackingSolver


def test_solver_finds_at_least_one_solution_for_simple_puzzle():
    text = """hex
A . .
. B .
A . B
"""
    puzzle = parse_puzzle(text)
    geometry = create_geometry(puzzle)
    solver = BacktrackingSolver()

    solutions = solver.solve_all(puzzle, geometry)

    assert len(solutions) >= 1


def test_solver_returns_list():
    text = """hex
A . .
. B .
A . B
"""
    puzzle = parse_puzzle(text)
    geometry = create_geometry(puzzle)
    solver = BacktrackingSolver()

    solutions = solver.solve_all(puzzle, geometry)

    assert isinstance(solutions, list)


def test_every_solution_contains_correct_endpoints():
    text = """hex
A . .
. B .
A . B
"""
    puzzle = parse_puzzle(text)
    geometry = create_geometry(puzzle)
    solver = BacktrackingSolver()

    solutions = solver.solve_all(puzzle, geometry)

    assert solutions

    for solution in solutions:
        assert "A" in solution
        assert "B" in solution

        assert solution["A"][0] == Position(0, 0)
        assert solution["A"][-1] == Position(2, 0)

        assert solution["B"][0] == Position(1, 1)
        assert solution["B"][-1] == Position(2, 2)


def test_solver_returns_empty_list_for_unsolvable_puzzle():
    text = """hex
A B
B A
"""
    puzzle = parse_puzzle(text)
    geometry = create_geometry(puzzle)
    solver = BacktrackingSolver()

    solutions = solver.solve_all(puzzle, geometry)

    assert solutions == []


from numberlink.domain.position import Position
from numberlink.file_io.parser import parse_puzzle
from numberlink.geometry.factory import create_geometry
from numberlink.solver.backtracking import BacktrackingSolver


def test_solver_finds_at_least_one_solution_for_simple_puzzle():
    """Проверяем, что для простой головоломки метод solve_all находит хотя бы одно решение."""
    text = """hex
A . .
. B .
A . B
"""
    puzzle = parse_puzzle(text)
    geometry = create_geometry(puzzle)
    solver = BacktrackingSolver()

    solutions = solver.solve_all(puzzle, geometry)

    assert len(solutions) >= 1


def test_solver_returns_list():
    """Проверяем, что метод solve_all возвращает список решений."""
    text = """hex
A . .
. B .
A . B
"""
    puzzle = parse_puzzle(text)
    geometry = create_geometry(puzzle)
    solver = BacktrackingSolver()

    solutions = solver.solve_all(puzzle, geometry)

    assert isinstance(solutions, list)


def test_every_solution_contains_correct_endpoints():
    """Проверяем, что каждый найденный решением содержит правильные начальные и конечные позиции для каждой буквы."""
    text = """hex
A . .
. B .
A . B
"""
    puzzle = parse_puzzle(text)
    geometry = create_geometry(puzzle)
    solver = BacktrackingSolver()

    solutions = solver.solve_all(puzzle, geometry)

    assert solutions

    for solution in solutions:
        assert "A" in solution
        assert "B" in solution

        assert solution["A"][0] == Position(0, 0)
        assert solution["A"][-1] == Position(2, 0)

        assert solution["B"][0] == Position(1, 1)
        assert solution["B"][-1] == Position(2, 2)


def test_solver_returns_empty_list_for_unsolvable_puzzle():
    """Проверяем, что для головоломки, которая не имеет решения, метод solve_all возвращает пустой список."""
    text = """hex
A B
B A
"""
    puzzle = parse_puzzle(text)
    geometry = create_geometry(puzzle)
    solver = BacktrackingSolver()

    solutions = solver.solve_all(puzzle, geometry)

    assert solutions == []
