import math

class PlayingBoard:
    def __init__(self, column = 7, row = 6):
        self.column = column
        self.row = row
        self.fieldArr: int = [[0 for j in range(self.column)] for i in range(self.row)] # Fill a column x row 2D Array with 0's
        self.winningPos = [""] * 4  #Array for the positions of the winning tokens
        self.scoreValue = 0         #Set to 0 at the start

    def checkFull(self):    #Iterates through the "highest" (in terms of looking at the playingboard) position and checks if its filled with a token. If all are filled, then the board must be full
        for columns in range(self.column):
            if self.fieldArr[0][columns] == 0:
                return False
        return True

    def checkFullCol(self, inputCol):   #Checks if one column of the board is filled by merely looking at the top position of the chosen column
        if self.fieldArr[0][inputCol] == 0:
            return False
        else:
            return True


    def evaluateScore(self, playerID) -> bool:

        def checkPosition(row, column, xPos, yPos) -> bool:
            winCounter = 0  #Temp
            
            for tokens in range(4):                         #4 tokens in one row determine a win
                if self.fieldArr[row][column] == playerID:  #First loop=Uses the initial values, After that=Uses the changed values below by using the xyPos Variables
                    winCounter += 1                         #Necessary for the score below
                    self.winningPos[tokens] = row, column   #Fill the list with row/col or x/y positions of the tokens of one player in a row
                
                #Still part of the loop, checks the token next to the initial/previous one by increasing the direction
                row += yPos     #Can be +1 or +0
                column += xPos  #Can be +1 or +0
                
            #Gives a connected row of tokens a score determined by how many tokens of one player are in a connected row
            if winCounter >= 4:
                return True     #Someone won
            elif winCounter == 3:
                self.scoreValue += 2
            elif winCounter == 2:
                self.scoreValue += 1

            return False        #No one won yet

        for row in range(self.row):
            for column in range(self.column):
                #Vertical |
                if row < self.row - 3 and checkPosition(row, column, 0, 1):             #Check yPos + 1 (one step down)
                    return True     #Win
                #Horizontal -
                elif column < self.column - 3 and checkPosition(row, column, 1, 0):     #Check xPos + 1 (one step to the right)
                    return True     #Win
                #Diagonal Up /
                elif row < self.row - 3 and column < self.column - 3 and checkPosition(row, column, 1, 1):  #Check X&Y (one step right and up) 
                    return True     #Win
                #Diagonal Down \
                elif row >= 3 and column < self.column - 3 and checkPosition(row, column, 1, -1):  #Check X&Y (One step right and down)
                    return True     #Win
        return False    #No one won yet / Continue the game

    def isTerminalNode(self) -> bool:
        return self.evaluateScore(1) or self.evaluateScore(2) or self.checkFull()       #Needs one True to stop the recursion