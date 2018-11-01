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
    def __generateVariablesAndConstraints(self):
        size = constants.GRID_SIZE

        # On crée une grille de variable temporaire pour les associer aux Tiles
        grid = self.assignment.getGrid()
        variableGrid = [[Variable(grid[j][i]) for i in range(size)] for j in range(size)]

        # On ajoute les variables au CSP
        for i in range(size):
            for j in range(size):
                self.variables.append(variableGrid[i][j])

        # On crée les contraintes sur chaque ligne
        for i in range(size):
            row = variableGrid[i]

            for j in range(size):
                variableOne = row[j]

                for k in range(j + 1, size):
                    variableTwo = row[k]
                    constraint = NotEqualConstraint(variableOne, variableTwo)
                    self.constraints.append(constraint)
                    variableOne.addConstraint(constraint)
                    variableTwo.addConstraint(constraint)

        # On crée les contraintes sur chaque colonne
        for i in range(size):
            column = []
            for row in variableGrid:
                column.append(row[i]) 

            for j in range(size):
                variableOne = column[j]

                for k in range(j + 1, size):
                    variableTwo = column[k]
                    constraint = NotEqualConstraint(variableOne, variableTwo)
                    self.constraints.append(constraint)
                    variableOne.addConstraint(constraint)
                    variableTwo.addConstraint(constraint)

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
                            if(p[0].object.getPosition() == squareList[q][1].object.getPosition()): toRemove.append(squareList[q])

                    i += 1

                toRemove = set(toRemove)
                for p in toRemove:
                    squareList.remove(p)

                # On ajoute les contraintes restantes du carré
                for p in squareList:
                    variableOne = p[0]
                    variableTwo = p[1]
                    constraint = NotEqualConstraint(variableOne, variableTwo)
                    self.constraints.append(constraint)
                    variableOne.addConstraint(constraint)
                    variableTwo.addConstraint(constraint)

    def __isAssignementComplete(self):
        for v in self.variables:
            if(not v.isSet()): return False

        return True

    def __getUnassignedVariable(self):

        # Minimum remining values

        mrv = len(constants.Domain)
        init = True
        
        # For each variable
        for var in self.variables:
            
            # If the value is not set
            if not var.isSet():
                # Initialisation of return object
                if init == True:
                    mrvVar = var
                    init = False
                    
                # If the remaining value is less than the current mrv, then we update the mrv and the return object
                if var.getDomainLength() < mrv:
                    mrv = var.getDomainLength()
                    mrvVar = var
                    
                # Degree heurisitic : choosing the variable with the most constaints
                if var.getDomainLength() == mrv and mrv < len(constants.Domain):
                    if var.getNbConstraints() > mrvVar.getNbConstraints():
                        mrvVar = var

        return mrvVar

    def __orderDomainValues(self, var):
        # Least constraining value
        domain = []
        constrainingRatio = []
        
        for value in constants.Domain.getAsArray():
          # copie de la variable couple dans la contrainte pour ne pas modifier la vrai valeur 
          varCopy = None
          sumOfDomainsLength = 0 # comptage du nombre de possibilité du domaine de chaque variable couple de la contrainte sur laquelle on travaille
          # on parcourt chacune des contraintes
          for constraint in var.getConstraints() :
            varCopy = constraint.variableTwo # on fait une copie de la variable 'couple' de la contrainte sur laquelle on travaille
            if value in varCopy.getDomain() : # on regarde si la valeur qu'on a choisit va influencer le domaine de cette variable
              varCopy.removeFromDomain(value) # si oui on la retire de la copie 
            sumOfDomainsLength += varCopy.getDomainLength() # on additionne pour chaque contrainte la taille du domaine associé

          # Avec ces données, on arrange dans un tableau les valeurs qui diminue le moins possible les domaines des autres variables
          if len(constrainingRatio) == 0 :
            domain.append(value)
            constrainingRatio.append(sumOfDomainsLength)
          else :
            for pos , sumValue in enumerate(constrainingRatio) :
              if sumOfDomainsLength > sumValue : # si, pour la valeur de travaille, on trouve que la taille totale des domaines est plus grande, on positionne avant dans le tableau 
                domain.insert(pos,value)
                constrainingRatio.insert(pos,sumOfDomainsLength)
              if pos + 1 == len(constrainingRatio) :
                domain.append(value)
                constrainingRatio.append(sumOfDomainsLength)
                break # sinon pos s'indente et len(constrainingRatio) de meme -> donc boucle infini

        return domain
        # return constants.Domain.getAsArray()

    def __isConsistentWithValue(self, var, value):
        var.setValue(value)

        for c in var.getConstraints():
            if(not c.check()):
                var.removeValue()
                return False

        var.removeValue()
        return True

    # ================================================================================================
    # PUBLIC FUNCTIONS
    # ================================================================================================
    def displayVariables(self):
        for v in self.variables:
            v.displayConstraints()

 
    def backtrackingSearch(self):
        if(self.__isAssignementComplete()): return self.assignment
        
        var = self.__getUnassignedVariable()
        for value in self.__orderDomainValues(var):
            if(self.__isConsistentWithValue(var, value)):
                var.setValue(value)
                
                # Refreshing arc consistency
                self.arcConsistency()

                result = self.backtrackingSearch()
                if(result != constants.FAILURE): return result
                
                var.removeValue()
        
        return constants.FAILURE
    
    
    def arcConsistency(self):
        queue = self.constraints
        
        # For each arc (same as constraints here)
        while queue:
            arc = queue.pop()
            
            # Checking inconsistent values. If any found, we need to check every other arc of the variable who saw his domain shrink
            if self.removeInconsistentValues(arc.variableOne,arc.variableTwo):
                for constraint in arc.variableOne.getConstraints():
                    if constraint not in queue:
                        queue.append(constraint)

    
    #NOTE: Une remodélisation du système de contrainte doit être fait pour généraliser la fonction correctement à l'image du cours. A faire si possible.
    def removeInconsistentValues(self,varI, varJ):
        removed = False
        
        # For each remaining value available for I
        for valueI in varI.getDomain():
            check = False
            
            # For each remaining value available for J
            for valueJ in varJ.getDomain():
                # If the constraint between the two variables can be satisfied (always not equal), we try the next I value
                if(valueI != valueJ):
                    check = True
                    break
            # If no suitable value can be found in the restrained J domain, then the I value can't be chosed and must be removed
            if check == False :
                varI.removeFromDomain(valueI)
                removed = True
        
        # Is true if any variable has been removed from the variable I, false otherwise
        return removed



    # def minimumRemainingValues(self):
    #   assert len(self.variables) > 0
    #   variableChosen = None
    #   remainingValuesV = 10
    #   for variable in self.variables :
    #     if not variable.isSet() :
    #       remainingValues = 9
    #       possibleValuesDomain = []
    #       for constraint in variable.getConstraints() :
    #         # Il n'y a au maximum qu'une seule variable ici qui sera différente de zéro 
    #         if constraint.variableOne.getValue() != constants.NO_VALUE :
    #           if not constraint.variableOne.getValue() in possibleValuesDomain :
    #             possibleValuesDomain.append(constraint.variableOne.getValue())
    #             remainingValues -= 1
    #         if constraint.variableTwo.getValue() != constants.NO_VALUE :
    #           if not constraint.variableTwo.getValue() in possibleValuesDomain :
    #             possibleValuesDomain.append(constraint.variableTwo.getValue())
    #             remainingValues -= 1
    #       if remainingValues < remainingValuesV :
    #         variableChosen = variable
    #         remainingValuesV = remainingValues
    #   return variableChosen





