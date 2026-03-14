from copy import deepcopy

class Board:
    """Модель игрового поля Numberlink"""

    def __init__(self, grid):
        if not grid:
            raise ValueError("Пустая сетка недопустима")
        
        row_lengths = {len(row) for row in grid}
        if len(row_lengths) > 1:
            raise ValueError("Все строки должны иметь одинаковую длину")
        
        self.grid = [list(row) for row in grid]
        self.height = len(self.grid)
        self.width = len(self.grid[0]) if self.grid else 0

    def is_inside(self, row, col):
            """Проверяет, находится ли позиция внутри границ доски"""
            return 0 <= row < self.height and 0 <= col < self.width    
        
    def get_cell(self, row, col):
            """Возвращает значение в указанной ячейке"""
            if not self.is_inside(row, col):
                raise IndexError("Позиция вне границ доски")
            return self.grid[row][col]    
        
    def set_cell(self, row, col, value):
        """Устанавливает значение в указанной ячейке"""
        if not self.is_inside(row, col):
            raise IndexError("Позиция вне границ доски")
        self.grid[row][col] = value

    def neighbors(self, row, col):
        """Возвращает соседние позиции (вверх, вниз, влево, вправо)"""
        candidates = [
            (row - 1, col),  # вверх
            (row + 1, col),  # вниз
            (row, col - 1),  # влево
            (row, col + 1)   # вправо
        ]
        return [(r, c) for r, c in candidates if self.is_inside(r, c)]
    
    def find_endpoints(self):
        """Находит все конечные точки на доске"""
        endpoints = {}
        for row in range(self.height):
            for col in range(self.width):
                value = self.grid[row][col]
                if value != '.':
                    endpoints.setdefault(value, []).append((row, col))
        return endpoints
    
    def count_empty_cells(self):
        """Подсчитывает количество пустых ячеек на доске"""
        return sum(row.count('.') for row in self.grid)
    
    def copy(self):
        """Создает глубокую копию доски"""
        return Board(deepcopy(self.grid))
    
    def __str__(self):
        """Возвращает строковое представление доски"""
        return '\n'.join(''.join(row) for row in self.grid)
    

board = Board([
    "A..B",
    "....",
    "....",
    "A..B",
])

print(board.height)
print(board.width)
print(board.get_cell(0, 0))
print(board.is_inside(3, 3))
print(board.neighbors(0, 0))
print(board.find_endpoints())
print(board.count_empty_cells())
print(board)