from dataclasses import dataclass

@dataclass(frozen=True)
class Position:
    row: int
    column: int

    def shifted(self, delta_row: int, delta_column: int) -> 'Position':
        """Возвращает новую позицию, смещённую на заданные значения"""
        return Position(self.row + delta_row, self.column + delta_column)