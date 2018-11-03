import constants
import itertools
import random

class CSP:

    # ================================================================================================
    # CONSTRUCTOR
    # ================================================================================================
    def __init__(self, sudoku):
        self.assignment = sudoku
        self.domain = constants.Domain
        self.variables = []
        self.constraints = []
        self.__generateVariablesAndConstraints()

    # ================================================================================================
    # PRIVATE FUNCTIONS
    # ================================================================================================
    def __addNotEqualConstraint(self, var1, var2):
        constraint = NotEqualConstraint(var1, var2)
        self.constraints.append(constraint)
        var1.addConstraint(constraint)
        var2.addConstraint(constraint)

    def __generateVariablesAndConstraints(self):
        size = constants.GRID_SIZE

        # On crée une grille de variable temporaire pour les associer aux Tiles
        grid = self.assignment.getGrid()
        variableGrid = [[Variable(grid[j][i]) for i in range(size)] for j in range(size)]

        # On crée les contraintes sur chaque ligne et chaque colonne
        for i in range(size):
            # Ligne
            row = variableGrid[i]
            # Colonne
            column = []
            for rowTmp in variableGrid:
                column.append(rowTmp[i])

            for j in range(size):
                # On ajoute la variable au CSP
                self.variables.append(variableGrid[i][j])
                
                for k in range(j + 1, size):
                    # Ligne
                    self.__addNotEqualConstraint(row[j], row[k])
                    # Colonne
                    self.__addNotEqualConstraint(column[j], column[k])

        # On crée les contraintes dans chaque carré
        for squareI in range(3):
            for squareJ in range(3):
                square = []
                for i in range(3):
                    for j in range(3):
                        square.append(variableGrid[squareI * 3 + i][squareJ * 3 + j])
                    
                # On génère toutes les paires de case possible dans un carré
                squareList = list(itertools.product(square, square))

                # On enlève les paires avec deux cases sur la même ligne et/ou la même colonne
                # et les paires symétriques
                toRemove = []
                i = 0
                for p in squareList:
                    if(
                        p[0].object.getPosition()[0] == p[1].object.getPosition()[0] or
                        p[0].object.getPosition()[1] == p[1].object.getPosition()[1]
                    ):
                        toRemove.append(p)
                    else:
                        for q in range(i + 1, squareList.__len__()):
                            if(p[0].object.getPosition() == squareList[q][1].object.getPosition()):
                                toRemove.append(squareList[q])

                    i += 1

                toRemove = set(toRemove)
                for p in toRemove:
                    squareList.remove(p)

                # On ajoute les contraintes restantes du carré
                for p in squareList:
                    self.__addNotEqualConstraint(p[0], p[1])

    def __isAssignementComplete(self):
        for v in self.variables:
            if(not v.isSet()): return False

        return True

    def __getUnassignedVariable(self):
        # Minimum remaining values
        variableChosen = None
        remainingValuesV = 10
        for variable in self.variables :
            if not variable.isSet() :
                remainingValues = 9
                possibleValuesDomain = []
                for constraint in variable.getConstraints() :
                    # Il n'y a au maximum qu'une seule variable ici qui sera différente de zéro
                    if constraint.variableOne.getValue() != constants.NO_VALUE :
                        if not constraint.variableOne.getValue() in possibleValuesDomain :
                            possibleValuesDomain.append(constraint.variableOne.getValue())
                            remainingValues -= 1
                    if constraint.variableTwo.getValue() != constants.NO_VALUE :
                        if not constraint.variableTwo.getValue() in possibleValuesDomain :
                            possibleValuesDomain.append(constraint.variableTwo.getValue())
                            remainingValues -= 1
                if remainingValues < remainingValuesV :
                    variableChosen = variable
                    remainingValuesV = remainingValues
                # Degree heuristic : choosing the variable with the most constaints
                elif remainingValues == remainingValuesV :
                    if variableChosen.getNbRemainingConstraints() < variable.getNbRemainingConstraints()  :
                        variableChosen = variable
                        remainingValuesV = remainingValues
        return variableChosen

    # Least constraining value
    def __orderDomainValues(self, var):
        domain = []
        constrainingRatio = []
        for value in var.getDomain():
            # comptage du nombre de possibilité du domaine de chaque variablecouple de la
            # contrainte sur laquelle on travaille
            sumOfDomainsLength = 0
            # on parcourt chacune des contraintes
            for constraint in var.getConstraints() :
                # copie du domaine de la variable couple dans la contrainte pour ne pas
                # modifier la vraie valeur     
                domainCopy = None
                # false = passer à la contrainte suivante pour ne pas prendre en compte celles 
                # qui ont deja une valeur
                continu = True
                if constraint.variableOne == var : 
                    if constraint.variableTwo.isSet(): continu = False
                    else :
                        # on fait une copie du domaine de la variable 'couple' de la contrainte
                        # sur laquelle on travaille
                        domainCopy = constraint.variableTwo.getDomain().copy()
                else :
                    if constraint.variableOne.isSet(): continu = False 
                    else :
                        domainCopy = constraint.variableOne.getDomain().copy()
                if continu :
                    present = False
                    # on regarde si la valeur qu'on a choisit va influencer le domaine de cette variable
                    if value in domainCopy :
                        present = True
                    if present : 
                        domainCopy.remove(value) # si oui on la retire de la copie 
                    sumOfDomainsLength += len(domainCopy) 
            # Avec ces données, on arrange dans un tableau les valeurs qui diminuent le moins possible
            # les domaines des autres variables
            if len(constrainingRatio) == 0 :
                domain.append(value)
                constrainingRatio.append(sumOfDomainsLength)
            else :
                for pos , sumValue in enumerate(constrainingRatio) :
                    # si, pour la valeur de travaille, on trouve que la taille totale des domaines est
                    # plus grande, on positionne avant dans le tableau 
                    if sumOfDomainsLength > sumValue :
                        domain.insert(pos,value)
                        constrainingRatio.insert(pos,sumOfDomainsLength)
                        break # sinon pos s'indente et len(constrainingRatio) de meme -> donc boucle infini
                    if pos + 1 == len(constrainingRatio) :
                        domain.append(value)
                        constrainingRatio.append(sumOfDomainsLength)
                        break # sinon pos s'indente et len(constrainingRatio) de meme -> donc boucle infini
        return domain

    def __isConsistentWithValue(self, var, value):
        var.setValue(value)

        for c in var.getConstraints():
            if(not c.check()):
                var.removeValue()
                return False

        var.removeValue()
        return True

    def __arcConsistency(self):
        queue = self.constraints.copy()
        
        # For each arc (same as constraints here)
        while queue:
            arc = queue.pop()
            
            # Checking inconsistent values. If any found, we need to check
            # every other arc of the variable who saw his domain shrink
            if self.__removeInconsistentValues(arc.variableOne, arc.variableTwo, arc):
                for constraint in arc.variableOne.getConstraints():
                    if constraint not in queue:
                        queue.append(constraint)

    # The constraint between varI and varJ is given to avoid looking for it
    def __removeInconsistentValues(self, varI, varJ, constraint):
        removed = False
        
        # For each remaining value available for I
        for valueI in varI.getDomain():
            check = False
            
            # For each remaining value available for J
            for valueJ in varJ.getDomain():
                # If the constraint between the two variables can be satisfied,
                # we try the next I value
                if(constraint.tryConstraint(valueI, valueJ)):
                    check = True
                    break

            # If no suitable value can be found in the restrained J domain,
            # then the I value can't be choosen and must be removed
            if check == False :
                varI.removeFromDomain(valueI)
                removed = True
        
        # True if any variable has been removed from the variable I, false otherwise
        return removed

    # ================================================================================================
    # PUBLIC FUNCTIONS
    # ================================================================================================
    def displayVariables(self):
        for v in self.variables:
            v.display()

    def backtrackingSearch(self):
        if(self.__isAssignementComplete()): return self.assignment

        # Refreshing arc consistency
        self.__arcConsistency()
        
        var = self.__getUnassignedVariable()
        for value in self.__orderDomainValues(var):
            if(self.__isConsistentWithValue(var, value)):
                var.setValue(value)

                result = self.backtrackingSearch()
                if(result != constants.FAILURE): return result
                
                var.removeValue()
        
        return constants.FAILURE


