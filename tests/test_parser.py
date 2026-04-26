import unittest

from numberlink.domain.position import Position
from numberlink.exceptions import InputFormatError
from numberlink.file_io.parser import parse_puzzle


class TestParser(unittest.TestCase):
    def test_parse_valid_puzzle(self):
        text = """hex
A . .
. B .
A . B
"""
        puzzle = parse_puzzle(text)

        self.assertEqual(puzzle.geometry_type, "hex")
        self.assertEqual(puzzle.height, 3)
        self.assertEqual(puzzle.width, 3)
        self.assertEqual(puzzle.get_cell(Position(0, 0)), "A")
        self.assertEqual(puzzle.get_cell(Position(1, 1)), "B")
        self.assertEqual(puzzle.get_cell(Position(0, 1)), ".")

    def test_parse_empty_input_raises_error(self):
        with self.assertRaisesRegex(InputFormatError, "пуст"):
            parse_puzzle("")

    def test_parse_without_grid_raises_error(self):
        with self.assertRaisesRegex(InputFormatError, "Отсутствует поле"):
            parse_puzzle("hex")

    def test_parse_ragged_rows_raises_error(self):
        text = """hex
A .
. B .
"""
        with self.assertRaisesRegex(InputFormatError, "одинаковую длину"):
            parse_puzzle(text)

    def test_parse_invalid_symbol_raises_error(self):
        text = """hex
A . .
. 1 .
A . B
"""
        with self.assertRaisesRegex(InputFormatError, "Недопустимый символ"):
            parse_puzzle(text)

    def test_parse_trims_outer_whitespace(self):
        text = """

hex
A . .
. B .
A . B

"""
        puzzle = parse_puzzle(text)

        self.assertEqual(puzzle.geometry_type, "hex")
        self.assertEqual(puzzle.height, 3)
        self.assertEqual(puzzle.width, 3)


if __name__ == "__main__":
    unittest.main()
