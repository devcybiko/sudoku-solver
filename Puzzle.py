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

    def is_col_candidate(self, col, digit):
        cell0 = self.rows[0][col]
        cell1 = self.rows[1][col]
        cell2 = self.rows[2][col]
        cell3 = self.rows[3][col]
        cell4 = self.rows[4][col]
        cell5 = self.rows[5][col]
        cell6 = self.rows[6][col]
        cell7 = self.rows[7][col]
        cell8 = self.rows[8][col]
        if digit in [cell0, cell1, cell2, cell3, cell4, cell5, cell6, cell7, cell8]: return False
        return True

    def is_grid_candidate(self, row, col, digit):
        grid_row = (row // 3) * 3
        grid_col = (col // 3) * 3
        grid_col_3 = grid_col+3
        has_digit = (digit in self.rows[grid_row][grid_col:grid_col_3]) or (digit in self.rows[grid_row+1][grid_col:grid_col_3]) or (digit in self.rows[grid_row+2][grid_col:grid_col_3])
        return not has_digit

    def is_candidate(self, row, col, digit):
        if self.rows[row][col] != 0: return False
        if digit in self.rows[row]: return False
        if not self.is_col_candidate(col, digit): return False
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
        col_sum = [0,0,0,0,0,0,0,0,0]
        for irow in range(0, 9):
            row_sum = 0
            for icol in range(0, 9):
                cell = self.get(irow, icol) 
                if cell == 0: return False
                row_sum += cell
                col_sum[icol] += cell
            if row_sum != 45:
                print("ERROR: row_sum["+str(irow)+"] = " + str(row_sum))
                return False
        for icol in range(0,9):
            if col_sum[icol] != 45:
                print("ERROR: col_sum["+str(icol)+"] = " + str(col_sum[icol]))
                return False
        return True