class Variable:
    def __init__(self, object):
        self.object = object
        self.constraints = []
        # Remaining domain values of the variable, initialised as the entierty of domain values
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

    def getConstraints(self):
        return self.constraints
    
    #def getConstraint(self,var):
    #    for c in self.constraints:
    #        if (c.variableOne == self and c.variableTwo = var) or (c.variableTwo = self and c.variableOne = var):
    #            return c
    #    return constants.FAILURE

    def displayConstraints(self):
        print("Case", self.object.getPosition(), end = "")
        if(self.isSet()) :print("; valeur", self.getValue(), end = "")
        print(";", self.getNbConstraints(), "contraintes")
        for c in self.constraints:
            if(c.variableOne == self): print(c.variableTwo.object.getPosition(), end = ", ")
            else : print(c.variableOne.object.getPosition(), end = ", ")
        print(end = "\n\n")
        
    # Get the remaining domain values of the variable    
    def getDomain(self):
        return self.domain    
    
    # Remove a given value from the remaining domain values of the variable
    def removeFromDomain(self, value):
        self.domain.remove(value)
        
    # Get the number of remaining domain values of the variable
    def getDomainLength(self):
        return len(self.domain)


class NotEqualConstraint:
    def __init__(self, variableOne, variableTwo):
        self.variableOne = variableOne
        self.variableTwo = variableTwo

    def check(self):
        if(
            self.variableOne.getValue() == constants.NO_VALUE or
            self.variableTwo.getValue() == constants.NO_VALUE
        ):
            return True

        return(self.variableOne.getValue() != self.variableTwo.getValue())

