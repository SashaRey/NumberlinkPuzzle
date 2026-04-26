import unittest

from numberlink.domain.position import Position
from numberlink.domain.puzzle import Puzzle
from numberlink.exceptions import InvalidPuzzleError
from numberlink.geometry.factory import create_geometry
from numberlink.geometry.hex import HexGeometry


class TestGeometryFactory(unittest.TestCase):
    def test_create_geometry_returns_hex_geometry_for_hex_type(self):
        puzzle = Puzzle(
            cells={Position(0, 0): "."},
            height=1,
            width=1,
            geometry_type="hex",
        )

        geometry = create_geometry(puzzle)

        self.assertIsInstance(geometry, HexGeometry)

    def test_create_geometry_raises_for_unknown_type(self):
        puzzle = Puzzle(
            cells={Position(0, 0): "."},
            height=1,
            width=1,
            geometry_type="triangle",
        )

        with self.assertRaisesRegex(
            InvalidPuzzleError,
            "Неизвестный тип геометрии",
        ):
            create_geometry(puzzle)


if __name__ == "__main__":
    unittest.main()
