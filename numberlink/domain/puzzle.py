from dataclasses import dataclass
from typing import Dict
from .position import Position

@dataclass(frozen=True)
class Puzzle:
    cells: Dict[Position, str]
    height: int
    width: int
    geometry_type: str

    def get_cell(self, position: Position) -> str:
        """Возвращает значение в указанной позиции"""
        return self.cells.get(position, '.')
    
    def is_inside(self, position: Position) -> bool:
        """Проверяет, находится ли позиция внутри границ доски"""
        return 0 <= position.row < self.height and 0 <= position.column < self.width