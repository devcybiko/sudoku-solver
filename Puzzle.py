import sys
import json

class Puzzle:
    def __init__(self, fname):
        self.rows = self.read_puzzle(fname)
        pass

    def read_puzzle(self, fname):
        newrows = []
        f = open(fname)
        rows = json.load(f)
        f.close()
        if len(rows) != 9: raise "bad puzzle format - rows should be 9 but is " + len(rows)
        for irow in range(0,len(rows)):
            row = rows[irow]
            newrow = []
            if len(row) != 9: raise "bad puzzle format - each row should be 9 characters"
            for icol in range(0, len(row)):
                cell = row[icol]
                if cell not in "0123456789-": raise "bad puzzle format - bad cell: " + cell
                if cell == '-' or cell == '.' : cell = '0'
                newrow.append(int(cell))
            newrows.append(newrow)
        return newrows

    def get_row(self,row):
        cells = []
        for i in range(0,9):
            cells.append(self.rows[row][i])
        return cells

    def get_col(self, col):
        cells = []
        for row in range(0,9):
            cells.append(self.rows[row][col])
        return cells

    def get_grid(self, gridno):
        cells = []
        grid_row, grid_col = self.uncalculate_gridno(gridno)
        grid_rows = range(grid_row, grid_row + 3)
        grid_cols = range(grid_col, grid_col + 3)
        for irow in grid_rows:
            for icol in grid_cols:
                cells.append(self.rows[irow][icol])
        return cells

    def count_cells(self, cells):
        digits = [0,0,0,0,0,0,0,0,0,0]
        for i in range(0,len(cells)): # iterate across the row
            digit = cells[i] # get the digit
            digits[digit] += 1 # count the number of times a digit is used
        return digits

    def print(self):
        print("+ --- + --- + --- +")
        for irow in range(0,9):
            s = "| "
            for icol in range(0,9):
                cell = str(self.rows[irow][icol])
                if cell == '0': cell = '.'
                s += cell
                if icol % 3 == 2: s += " | "
            print(s)
            if irow % 3 == 2: print("+ --- + --- + --- +")

    def calculate_gridno(self, row, col):
        return (row // 3) * 3 + (col // 3);
    
    def uncalculate_gridno(self, gridno):
        return (gridno // 3) * 3, (gridno % 3) * 3

    def is_row_candidate(self, row, digit):
        has_zero = False
        for col in range(0, 9):
            cell = self.rows[row][col]
            if cell == digit: return False
            if cell == 0: has_zero = True
        return has_zero

    def is_col_candidate(self, col, digit):
        has_zero = False
        for row in range(0,9):
            cell = self.rows[row][col]
            if cell == digit: return False
            if cell == 0: has_zero = True
        return has_zero

    def is_grid_candidate(self, row, col, digit):
        has_zero = False
        gridno = self.calculate_gridno(row, col)
        grid_row, grid_col = self.uncalculate_gridno(gridno)
        grid_rows = range(grid_row, grid_row + 3)
        grid_cols = range(grid_col, grid_col + 3)
        for irow in grid_rows:
            for icol in grid_cols:
                cell = self.rows[irow][icol]
                if cell == digit: return False
                if cell == 0: has_zero = True
        return has_zero

    def is_candidate(self, row, col, digit):
        if self.rows[row][col] != 0: return False

        # the_row = self.get_row(row)
        # row_counts = self.count_cells(the_row)
        # if row_counts[digit] != 0: return False
        if not self.is_row_candidate(row, digit): return False

        # the_col = self.get_col(col)
        # col_counts = self.count_cells(the_col)
        # if col_counts[digit] != 0: return False
        if not self.is_col_candidate(col, digit): return False

        # gridno = self.calculate_gridno(row, col)
        # the_grid = self.get_grid(gridno)
        # grid_counts = self.count_cells(the_grid)
        # if grid_counts[digit] != 0: return False
        if not self.is_grid_candidate(row, col, digit): return False

        return True
    
    def get_candidates(self, row, col):
        candidates = []
        my_digit = self.get(row, col)
        if my_digit != 0:
            return [my_digit]
        for candidate in range(1,10):
            if self.is_candidate(row, col, candidate):
                candidates.append(candidate)
        return candidates
    
    def get(self, row, col):
        return self.rows[row][col]
    
    def update(self, row, col, digit):
        if self.rows[row][col]: return False
        self.rows[row][col] = digit
        return True
    
    def set(self, row, col, digit):
        self.rows[row][col] = digit

    def next_cell(self, row, col):
        irow = row
        icol = col
        while(True):
            icol += 1
            if icol >= 9:
                icol = 0
                irow += 1
                if irow >= 9:
                    break
            if self.get(irow, icol) == 0: break
        return irow, icol

    def is_solved(self):
        for irow in range(0, 9):
            for icol in range(0, 9):
                if self.get(irow, icol) == 0: return False
        return True