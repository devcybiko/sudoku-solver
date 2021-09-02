import unittest
from ddt import ddt, data, file_data, unpack
from Puzzle import Puzzle

expected_rows_1 = [[0, 7, 0, 0, 2, 0, 0, 4, 6], [0, 6, 0, 0, 0, 0, 8, 9, 0], [2, 0, 0, 8, 0, 0, 7, 1, 5], [0, 8, 4, 0, 9, 7, 0, 0, 0],
                    [7, 1, 0, 0, 0, 0, 0, 5, 9], [0, 0, 0, 1, 3, 0, 4, 8, 0], [6, 9, 7, 0, 0, 2, 0, 0, 8], [0, 5, 8, 0, 0, 0, 0, 6, 0], [4, 3, 0, 0, 8, 0, 0, 7, 0]]
expected_cols_1 = [[0, 0, 2, 0, 7, 0, 6, 0, 4],[7, 6, 0, 8, 1, 0, 9, 5, 3],[0, 0, 0, 4, 0, 0, 7, 8, 0],[0, 0, 8, 0, 0, 1, 0, 0, 0],[2, 0, 0, 9, 0, 3, 0, 0, 8],
                   [0, 0, 0, 7, 0, 0, 2, 0, 0],[0, 8, 7, 0, 0, 4, 0, 0, 0],[4, 9, 1, 0, 5, 8, 0, 6, 7],[6, 0, 5, 0, 9, 0, 8, 0, 0]]
expected_grids_1 = [
    [0, 7, 0, 0, 6, 0, 2, 0, 0],
[0, 2, 0, 0, 0, 0, 8, 0, 0],
[0, 4, 6, 8, 9, 0, 7, 1, 5],
[0, 8, 4, 7, 1, 0, 0, 0, 0],
[0, 9, 7, 0, 0, 0, 1, 3, 0],
[0, 0, 0, 0, 5, 9, 4, 8, 0],
[6, 9, 7, 0, 5, 8, 4, 3, 0],
[0, 0, 2, 0, 0, 0, 0, 8, 0],
[0, 0, 8, 0, 6, 0, 0, 7, 0]]

@ddt
class TestPuzzle(unittest.TestCase):
    def setUp(self):
        self.puzzle = Puzzle("puzzle-1.json")

    def test_loaded(self):
        self.assertEqual(self.puzzle.rows, expected_rows_1)

    def test_get_row(self):
        for row in range(0, 9):
            cells = self.puzzle.get_row(row)
            self.assertEqual(cells, expected_rows_1[row])

    def test_get_col(self):
        for col in range(0, 9):
            cells = self.puzzle.get_col(col)
            self.assertEqual(cells, expected_cols_1[col])

    def test_get_grid(self):
        for grid in range(0, 9):
            cells = self.puzzle.get_grid(grid)
            self.assertEqual(cells, expected_grids_1[grid])

    @data({"row": 0, "col": 0, "gridno": 0}, { "row": 0, "col": 1, "gridno": 0}, {"row": 0, "col": 2, "gridno": 0}, {"row": 0, "col": 3, "gridno": 1},
    {"row": 2, "col":2, "gridno": 0}, {"row": 3, "col": 1, "gridno": 3}, {"row": 4, "col": 5, "gridno": 4}, {"row": 5, "col": 8, "gridno": 5},
    {"row": 6, "col": 3, "gridno": 7}, {"row": 7, "col": 7, "gridno": 8})
    def test_calculate_gridno(self, value):
        gridno = self.puzzle.calculate_gridno(value["row"], value["col"])
        self.assertEqual(gridno, value["gridno"])

    @data(
        {"row": 0, "col": 0, "gridno": 0}, {"row": 0, "col": 3, "gridno": 1}, {"row": 0, "col": 6, "gridno": 2}, 
        {"row": 3, "col": 0, "gridno": 3}, {"row": 3, "col": 3, "gridno": 4}, {"row": 3, "col": 6, "gridno": 5}, 
        {"row": 6, "col": 0, "gridno": 6}, {"row": 6, "col": 3, "gridno": 7}, {"row": 6, "col": 6, "gridno": 8})
    def test_uncalculate_gridno(self, value):
        row, col = self.puzzle.uncalculate_gridno(value["gridno"])
        self.assertEqual(row, value["row"])
        self.assertEqual(col, value["col"])

    def test_count_cells(self):
        the_row = self.puzzle.get_row(0)
        counts = self.puzzle.count_cells(the_row)
        self.assertEqual(counts, [5, 0, 1, 0, 1, 0, 1, 1, 0, 0])
        the_col = self.puzzle.get_col(5)
        counts = self.puzzle.count_cells(the_col)
        self.assertEqual(counts, [7, 0, 1, 0, 0, 0, 0, 1, 0, 0])
        the_grid = self.puzzle.get_grid(5)
        counts = self.puzzle.count_cells(the_grid)
        self.assertEqual(counts, [5, 0, 0, 0, 1, 1, 0, 0, 1, 1])
    
    @data([0, 0, 1, True], [0, 0, 7, False], [4, 4, 5, False], [5, 5, 5, True])
    @unpack
    def test_is_candidate(self, row, col, digit, expected):
        result = self.puzzle.is_candidate(row, col, digit)
        self.assertEqual(result, expected)

    @data([0, 0, [1, 3, 5, 8, 9] ], [5, 5, [5, 6] ], [0, 1, [7]])
    @unpack
    def test_get_candidates(self, row, col, expected):
        result = self.puzzle.get_candidates(row, col)
        self.assertEqual(result, expected)

    @data([0, 0, 0, 2 ], [8, 7, 8, 8 ], [8, 8, 9, 0 ])
    @unpack
    def test_next_cell(self, row, col, expected_row, expected_col):
        result_row, result_col = self.puzzle.next_cell(row, col)
        self.assertEqual(result_row, expected_row)
        self.assertEqual(result_col, expected_col)
