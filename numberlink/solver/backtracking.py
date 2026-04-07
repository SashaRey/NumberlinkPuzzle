from collections import defaultdict
from numberlink.solver.base import Solver


class BacktrackingSolver(Solver):
    def solve_all(self, puzzle, geometry):
        endpoints = self._find_endpoints(puzzle)

        occupied = set()
        for positions in endpoints.values():
            occupied.update(positions)

        labels = list(endpoints.keys())
        paths = {}
        solutions = []

        # success = self._connect_pairs(
        #     labels=labels,
        #     index=0,
        #     endpoints=endpoints,
        #     geometry=geometry,
        #     occupied=occupied,
        #     paths=paths,
        # )

        # if success:
        #     return [paths.copy()]
        # return []
        self._connect_pairs(labels, 0, endpoints, geometry, occupied, paths, solutions)
        return solutions

    def _find_endpoints(self, puzzle):
        endpoints = defaultdict(list)

        for pos, value in puzzle.cells.items():
            if value != ".":
                endpoints[value].append(pos)

        return dict(endpoints)

    def _connect_pairs(self, labels, index, endpoints, geometry, occupied, paths, solutions):
        if index == len(labels):
            solutions.append(paths.copy())
            return

        label = labels[index]
        start, end = endpoints[label]

        for path in self._find_all_paths(start, end, geometry, occupied):
            paths[label] = path.copy()

            added_positions = []
            for pos in path:
                if pos not in occupied:
                    occupied.add(pos)
                    added_positions.append(pos)

            self._connect_pairs(
            labels,
            index + 1,
            endpoints,
            geometry,
            occupied,
            paths,
            solutions,
        )

            for pos in added_positions:
                occupied.remove(pos)
            del paths[label]

        return False

    def _find_all_paths(self, start, target, geometry, occupied):
        path = [start]
        used_in_path = {start}
        result = []

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

    def _dfs_collect_paths(self, current, target, geometry, occupied, path, used_in_path, result):
        if current == target:
            result.append(path.copy())
            return

        for neighbor in geometry.neighbors(current):
            if neighbor == target:
                path.append(neighbor)
                result.append(path.copy())
                path.pop()
                continue

            if neighbor in occupied:
                continue

            if neighbor in used_in_path:
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