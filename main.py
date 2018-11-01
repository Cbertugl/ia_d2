import constants
import csp
import sudoku


# ==================================================================================================
# MAIN
# ==================================================================================================
print("Sudoku is:")
S = sudoku.Sudoku.getSudokuFromFile("sudoku/1.txt")
S.display()

print("Trying to solve it...")
CSP = csp.CSP(S)
solvedSudoku = CSP.backtrackingSearch()

if(solvedSudoku != constants.FAILURE):
    print("Solved sudoku is:")
    solvedSudoku.display()
else: print("Failed to solve the sudoku... :-(")
