from parser import parse_puzzle
from exceptions import InputFormatError, InvalidPuzzleError
import pytest

def test_parse_valid_puzzle():
    text = """4 4
    A..B
    ....
    ....
    A..B"""

    board = parse_puzzle(text)
    assert board.height == 4
    assert board.width == 4
    assert board.get_cell(0, 0) == 'A'
    assert board.get_cell(0, 3) == 'B'
    assert board.get_cell(1, 1) == '.'

def test_parse_empty_input():
    with pytest.raises(InputFormatError):
        parse_puzzle("")

def test_invalid_header():
    text = """4
    A..B
    ....
    ....
    A..B"""
    with pytest.raises(InputFormatError):
        parse_puzzle(text)

def test_non_integer_dimensions():
    text = """x y
    A..B
    ....
    ....
    A..B"""
    with pytest.raises(InputFormatError):
        parse_puzzle(text)

def test_negative_dimensions():
    text = """-4 -4
    A..B
    ....
    ....
    A..B"""
    with pytest.raises(InputFormatError):
        parse_puzzle(text)

def test_invalid_symbol():
    text = """4 4
    A..B
    ....
    ..@.
    A..B"""
    with pytest.raises(InputFormatError):
        parse_puzzle(text)

def test_label_appears_once():
    text = """4 4
    A..B
    ....
    ....
    A..C"""
    with pytest.raises(InvalidPuzzleError):
        parse_puzzle(text)

def test_label_appears_more_than_twice():
    text = """4 4
    A..B
    ....
    ....
    A..A"""
    with pytest.raises(InvalidPuzzleError):
        parse_puzzle(text)

def test_wrong_number_of_rows():
    text = """4 4
    A..B
    ....
    A..B"""
    with pytest.raises(InputFormatError):
        parse_puzzle(text)

def test_wrong_row_length():
    text = """4 4
    A..B
    .....
    ....
    A..B"""
    with pytest.raises(InputFormatError):
        parse_puzzle(text)