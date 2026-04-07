from abc import ABC, abstractmethod

class Solver(ABC):
    @abstractmethod
    def solve_all(self, puzzle, geometry):
        """Возвращает все допустимые решения головоломки"""
        pass