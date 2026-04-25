from __future__ import annotations

from dataclasses import dataclass, field
from numberlink.domain.position import Position


@dataclass(frozen=True)
class Puzzle:
    cells: dict[Position, str]
    height: int
    width: int
    geometry_type: str
    walls: frozenset = field(default_factory=frozenset)

    def get_cell(self, position: Position) -> str:
        """Возвращает значение в указанной позиции"""
        return self.cells.get(position, ".")

    def is_inside(self, position: Position) -> bool:
        """Проверяет, находится ли позиция внутри границ доски"""
        return 0 <= position.row < self.height and 0 <= position.column < self.width
