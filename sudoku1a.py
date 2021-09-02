#!/usr/bin/env python
from Puzzle import Puzzle 
import sys
import time

"""
NOTE: This doesn't work
"""

candidate_cache = []

def calculate_candidate_cache(puzzle):
    global candidate_cache
    candidate_cache = []
    for row in range(0, 9):
        candidate_cache.append([])
        for col in range(0,9):
            candidate_cache[row].append(puzzle.get_candidates(row, col))

def solve(puzzle: Puzzle, row, col):
    global candidate_cache
    next_row, next_col = puzzle.next_cell(row, col)
    candidates = candidate_cache[row][col]
    print(row, col, candidates)
    orig_digit = puzzle.get(row, col)
    for candidate in candidates:
        if not puzzle.is_candidate(row, col, candidate): continue
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
    calculate_candidate_cache(puzzle)
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