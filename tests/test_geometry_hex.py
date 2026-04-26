import unittest

from numberlink.domain.position import Position
from numberlink.domain.puzzle import Puzzle
from numberlink.geometry.hex import HexGeometry


def make_puzzle_3x3():
    cells = {}
    for row in range(3):
        for col in range(3):
            cells[Position(row, col)] = "."
    return Puzzle(cells=cells, height=3, width=3, geometry_type="hex")


class TestHexGeometry(unittest.TestCase):
    def test_contains_returns_true_for_existing_cell(self):
        puzzle = make_puzzle_3x3()
        geometry = HexGeometry(puzzle)

        self.assertTrue(geometry.contains(Position(1, 1)))

    def test_contains_returns_false_for_missing_cell(self):
        puzzle = make_puzzle_3x3()
        geometry = HexGeometry(puzzle)

        self.assertFalse(geometry.contains(Position(5, 5)))

    def test_neighbors_for_top_left_corner(self):
        puzzle = make_puzzle_3x3()
        geometry = HexGeometry(puzzle)

        neighbors = geometry.neighbors(Position(0, 0))

        self.assertEqual(
            neighbors,
            [
                Position(0, 1),
                Position(1, 0),
            ],
        )

    def test_neighbors_for_center_cell(self):
        puzzle = make_puzzle_3x3()
        geometry = HexGeometry(puzzle)

        neighbors = geometry.neighbors(Position(1, 1))

        self.assertEqual(
            neighbors,
            [
                Position(0, 1),
                Position(0, 2),
                Position(1, 2),
                Position(2, 1),
                Position(2, 0),
                Position(1, 0),
            ],
        )


if __name__ == "__main__":
    unittest.main()
