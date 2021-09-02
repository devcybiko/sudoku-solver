# sudoku-solver

This is a quick hack to solve Sudoku puzzles. It uses a recursive descent / depth-first algorithm to exhaust all possible candidates.

Each cell is visited and analyzed for possible candidates (looking horizontally, vertically, and in the subgrid to select digits that are not already represented).

The first candidate is added to the puzzle and the next cell is visited (working left to right, from top to bottom). That cell also selects a list of candidates and tries its first one, and calls the next cell, recursively.

If we get to a place in the recursion where no candidates exist, or if a "child" cell returns a 'False', a False is returned and the "parent" (or previous) cell - which tries its next candidate.

If a cell exhausts all its possible candidates, then it returns False to the parent which tries its next candidate and the process repeats.

If the last cell is visited and it successfully places one of its candidates, the puzzle is considered 'solved' and a True is passed up to the parents, unwinding the recursion. The algorithm then halts. If other solutions are possible, this algorithm will not find them.

**NOTE** The recursive code to solve the puzzle is in `sudoku1.py`. It rightly might belong in the `Puzzle.py` class. However, I wanted to isolate the solution code in its own file. Also, I am thinking of writing a non-recursive version and putting it in a separate source file.

## Installing
* `make install`

## Running unit tests / code coverage
* `make coverage` - run all tests and code coverage
* `make report` - generate HTML report on coverage

## Run it
* `./sudoku1.py <filename>`

or

* `run-all.sh`

## Sample puzzles were from this link - some are very hard
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
* puzzle-*.json - puzzle files
* requirements.txt - required Python libraries
* run-all.sh - script to run all puzzles
* solved-01.json - a solved puzzle for unit tests
* sudoku1.py - main code
* tests/ - test cases

## Implementation notes
1. In `Puzzle.get_candiates()` I return a single candidate if the cell is already occupied. While this introduces some inefficiencies, it greatly simplified the recursion

2. This is not necessarily a very efficient solution. I opted for clarity in the code over more optimal methods. For example, I could have iterated over every cell and computed the candidates (`Puzzle.get_candidates()`) once at the very beginning (rather than during the recursion) and reused them.
