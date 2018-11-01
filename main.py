import constants
import csp
import sudoku
import time


# ==================================================================================================
# MAIN
# ==================================================================================================
print("Sudoku is:")
S = sudoku.Sudoku.getSudokuFromFile("sudoku/1.txt")
S.display()

print("Trying to solve it...\n")
elapsedTime = -time.time()
CSP = csp.CSP(S)
solvedSudoku = CSP.backtrackingSearch()
elapsedTime += time.time()

print("Finished in ", elapsedTime,"s, ", sep = "", end = "")
if(solvedSudoku != constants.FAILURE):
    print("solved sudoku is:")
    solvedSudoku.display()
else: print("failed to solve the sudoku... :-(")
