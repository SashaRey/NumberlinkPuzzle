def render_solution(puzzle, solution):
    grid = [["." for _ in range(puzzle.width)] for _ in range(puzzle.height)]

    for label, path in solution.items():
        for pos in path:
            grid[pos.row][pos.column] = label

    for row_index, row in enumerate(grid):
        indent = "  " * row_index
        print(indent + " ".join(row))