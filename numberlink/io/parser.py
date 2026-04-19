from numberlink.domain.position import Position
from numberlink.domain.puzzle import Puzzle
from numberlink.exceptions import InputFormatError


def parse_puzzle(text: str) -> Puzzle:
    lines = _prepare_lines(text)

    geometry_type = lines[0]
    grid_lines = lines[1:]

    if not grid_lines:
        raise InputFormatError("Отсутствует поле")

    parsed_rows = [row.split() for row in grid_lines]

    _validate_row_lenghts(parsed_rows)
    _validate_symbols(parsed_rows)

    height = len(parsed_rows)
    width = len(parsed_rows[0]) if height > 0 else 0

    cells = {}
    for row_idx, row in enumerate(parsed_rows):
        for col_idx, symbol in enumerate(row):
            cells[Position(row_idx, col_idx)] = symbol

    return Puzzle(
        cells=cells,
        height=height,
        width=width,
        geometry_type=geometry_type,
    )


# Вспомогательные функции для парсинга и валидации


def _prepare_lines(text: str) -> list[str]:
    """Подготавливает строки, удаляя лишние пробелы и проверяя формат"""
    lines = text.strip().splitlines()
    if not lines:
        raise InputFormatError("Входные данные не могут быть пустыми")
    return lines


def _validate_row_lenghts(rows: list[list[str]]) -> None:
    """Проверяет, что все строки имеют одинаковую длину"""
    lengths = {len(row) for row in rows}
    if len(lengths) != 1:
        raise InputFormatError("Все строки должны иметь одинаковую длину")


def _validate_symbols(rows: list[list[str]]) -> None:
    """Проверяет, что все символы на доске допустимы"""
    valid_symbols = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ.")
    for row in rows:
        for cell in row:
            if cell not in valid_symbols:
                raise InputFormatError(f"Недопустимый символ '{cell}' на доске")
