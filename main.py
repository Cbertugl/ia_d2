import constants
import csp
import sudoku


# ==================================================================================================
# MAIN
# ==================================================================================================
S = sudoku.Sudoku.getSudokuFromFile("sudoku/1.txt")
S.display()

CSP = csp.CSP(S)

solvedSudoku = CSP.backtrackingSearch()

if(solvedSudoku != constants.FAILURE): solvedSudoku.display()
else: print("Failed to solve the sudoku... :-(")
