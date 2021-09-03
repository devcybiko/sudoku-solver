import json

"""
even more optimized solution
we gain a small benefit by keeping three versions of the puzzle
- row-major form
- col-major form
- grid translate table

this allows us to use the `in` operator on arrays of values
which is much faster than iteration or even literal lookups

however there is an increased cost to maintain three tables

"""

class Puzzle:
    def __init__(self, fname):
        self.xlate_row, self.xlate_col = self.build_grid_xlate_table()
        self.rows, self.cols, self.grid = self.read_puzzle(fname)
        pass

    def read_puzzle(self, fname):
        newrows = []
        newcols = [[],[],[],[],[],[],[],[],[]]
        newgrid = [[],[],[],[],[],[],[],[],[]]
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
                newcols[icol].append(int(cell))
                grid_row = self.xlate_row[irow][icol]
                newgrid[grid_row].append(int(cell))
            newrows.append(newrow)
        return newrows, newcols, newgrid

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

    def build_grid_xlate_table(self):
        xlate_row = [[],[],[],[],[],[],[],[],[]]
        xlate_col = [[],[],[],[],[],[],[],[],[]]
        grid_row = '000111222000111222000111222333444555333444555333444555666777888666777888666777888'
        grid_col = '012012012345345345678678678012012012345345345678678678012012012345345345678678678'
        for i in range(0,81):
            row = i // 9
            col = i % 9
            xlate_row[row].append(int(grid_row[i]))
            xlate_col[col].append(int(grid_col[i]))
        return xlate_row, xlate_col

    def is_candidate(self, row, col, digit):
        if self.rows[row][col] != 0: return False
        if digit in self.rows[row]: return False
        if digit in self.cols[col]: return False
        if digit in self.grid[self.xlate_row[row][col]]: return False
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
        self.cols[col][row] = digit
        self.grid[self.xlate_row[row][col]][self.xlate_col[row][col]] = digit

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