from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterator

from numberlink.domain.position import Position
from numberlink.domain.puzzle import Puzzle

Solution = dict[str, list[Position]]


class Solver(ABC):
    @abstractmethod
    def iter_solutions(
        self, puzzle: Puzzle, geometry: object, max_solutions: int | None = None
    ) -> Iterator[Solution]:
        """Лениво возвращает найденные решения головоломки."""
        raise

    def solve_all(
        self, puzzle: Puzzle, geometry: object, max_solutions: int | None = None
    ) -> list[Solution]:
        """Возвращает все найденные решения головоломки."""
        return list(self.iter_solutions(puzzle, geometry, max_solutions))
