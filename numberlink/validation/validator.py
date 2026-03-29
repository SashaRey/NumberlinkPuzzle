from collections import defaultdict

from numberlink.exceptions import InvalidPuzzleError


class PuzzleValidator:
    def find_endpoints(self, puzzle):
        endpoints = defaultdict(list)

        for pos, value in puzzle.cells.items():
            if value != '.':
                endpoints[value].append(pos)

        return dict(endpoints)

    def validate(self, puzzle):
        if not puzzle.cells:
            raise InvalidPuzzleError("Поле пустое")

        if puzzle.geometry_type != "hex":
            raise InvalidPuzzleError(f"Неподдерживаемая геометрия: {puzzle.geometry_type}")

        endpoints = self.find_endpoints(puzzle)

        if not endpoints:
            raise InvalidPuzzleError("На поле нет ни одной пары точек")

        for label, positions in endpoints.items():
            if len(positions) != 2:
                raise InvalidPuzzleError(
                    f"Символ '{label}' должен встречаться ровно 2 раза, сейчас: {len(positions)}"
                )