class Variable:

    def __init__(self, object):
        self.object = object
        self.constraints = []
        # Remaining domain values of the variable, initialised as the entirety of domain values
        self.domain = constants.Domain.getAsArray()

    def isSet(self):
        return(self.getValue() != constants.NO_VALUE)

    def getValue(self):
        return self.object.getValue()

    def setValue(self, value):
        self.object.setValue(value)

    def removeValue(self):
        self.setValue(constants.NO_VALUE)

    def addConstraint(self, constraint):
        self.constraints.append(constraint)

    def getNbConstraints(self):
        return self.constraints.__len__()

    def getNbRemainingConstraints(self):
        valideConstraints = 0
        for constraint in self.getConstraints() :
            if not (
                constraint.variableOne.getValue() == constants.NO_VALUE and
                constraint.variableTwo.getValue() == constants.NO_VALUE
            ): valideConstraints += 1
        return valideConstraints

    def getConstraints(self):
        return self.constraints

    # Get the remaining domain values of the variable    
    def getDomain(self):
        if(self.isSet()): return [self.getValue()]
        return self.domain
    
    # Remove a given value from the remaining domain values of the variable
    def removeFromDomain(self, value):
        if not self.isSet(): self.domain.remove(value)
            
    # Get the number of remaining domain values of the variable
    def getDomainLength(self):
        return len(self.getDomain())

    def display(self):
        print("Case", self.object.getPosition(), end = "")
        print(";", self.getNbConstraints(), "contraintes", end = "")
        if(self.isSet()): print("; valeur", self.getValue(), end = "")
        else: print("; domaine", self.domain, end = "")
        print()

    def displayConstraints(self):
        print("Case", self.object.getPosition(), end = ": ")
        for c in self.constraints:
                if(c.variableOne == self): print(c.variableTwo.object.getPosition(), end = ", ")
                else : print(c.variableOne.object.getPosition(), end = ", ")
        print()


class NotEqualConstraint:

    def __init__(self, variableOne, variableTwo):
        self.variableOne = variableOne
        self.variableTwo = variableTwo

    # Try the constraint with two values
    @staticmethod
    def tryConstraint(valueOne, valueTwo):
        if(
            valueOne == constants.NO_VALUE or
            valueTwo == constants.NO_VALUE
        ):
            return True

        return(valueOne != valueTwo)

    def check(self):
        return NotEqualConstraint.tryConstraint(
            self.variableOne.getValue(),
            self.variableTwo.getValue()
        )
