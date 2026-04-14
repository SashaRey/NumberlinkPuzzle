import pytest

from numberlink.domain.position import Position
from numberlink.domain.puzzle import Puzzle
from numberlink.exceptions import InvalidPuzzleError
from numberlink.validation import validate_puzzle


def make_puzzle(cells, height=3, width=3, geometry_type="hex"):
    """Вспомогательная функция для создания головоломки с заданными параметрами."""
    return Puzzle(
        cells=cells,
        height=height,
        width=width,
        geometry_type=geometry_type,
    )


def test_validate_correct_puzzle_passes():
    """Проверяем, что корректная головоломка проходит валидацию без ошибок."""
    puzzle = make_puzzle(
        {
            Position(0, 0): "A",
            Position(0, 1): ".",
            Position(0, 2): ".",
            Position(1, 0): ".",
            Position(1, 1): "B",
            Position(1, 2): ".",
            Position(2, 0): "A",
            Position(2, 1): ".",
            Position(2, 2): "B",
        }
    )

    validate_puzzle(puzzle)


def test_validate_empty_field_raises_error():
    """Проверяем, что пустое поле вызывает ошибку валидации."""
    puzzle = make_puzzle({}, height=0, width=0)

    with pytest.raises(InvalidPuzzleError, match="Поле пустое"):
        validate_puzzle(puzzle)


def test_validate_unsupported_geometry_raises_error():
    """Проверяем, что неподдерживаемая геометрия вызывает ошибку валидации."""
    puzzle = make_puzzle(
        {
            Position(0, 0): "A",
            Position(0, 1): "A",
        },
        height=1,
        width=2,
        geometry_type="square",
    )

    with pytest.raises(InvalidPuzzleError, match="Неподдерживаемая геометрия"):
        validate_puzzle(puzzle)


def test_validate_no_pairs_raises_error():
    """Проверяем, что отсутствие пар вызывает ошибку валидации."""
    puzzle = make_puzzle(
        {
            Position(0, 0): ".",
            Position(0, 1): ".",
            Position(1, 0): ".",
            Position(1, 1): ".",
        },
        height=2,
        width=2,
    )

    with pytest.raises(InvalidPuzzleError, match="нет ни одной пары"):
        validate_puzzle(puzzle)


def test_validate_label_occurs_once_raises_error():
    """Проверяем, что метка, которая встречается 1 раз, вызывает ошибку валидации."""
    puzzle = make_puzzle(
        {
            Position(0, 0): "A",
            Position(0, 1): ".",
            Position(1, 0): ".",
            Position(1, 1): ".",
        },
        height=2,
        width=2,
    )

    with pytest.raises(InvalidPuzzleError, match="ровно 2 раза"):
        validate_puzzle(puzzle)


def test_validate_label_occurs_three_times_raises_error():
    """Проверяем, что метка, которая встречается 3 раза, вызывает ошибку валидации."""
    puzzle = make_puzzle(
        {
            Position(0, 0): "A",
            Position(0, 1): "A",
            Position(1, 0): "A",
            Position(1, 1): ".",
        },
        height=2,
        width=2,
    )

    with pytest.raises(InvalidPuzzleError, match="ровно 2 раза"):
        validate_puzzle(puzzle)
