from __future__ import annotations

from numberlink.domain.position import Position
from numberlink.domain.puzzle import Puzzle


class HexGeometry:
    # Смещения для шестиугольной сетки (в виде (delta_row, delta_column))
    DIRECTIONS = [
        (-1, 0),  # вверх
        (-1, 1),  # вверх-вправо
        (0, 1),  # вправо
        (1, 0),  # вниз
        (1, -1),  # вниз-влево
        (0, -1),  # влево
    ]

    def __init__(self, puzzle: Puzzle) -> None:
        self.puzzle = puzzle

    def contains(self, position: Position) -> bool:
        """Проверяет, находится ли позиция внутри границ доски"""
        return position in self.puzzle.cells

    def neighbors(self, position: Position) -> list[Position]:
        """Возвращает соседние позиции в шестиугольной сетке"""
        neighbors = []
        for delta_row, delta_col in self.DIRECTIONS:
            neighbor_pos = position.shifted(delta_row, delta_col)
            if self.contains(neighbor_pos):
                neighbors.append(neighbor_pos)
        return neighbors
