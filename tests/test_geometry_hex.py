from numberlink.domain.position import Position
from numberlink.domain.puzzle import Puzzle
from numberlink.geometry.hex import HexGeometry


def make_puzzle_3x3():
    cells = {}
    for row in range(3):
        for col in range(3):
            cells[Position(row, col)] = "."
    return Puzzle(cells=cells, height=3, width=3, geometry_type="hex")


def test_contains_returns_true_for_existing_cell():
    """Проверяет, что contains возвращает True для существующей ячейки."""
    puzzle = make_puzzle_3x3()
    geometry = HexGeometry(puzzle)

    assert geometry.contains(Position(1, 1)) is True


def test_contains_returns_false_for_missing_cell():
    """Проверяет, что contains возвращает False для несуществующей ячейки."""
    puzzle = make_puzzle_3x3()
    geometry = HexGeometry(puzzle)

    assert geometry.contains(Position(5, 5)) is False


def test_neighbors_for_top_left_corner():
    """Проверяет соседей для верхнего левого угла."""
    puzzle = make_puzzle_3x3()
    geometry = HexGeometry(puzzle)

    neighbors = geometry.neighbors(Position(0, 0))

    assert neighbors == [
        Position(0, 1),
        Position(1, 0),
    ]


def test_neighbors_for_center_cell():
    """Проверяет соседей для центральной ячейки."""
    puzzle = make_puzzle_3x3()
    geometry = HexGeometry(puzzle)

    neighbors = geometry.neighbors(Position(1, 1))

    assert neighbors == [
        Position(0, 1),
        Position(0, 2),
        Position(1, 2),
        Position(2, 1),
        Position(2, 0),
        Position(1, 0),
    ]