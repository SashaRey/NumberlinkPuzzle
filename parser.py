from board import Board
from exceptions import InputFormatError, InvalidPuzzleError

def parse_puzzle(text):
    """Парсит входной текст и возвращает объект Board"""
    lines = text.strip().splitlines()
    if not lines:
        raise InputFormatError("Входные данные не могут быть пустыми")
    
    width = len(lines[0])
    for line in lines:
        if len(line) != width:
            raise InputFormatError("Все строки должны иметь одинаковую длину")
    
    grid = [list(line) for line in lines]
    board = Board(grid)
    
    endpoints = board.find_endpoints()
    for value, positions in endpoints.items():
        if len(positions) != 2:
            raise InvalidPuzzleError(f"Значение '{value}' должно иметь ровно две конечные точки")
    
    return board

def _prepare_lines(text):
    """Подготавливает строки, удаляя лишние пробелы и проверяя формат"""
    lines = text.strip().splitlines()
    if not lines:
        raise InputFormatError("Входные данные не могут быть пустыми")
    
    width = len(lines[0])
    for line in lines:
        if len(line) != width:
            raise InputFormatError("Все строки должны иметь одинаковую длину")
    
    return lines

def _parse_structure(lines):
    """Парсит структуру доски и возвращает сетку"""
    grid = [list(line) for line in lines]
    return grid

def _validate_symbols(grid):
    """Проверяет, что все символы на доске допустимы"""
    valid_symbols = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ.")
    for row in grid:
        for cell in row:
            if cell not in valid_symbols:
                raise InputFormatError(f"Недопустимый символ '{cell}' на доске")

def _validate_endpoints(board):
    """Проверяет, что каждая буква имеет ровно две конечные точки"""
    endpoints = board.find_endpoints()
    for value, positions in endpoints.items():
        if len(positions) != 2:
            raise InvalidPuzzleError(f"Значение '{value}' должно иметь ровно две конечные точки") 

def _validate_puzzle(board, expected_height, expected_width):
    """Проверяет, что размеры доски соответствуют ожиданиям"""
    if board.height != expected_height:
        raise InputFormatError(f"Ожидалось {expected_height} строк, но получено {board.height}")
    if board.width != expected_width:
        raise InputFormatError(f"Ожидалось {expected_width} столбцов, но получено {board.width}")                   
            