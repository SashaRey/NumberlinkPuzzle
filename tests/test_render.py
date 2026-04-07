from numberlink.domain.position import Position
from numberlink.domain.puzzle import Puzzle
from numberlink.render import render_solution


def test_render_solution_prints_grid(capsys):
    """Проверяет, что render_solution правильно отображает сетку."""
    puzzle = Puzzle(
        cells={
            Position(0, 0): "A",
            Position(0, 1): ".",
            Position(1, 0): ".",
            Position(1, 1): "A",
        },
        height=2,
        width=2,
        geometry_type="hex",
    )

    solution = {
        "A": [Position(0, 0), Position(0, 1), Position(1, 1)],
    }