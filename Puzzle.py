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
        # has_zero = False
        # for col in range(0, 9):
        #     cell = self.rows[row][col]
        #     if cell == digit: return False
        #     if cell == 0: has_zero = True
        # return has_zero
        return digit not in self.rows[row] and 0 in self.rows[row]

    def is_col_candidate(self, col, digit):
        # has_zero = False
        # row = 0
        # while True:
        #     cell = self.rows[row][col]
        #     if cell == digit: return False
        #     if cell == 0: has_zero = True
        #     row += 1
        #     if row == 9: break
        # return has_zero
        has_zero = True
        cell0 = self.rows[0][col]
        cell1 = self.rows[1][col]
        cell2 = self.rows[2][col]
        cell3 = self.rows[3][col]
        cell4 = self.rows[4][col]
        cell5 = self.rows[5][col]
        cell6 = self.rows[6][col]
        cell7 = self.rows[7][col]
        cell8 = self.rows[8][col]
        if cell0 and cell1 and cell2 and cell3 and cell4 and cell5 and cell6 and cell7 and cell8: return False
        if cell1 == digit: return False
        if cell2 == digit: return False
        if cell3 == digit: return False
        if cell4 == digit: return False
        if cell5 == digit: return False
        if cell6 == digit: return False
        if cell7 == digit: return False
        if cell8 == digit: return False
        return True

    def is_grid_candidate(self, row, col, digit):
        gridno = self.calculate_gridno(row, col)
        grid_row, grid_col = self.uncalculate_gridno(gridno)
        # has_zero = False
        # grid_rows = range(grid_row, grid_row + 3)
        # grid_cols = range(grid_col, grid_col + 3)
        # for irow in grid_rows:
        #     for icol in grid_cols:
        #         cell = self.rows[irow][icol]
        #         if cell == digit: return False
        #         if cell == 0: has_zero = True
        # return has_zero
        grid_col_3 = grid_col+3
        has_zero = (0 in self.rows[grid_row][grid_col:grid_col_3]) or (0 in self.rows[grid_row+1][grid_col:grid_col_3]) or (0 in self.rows[grid_row+2][grid_col:grid_col_3])
        if not has_zero: return False
        no_digit = (digit not in self.rows[grid_row][grid_col:grid_col_3]) and (digit not in self.rows[grid_row+1][grid_col:grid_col_3]) and (digit not in self.rows[grid_row+2][grid_col:grid_col_3])
        return no_digit

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