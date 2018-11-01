import constants
import csp
import sudoku
import time


# ==================================================================================================
# MAIN
# ==================================================================================================

# Displaying the sudoku before the resolution
print("Sudoku is:")
S = sudoku.Sudoku.getSudokuFromFile("sudoku/1.txt")
S.display()

# Resolving the sudoku and keeping track of time
print("Trying to solve it...\n")
elapsedTime = -time.time()
CSP = csp.CSP(S)
solvedSudoku = CSP.backtrackingSearch()
elapsedTime += time.time()

# Displaying the solution
print("Finished in ", elapsedTime,"s, ", sep = "", end = "")
if(solvedSudoku != constants.FAILURE):
    print("solved sudoku is:")
    solvedSudoku.display()
else: print("failed to solve the sudoku... :-(")
