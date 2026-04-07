import pytest

from numberlink.io.parser import parse_puzzle
from numberlink.exceptions import InputFormatError
from numberlink.domain.position import Position


def test_parse_valid_puzzle():
    text = """hex
A . .
. B .
A . B
"""
    puzzle = parse_puzzle(text)

    assert puzzle.geometry_type == "hex"
    assert puzzle.height == 3
    assert puzzle.width == 3
    assert puzzle.get_cell(Position(0, 0)) == "A"
    assert puzzle.get_cell(Position(1, 1)) == "B"
    assert puzzle.get_cell(Position(0, 1)) == "."


def test_parse_empty_input_raises_error():
    with pytest.raises(InputFormatError, match="пуст"):
        parse_puzzle("")


def test_parse_without_grid_raises_error():
    text = "hex"
    with pytest.raises(InputFormatError, match="Отсутствует поле"):
        parse_puzzle(text)


def test_parse_ragged_rows_raises_error():
    text = """hex
A .
. B .
"""
    with pytest.raises(InputFormatError, match="одинаковую длину"):
        parse_puzzle(text)


def test_parse_invalid_symbol_raises_error():
    text = """hex
A . .
. 1 .
A . B
"""
    with pytest.raises(InputFormatError, match="Недопустимый символ"):
        parse_puzzle(text)


def test_parse_trims_outer_whitespace():
    text = """

hex
A . .
. B .
A . B

"""
    puzzle = parse_puzzle(text)

    assert puzzle.geometry_type == "hex"
    assert puzzle.height == 3
    assert puzzle.width == 3