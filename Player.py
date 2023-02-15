import math
import copy

class Player:

    amountPlayers = 0   #Temp number

    def __init__(self):
        Player.amountPlayers+=1             #increases the playernumber automatically depending on how many objects you create
        self.playerID = self.amountPlayers  

    
    def placeToken(self, board, inputCol, playerID = 0):
        if playerID == 0:
            playerID = self.playerID
        for row in range(board.row-1, -1, -1):      #Iterates through the array until the "lowest" (so that it appears as if the token is at the bottom of the board) free(with the value of 0) placement for a token can be found
            if board.fieldArr[row][inputCol] == 0:
                board.fieldArr[row][inputCol] = playerID
                break

class Computer(Player):
    def __init__(self):
        Player.__init__(self) #through calling it, the playerID increases for the computer too

    def minimax(self, board, depth, alpha, beta, maximizingPlayer) -> tuple:
        endRecursion = board.isTerminalNode()   #variable which holds the function to end the recursion

        if depth == 0 or endRecursion == True:  #If depth 0 has been reached or the recursion is == true

            if endRecursion == True:
                if board.evaluateScore(2):          
                    return (None, 1000000000000000)     #Really high number just to make sure that any score the evaluateScore() function produces, doesn't end up above the "winingScore"
                elif board.evaluateScore(1):
                    return (None, -1000000000000000)    #Same as above, just for the other direction. Plus/max or Minus/min scores are assigned to each of the two players.
                else: #No one wins
                    return (None, 0)
            else: 
                board.scoreValue = 0
                board.evaluateScore(2)
                return (None, board.scoreValue)

        if maximizingPlayer == True:
            value = -math.inf           #Infinity Value of the other direction depending on the function. Max gets -inf, min gets +inf
            column = 3                  #temp

            for col in range(board.column):
                if not board.checkFullCol(col):
                    boardCopy = copy.deepcopy(board)    #Creates a copy of the board with each calling so as to create every possible future tokenplacements in each board
                    self.placeToken(boardCopy, col, 2)  #Places token in the copy of the board
                    newScore = self.minimax(boardCopy, depth - 1, alpha, beta, False)[1] #Calls itself in the other direction, reduces the depth

                    if newScore > value:    #Should the new score be above the determined value (because we are trying to get the highest possible score in the maxmimizingPlayer part of this function)
                        value = newScore
                        column = col

                    #Alpha Beta Pruning. Don't test the paths of the "testing tree" which are already useless to test (because of the value it's gotten so far)
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break

            return column, value    #Return two variables
        
        else: #Minimizing Player, same as above only mirrored
            value = math.inf
            column = 3

            for col in range(board.column):
                if not board.checkFullCol(col):
                    boardCopy = copy.deepcopy(board)
                    self.placeToken(boardCopy, col, 1)
                    newScore = self.minimax(boardCopy, depth - 1, alpha, beta, True)[1]

                    if newScore < value:
                        value = newScore
                        #print(value, col)
                        column = col

                    beta = min(beta, value)
                    if alpha >= beta:
                        break

            return column, value
