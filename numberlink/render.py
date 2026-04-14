from __future__ import annotations

try:
    from colorama import just_fix_windows_console
except ImportError:
    just_fix_windows_console = None

from numberlink.domain.position import Position

if just_fix_windows_console is not None:
    just_fix_windows_console()


LABEL_COLORS = [
    "\033[92m",  # зелёный
    "\033[91m",  # красный
    "\033[94m",  # синий
    "\033[93m",  # жёлтый
    "\033[95m",  # фиолетовый
    "\033[96m",  # голубой
    "\033[97m",  # белый
]

RESET = "\033[0m"


def render_solution(puzzle, solution, color=False):
    "Рендерит решение головоломки в виде текстовой сетки."
    grid = [["." for _ in range(puzzle.width)] for _ in range(puzzle.height)]
    color_map = _build_label_color_map(solution)

    for label, path in solution.items():
        for index, pos in enumerate(path):
            is_endpoint = index == 0 or index == len(path) - 1
            value = label.upper() if is_endpoint else label.lower()

            if color:
                value = _paint(value, color_map[label])

            grid[pos.row][pos.column] = value

    for row_index, row in enumerate(grid):
        indent = " " * row_index
        print(indent + " ".join(row))


def render_graph_solution(puzzle, solution, color=False):
    """
    Рендерит решение как граф:
    - клетки показываются в виде [A], [a], [.]
    - путь показывается на рёбрах как ===, /, \
    - стены (если позже будут добавлены в puzzle.walls) показываются как X
    """
    cell_values, cell_labels = _build_cell_values(solution)
    path_edges = _build_path_edges(solution)
    edge_labels = _build_edge_labels(solution)
    color_map = _build_label_color_map(solution)
    walls = getattr(puzzle, "walls", set())

    for row in range(puzzle.height):
        print(
            _build_row_line(
                puzzle,
                row,
                cell_values,
                cell_labels,
                path_edges,
                edge_labels,
                walls,
                color,
                color_map,
            )
        )

        if row < puzzle.height - 1:
            connector_line = _build_between_rows_line(
                puzzle,
                row,
                path_edges,
                edge_labels,
                walls,
                color,
                color_map,
            )
            if connector_line.strip():
                print(connector_line)


def _build_label_color_map(solution) -> dict[str, str]:
    labels = list(solution.keys())
    return {
        label: LABEL_COLORS[index % len(LABEL_COLORS)]
        for index, label in enumerate(labels)
    }


def _paint(text: str, ansi_color: str) -> str:
    return f"{ansi_color}{text}{RESET}"


def _build_cell_values(
    solution,
) -> tuple[dict[Position, str], dict[Position, str]]:
    values = {}
    labels = {}

    for label, path in solution.items():
        for index, pos in enumerate(path):
            is_endpoint = index == 0 or index == len(path) - 1
            values[pos] = label.upper() if is_endpoint else label.lower()
            labels[pos] = label

    return values, labels


def _build_path_edges(solution) -> set[frozenset[Position]]:
    edges = set()

    for path in solution.values():
        for index in range(len(path) - 1):
            edge = frozenset((path[index], path[index + 1]))
            edges.add(edge)

    return edges


def _build_edge_labels(solution) -> dict[frozenset[Position], str]:
    edge_labels = {}

    for label, path in solution.items():
        for index in range(len(path) - 1):
            edge = frozenset((path[index], path[index + 1]))
            edge_labels[edge] = label

    return edge_labels


def _build_row_line(
    puzzle,
    row,
    cell_values,
    cell_labels,
    path_edges,
    edge_labels,
    walls,
    color,
    color_map,
) -> str:
    parts = ["  " * row]

    for column in range(puzzle.width):
        pos = Position(row, column)
        cell_text = f"[{cell_values.get(pos, '.')}]"

        label = cell_labels.get(pos)
        if color and label is not None:
            cell_text = _paint(cell_text, color_map[label])

        parts.append(cell_text)

        if column < puzzle.width - 1:
            right_pos = Position(row, column + 1)
            edge = frozenset((pos, right_pos))
            parts.append(
                _horizontal_edge_text(
                    edge,
                    path_edges,
                    edge_labels,
                    walls,
                    color,
                    color_map,
                )
            )

    return "".join(parts).rstrip()


def _build_between_rows_line(
    puzzle,
    row,
    path_edges,
    edge_labels,
    walls,
    color,
    color_map,
) -> str:
    """
    Строит строку диагональных связей между row и row + 1.

    Для клетки нижней строки (row + 1, col) возможны два соединения:
    - с верхней левой клеткой (row, col)          -> "\\"
    - с верхней правой клеткой (row, col + 1)     -> "/"
    """
    parts = ["  " * row, "  "]

    for column in range(puzzle.width):
        lower = Position(row + 1, column)

        upper_left = Position(row, column)
        upper_right = Position(row, column + 1)

        left_edge = frozenset((upper_left, lower))
        right_edge = frozenset((upper_right, lower))

        parts.append(
            _diagonal_edge_text(
                left_edge,
                path_edges,
                edge_labels,
                walls,
                color,
                color_map,
                "\\",
            )
        )
        parts.append("   ")
        parts.append(
            _diagonal_edge_text(
                right_edge,
                path_edges,
                edge_labels,
                walls,
                color,
                color_map,
                "/",
            )
        )

        if column < puzzle.width - 1:
            parts.append("   ")

    return "".join(parts).rstrip()


def _horizontal_edge_text(
    edge, path_edges, edge_labels, walls, color, color_map
) -> str:
    if edge in path_edges:
        text = "=== "
        if color:
            label = edge_labels[edge]
            return _paint(text, color_map[label])
        return text

    if edge in walls:
        return " X  "

    return "    "


def _diagonal_edge_text(
    edge, path_edges, edge_labels, walls, color, color_map, symbol: str
) -> str:
    if len(edge) < 2:
        return " "

    if edge in path_edges:
        if color:
            label = edge_labels[edge]
            return _paint(symbol, color_map[label])
        return symbol

    if edge in walls:
        return "X"

    return " "
