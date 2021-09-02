# sudoku-solver

This is a quick hack to solve Sudoku puzzles. It uses a recursive descent / depth-first algorithm to exhaust all possible candidates.

Each cell is visited and analyzed for possible candidates (looking horizontally, vertically, and in the subgrid to select digits that are not already represented).

The first candidate is added to the puzzle and the next cell is visited (going from top to bottom, left to right). That cell also selects a list of candidates and tries its first one, recursively.

If we get to a place in the recursion where no candidates exist, or if a "child" cell returns a 'False', a False is returned and the "parent" (or previous) cell - which tries its next candidate.

If a cell exhausts all its possible candidates, then it returns False to the parent which tries its next candidate and the process repeats.

## Installing
* make -f Makefile install

## Running unit tests / code coverage
* make -f Makefile coverage
* make -f Makefile report

## Run it
`./sudoku1.py <filename>`
or
`run-all.sh`

## Some puzzles to try - some are very hard
* https://www.rd.com/list/printable-sudoku-puzzles/

## Input file format
The input file is a JSON array of strings. Empty cells are represented by a single dash. Each line should have exactly 9 characters, and the array should be exactly 9 lines long.

```json
[
    "-7--2--46",
    "-6----89-",
    "2--8--715",
    "-84-97---",
    "71-----59",
    "---13-48-",
    "697--2--8",
    "-58----6-",
    "43--8--7-"
]

```
## Files
* Makefile - makefile
* Puzzle.py - Puzzle class (holds puzzle and its methods)
* README.md - this file
* puzzle-01.json
* puzzle-02.json
* puzzle-03.json
* puzzle-04.json
* puzzle-05.json
* puzzle-06.json
* puzzle-07.json
* puzzle-08.json
* puzzle-09.json
* puzzle-10.json
* requirements.txt - required Python libraries
* run-all.sh - script to run all puzzles
* sudoku1.py - main code
* tests/ - test cases

## Implementation notes
1. In `Puzzle.get_candiates()` I return a single candidate if the cell is already occupied. While this introduces some inefficiencies, it greatly simplified the recursion

