from __future__ import annotations

from numberlink.geometry.hex import HexGeometry
from numberlink.exceptions import InvalidPuzzleError


def create_geometry(puzzle) -> HexGeometry:
    """Фабрика для создания объекта геометрии на основе типа головоломки"""
    if puzzle.geometry_type == "hex":
        return HexGeometry(puzzle)
    else:
        msg = f"Неизвестный тип геометрии: {puzzle.geometry_type}"
        raise InvalidPuzzleError(msg)
