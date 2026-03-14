from board import Board
import pytest

class TestBoard:
    def test_board_initialization(self):
        board = Board([
            "A..B",
            "....",
            "....",
            "A..B",
        ])
        assert board.height == 4
        assert board.width == 4
        assert board.get_cell(0, 0) == 'A'
    
    def test_empty_grid_raises_error(self):
        with pytest.raises(ValueError):
            Board([])
    
    def test_rows_with_different_lengths_raise_error(self):
        with pytest.raises(ValueError):
            Board([
                "A..B",
                ".....",
            ])
    
    def test_is_inside(self):
        board = Board([
            "A..B",
            "....",
            "....",
            "A..B",
        ])
        assert board.is_inside(0, 0) == True
        assert board.is_inside(3, 3) == True
        assert board.is_inside(-1, 0) == False
        assert board.is_inside(0, -1) == False
        assert board.is_inside(4, 0) == False
        assert board.is_inside(0, 4) == False

    def test_get_cell():
        board = Board([
            "A..",
            "...",
            "..A",
        ])
        assert board.get_cell(0, 0) == 'A'
        assert board.get_cell(1, 1) == '.'
        assert board.get_cell(2, 2) == 'A'
    
    def test_get_cell_out_of_bounds_raises_error():
        board = Board([
            "A..",
            "...",
            "..A",
        ])
        with pytest.raises(IndexError, match="Позиция вне границ доски"):
            board.get_cell(5,5)

    def test_set_cell():
        board = Board([
            "A..",
            "...",
            "..A",
        ])
        board.set_cell(1, 1, 'X')
        assert board.get_cell(1, 1) == 'X'

    def test_set_cell_out_of_bounds_raises_error():
        board = Board([
            "A..",
            "...",
            "..A",
        ])
        with pytest.raises(IndexError, match="Позиция вне границ доски"):
            board.set_cell(5,5,'X')
    
    def test_neighbors(self):
        board = Board([
            "...",
            "...",
            "...",
        ])
        assert set(board.neighbors(0, 0)) == {(1,0), (0,1)}
    
    def test_neighbors_for_center_cell(self):
        board = Board([
            "...",
            "...",
            "...",
        ])
        assert set(board.neighbors(1, 1)) == {(0,1), (2,1), (1,0), (1,2)}

    def test_find_endpoints(self):
        board = Board([
            "A..B",
            "....",
            "....",
            "A..B",
        ])
        endpoints = board.find_endpoints()
        assert endpoints == {
            'A': [(0, 0), (3, 0)],
            'B': [(0, 3), (3, 3)]
        }

    def test_count_empty_cells():
        board = Board([
            "A..B",
            "....",
            "....",
            "A..B",
        ])
        assert board.count_empty_cells() == 12

    def test_copy_is_independent():
        board = Board([
            "A..",
            "...",
            "..A",
        ])
        board_copy = board.copy()
        board_copy.set_cell(0, 0, 'X')

        assert board.get_cell(0, 0) == 'A'
        assert board_copy.get_cell(0, 0) == 'X'

    def test_str_representation(self):
        board = Board([
            "A..",
            "...",
            "..A",
        ])
        expected_str = "A..\n...\n..A"
        assert str(board) == expected_str