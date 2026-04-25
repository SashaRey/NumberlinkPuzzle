import math
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QPolygonF, QFont
from PyQt6.QtCore import Qt, QPointF


class HexGrid:
    def __init__(self, size: float = 30.0):
        self.size = size
        self.width = size * math.sqrt(3)
        self.height = size * 2.0
        self.horizontal_spacing = self.width
        self.vertical_spacing = size * 1.5

    def center(self, row: int, col: int) -> tuple[float, float]:
        x = self.width * (col + row / 2.0)
        y = self.vertical_spacing * row
        return x, y

    def polygon(self, row: int, col: int) -> list[tuple[float, float]]:
        cx, cy = self.center(row, col)
        points = []
        for i in range(6):
            # Pointy top hexes start at 30 degrees (i=0 -> 30, i=1 -> 90, ...)
            angle_deg = 60 * i - 30
            angle_rad = math.radians(angle_deg)
            px = cx + self.size * math.cos(angle_rad)
            py = cy + self.size * math.sin(angle_rad)
            points.append((px, py))
        return points


class HexCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid = HexGrid(size=35.0)
        self.puzzle = None
        self.solution = None

        self.label_colors = [
            QColor("#2ecc71"),  # green
            QColor("#e74c3c"),  # red
            QColor("#3498db"),  # blue
            QColor("#f1c40f"),  # yellow
            QColor("#9b59b6"),  # purple
            QColor("#00bcd4"),  # cyan
            QColor("#ecf0f1"),  # white
        ]
        self.color_map = {}

    def set_puzzle(self, puzzle):
        self.puzzle = puzzle
        self.solution = None
        self.color_map = {}
        # assign colors to keys
        keys = set(puzzle.cells.values())
        keys.discard(".")
        for i, key in enumerate(sorted(keys)):
            self.color_map[key.upper()] = self.label_colors[i % len(self.label_colors)]
            self.color_map[key.lower()] = self.label_colors[i % len(self.label_colors)]

        self.update()

    def set_solution(self, solution):
        self.solution = solution
        self.update()

    def get_color(self, char):
        return self.color_map.get(char, QColor(255, 255, 255))

    def paintEvent(self, event):
        if not self.puzzle:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Calculate bounding box to center the grid
        min_x = min_y = float("inf")
        max_x = max_y = float("-inf")

        for pos in self.puzzle.cells:
            # check the boundary points
            pts = self.grid.polygon(pos.row, pos.column)
            for px, py in pts:
                min_x = min(min_x, px)
                min_y = min(min_y, py)
                max_x = max(max_x, px)
                max_y = max(max_y, py)

        grid_width = max_x - min_x
        grid_height = max_y - min_y

        offset_x = (self.width() - grid_width) / 2 - min_x
        offset_y = (self.height() - grid_height) / 2 - min_y

        painter.translate(offset_x, offset_y)

        # Draw background hexes
        for pos, val in self.puzzle.cells.items():
            self._draw_hex(painter, pos.row, pos.column, val)

        # Draw solution paths if present
        if self.solution:
            for label, path in self.solution.items():
                self._draw_path(painter, path, self.get_color(label))

        self._draw_walls(painter)

    def _draw_walls(self, painter: QPainter):
        walls = getattr(self.puzzle, "walls", set())
        if not walls:
            return

        pen = QPen(QColor(255, 50, 50), 6)
        painter.setPen(pen)

        for wall in walls:
            wall_list = list(wall)
            if len(wall_list) == 2:
                pos1, pos2 = wall_list
                # For hexes, find the midpoint between centers
                x1, y1 = self.grid.center(pos1.row, pos1.column)
                x2, y2 = self.grid.center(pos2.row, pos2.column)
                # find orthogonal vector for wall drawing
                dx = x2 - x1
                dy = y2 - y1
                # normalize vector
                length = (dx * dx + dy * dy) ** 0.5
                if length == 0:
                    continue
                nx, ny = dx / length, dy / length
                # tangent vector
                tx, ty = -ny, nx
                cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

                wall_len = self.grid.size * 0.8
                painter.drawLine(
                    QPointF(cx - tx * wall_len, cy - ty * wall_len),
                    QPointF(cx + tx * wall_len, cy + ty * wall_len),
                )

    def _draw_hex(self, painter: QPainter, row: int, col: int, val: str):
        pts = self.grid.polygon(row, col)
        polygon = QPolygonF([QPointF(x, y) for x, y in pts])

        # Pen and brush for hex
        pen = QPen(QColor(100, 100, 100), 2)
        brush = QBrush(QColor(40, 40, 40))

        if val != ".":
            # the endpoint background
            brush.setColor(QColor(60, 60, 60))

        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawPolygon(polygon)

        # Draw label if it's an endpoint
        if val != ".":
            painter.setPen(QPen(self.get_color(val)))
            font = painter.font()
            font.setPointSize(16)
            font.setBold(True)
            painter.setFont(font)
            cx, cy = self.grid.center(row, col)
            painter.drawText(
                int(cx - self.grid.size),
                int(cy - self.grid.size),
                int(self.grid.size * 2),
                int(self.grid.size * 2),
                Qt.AlignmentFlag.AlignCenter,
                val,
            )

    def _draw_path(self, painter: QPainter, path: list, color: QColor):
        if not path or len(path) < 2:
            return

        pen = QPen(
            color,
            6,
            Qt.PenStyle.SolidLine,
            Qt.PenCapStyle.RoundCap,
            Qt.PenJoinStyle.RoundJoin,
        )
        painter.setPen(pen)

        for i in range(len(path) - 1):
            pos1 = path[i]
            pos2 = path[i + 1]
            x1, y1 = self.grid.center(pos1.row, pos1.column)
            x2, y2 = self.grid.center(pos2.row, pos2.column)
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
