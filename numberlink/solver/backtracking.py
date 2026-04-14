from __future__ import annotations

from collections import defaultdict
from typing import Iterator, Optional

from numberlink.domain.position import Position
from numberlink.domain.puzzle import Puzzle
from numberlink.solver.base import Solution, Solver


class BacktrackingSolver(Solver):
    "Решатель головоломки Numberlink с помощью алгоритма бэктрекинга."

    def iter_solutions(
        self,
        puzzle: Puzzle,
        geometry: object,
        max_solutions: Optional[int] = None,
    ) -> Iterator[Solution]:
        endpoints = self._find_endpoints(puzzle)

        occupied: set[Position] = set()
        for positions in endpoints.values():
            occupied.update(positions)

        labels = list(endpoints.keys())
        paths: dict[str, list[Position]] = {}
        found_count = [0]

        yield from self._connect_pairs(
            labels=labels,
            index=0,
            endpoints=endpoints,
            geometry=geometry,
            occupied=occupied,
            paths=paths,
            found_count=found_count,
            max_solutions=max_solutions,
        )

    # def solve_all(self, puzzle, geometry):
    #     endpoints = self._find_endpoints(puzzle)

    #     occupied = set()
    #     for positions in endpoints.values():
    #         occupied.update(positions)

    #     labels = list(endpoints.keys())
    #     paths = {}
    #     solutions = []
    #     self._connect_pairs(
    #         labels, 0, endpoints, geometry, occupied, paths, solutions
    #     )
    #     return solutions

    def _find_endpoints(self, puzzle):
        "Находит все конечные точки для каждой метки в головоломке."
        endpoints: defaultdict[str, list[Position]] = defaultdict(list)  # ?

        for pos, value in puzzle.cells.items():
            if value != ".":
                endpoints[value].append(pos)

        return dict(endpoints)

    def _connect_pairs(
        self,
        labels: list[str],
        index: int,
        endpoints: dict[str, list[Position]],
        geometry: object,
        occupied: set[Position],
        paths: dict[str, list[Position]],
        found_count: list[int],
        max_solutions: Optional[int],
    ) -> Iterator[Solution]:
        "Рекурсивно пытается соединить все пары меток, используя бэктрекинг."
        if max_solutions is not None and found_count[0] >= max_solutions:
            return

        if index == len(labels):
            found_count[0] += 1
            yield {label: path.copy() for label, path in paths.items()}
            return

        label = labels[index]
        start, end = endpoints[label]

        for path in self._find_all_paths(start, end, geometry, occupied):
            if max_solutions is not None and found_count[0] >= max_solutions:
                return

            paths[label] = path.copy()

            added_positions: list[Position] = []
            for pos in path:
                if pos not in occupied:
                    occupied.add(pos)
                    added_positions.append(pos)

            yield from self._connect_pairs(
                labels=labels,
                index=index + 1,
                endpoints=endpoints,
                geometry=geometry,
                occupied=occupied,
                paths=paths,
                found_count=found_count,
                max_solutions=max_solutions,
            )

            for pos in added_positions:
                occupied.remove(pos)

            del paths[label]

    def _find_all_paths(
        self,
        start: Position,
        target: Position,
        geometry: object,
        occupied: set[Position],
    ):
        """Находит все возможные пути от start до target.

        Обходит уже занятые позиции.
        """
        path: list[Position] = [start]
        used_in_path: set[Position] = {start}
        result: list[list[Position]] = []

        self._dfs_collect_paths(
            current=start,
            target=target,
            geometry=geometry,
            occupied=occupied,
            path=path,
            used_in_path=used_in_path,
            result=result,
        )

        return result

    def _dfs_collect_paths(
        self,
        current: Position,
        target: Position,
        geometry: object,
        occupied: set[Position],
        path: list[Position],
        used_in_path: set[Position],
        result: list[list[Position]],
    ) -> None:
        """Собирает все пути от current до target с помощью DFS.

        Пропускает занятые позиции.
        """
        if current == target:
            result.append(path.copy())
            return

        for neighbor in geometry.neighbors(current):
            if neighbor == target:
                path.append(neighbor)
                result.append(path.copy())
                path.pop()
                continue

            if neighbor in occupied or neighbor in used_in_path:
                continue

            used_in_path.add(neighbor)
            path.append(neighbor)

            self._dfs_collect_paths(
                current=neighbor,
                target=target,
                geometry=geometry,
                occupied=occupied,
                path=path,
                used_in_path=used_in_path,
                result=result,
            )

            path.pop()
            used_in_path.remove(neighbor)
