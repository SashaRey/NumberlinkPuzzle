from __future__ import annotations

import json
import hashlib
from pathlib import Path
from typing import Iterator

from numberlink.domain.position import Position
from numberlink.domain.puzzle import Puzzle
from numberlink.solver.base import Solution, Solver


class CachedSolver(Solver):
    """
    Обертка над Solver, инкрементально сохраняющая решения в JSONL.
    При досрочном прерывании найденные решения остаются в кэше.
    """

    def __init__(self, solver: Solver, cache_dir: str = ".numberlink_cache"):
        self._solver = solver
        self._cache_dir = Path(cache_dir)
        self._cache_dir.mkdir(exist_ok=True)

    def _puzzle_key(self, puzzle: Puzzle) -> str:
        # Детерминированный ключ для состояния головоломки
        cells_items = sorted(
            puzzle.cells.items(), key=lambda item: (item[0].row, item[0].column)
        )
        cells_str = ",".join(f"{p.row}:{p.column}={v}" for p, v in cells_items)
        base_str = f"{puzzle.width}x{puzzle.height}|{puzzle.geometry_type}|{cells_str}"
        return hashlib.md5(base_str.encode("utf-8")).hexdigest()

    def _serialize_solution(self, solution: Solution) -> str:
        serialized = {
            label: [[p.row, p.column] for p in path] for label, path in solution.items()
        }
        return json.dumps(serialized)

    def _deserialize_solution(self, data: dict) -> Solution:
        return {
            label: [Position(r, c) for r, c in path] for label, path in data.items()
        }

    def iter_solutions(
        self, puzzle: Puzzle, geometry: object, max_solutions: int | None = None
    ) -> Iterator[Solution]:
        cache_key = self._puzzle_key(puzzle)
        cache_file = self._cache_dir / f"{cache_key}.jsonl"

        yielded_count = 0
        is_finished = False

        # Читаем уже найденные решения из кэша
        if cache_file.exists():
            with open(cache_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    data = json.loads(line)
                    # Метка того, что решатель дошёл до конца дерева
                    if data.get("__finished__") is True:
                        is_finished = True
                        continue

                    if max_solutions is not None and yielded_count >= max_solutions:
                        return

                    yield self._deserialize_solution(data)
                    yielded_count += 1

        if is_finished:
            return
        if max_solutions is not None and yielded_count >= max_solutions:
            return

        # Если кэш неполный, запускаем оригинальный решатель
        solver_iter = self._solver.iter_solutions(puzzle, geometry, max_solutions)

        # Вычисляем вхолостую те решения, что мы уже выдали из кэша
        for _ in range(yielded_count):
            try:
                next(solver_iter)
            except StopIteration:
                break

        # Дописываем новые решения в кэш
        with open(cache_file, "a", encoding="utf-8") as f:
            for sol in solver_iter:
                if max_solutions is not None and yielded_count >= max_solutions:
                    return

                # Записываем в файл и сразу сбрасываем буфер на диск
                f.write(self._serialize_solution(sol) + "\n")
                f.flush()

                yield sol
                yielded_count += 1

            # Если генератор исчерпан полностью, значит новых решений точно нет
            if max_solutions is None or yielded_count < max_solutions:
                f.write(json.dumps({"__finished__": True}) + "\n")
                f.flush()

    def solve_all(
        self, puzzle: Puzzle, geometry: object, max_solutions: int | None = None
    ) -> list[Solution]:
        return list(self.iter_solutions(puzzle, geometry, max_solutions))
