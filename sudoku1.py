#!/usr/bin/env python
from Puzzle import Puzzle 
import sys
import time

def solve(puzzle: Puzzle, row, col):
    next_row, next_col = puzzle.next_cell(row, col)
    candidates = puzzle.get_candidates(row, col)
    orig_digit = puzzle.get(row, col)
    for candidate in candidates:
        puzzle.set(row, col, candidate)
        if next_row >= 9: return True
        solved = solve(puzzle, next_row, next_col)
        if solved: return True
    puzzle.set(row, col, orig_digit)
    return False

def main():
    fname = len(sys.argv) > 1 and sys.argv[1] or 'puzzle-01.json'
    puzzle = Puzzle(fname)
    print("\n")
    print(fname)
    puzzle.print()
    print("\n")
    then = time.time()
    solved = solve(puzzle, 0, 0)
    now = time.time()
    delta = str(round(now-then, 2))
    if not solved:
        print(fname + " is unsolvable... in " + delta + " secs")
    else:
        puzzle.print() 
        print(fname + " solved in " + delta + " secs")
    print("\n")

main()