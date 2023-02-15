from tkinter import *
from PlayingBoard import PlayingBoard
from Player import Player
from Player import Computer
import constants
import math
import threading

class Game:
    def __init__(self):
        self.turnOf = 0 #Switches between 1 (Player 1) and 2 (Player 2)
        self.playerList = [] #Will be filled with the Player Objects
        self.gameStatus = 0 #0=running, 1 = win, 2 = draw
        self.difficulty = 6 #Difficulty/Depth Level of the AI, always set high

    def changeTurn(self): #Just changes between 1 and 2 for Player 1 and 2 after every successful turn
        if self.turnOf == 1:
            self.turnOf = 2
        elif self.turnOf == 2:
            self.turnOf = 1

    def checkDraw(self, board): #It's its own function so as to not change the status during the testing of all AI moves, because it (basically) brute-forces every possible move which would eventually result in a "draw". Which we don't want because the AI should only predict.
        if board.checkFull(): #Calls the function that checks if the Gameboard is filled
            self.gameStatus = 2 #Sets the game to "Draw" if the Gameboard has been filled

    def checkWin(self, board, playerID):
        if  board.evaluateScore(playerID): #Checks the entire board for a 4+ row of Tokens of the player with the playerID
            self.gameStatus = 1 #Sets Status to "win"
            self.winner = playerID #Setts the winner to its own Variable
   
class HoverButton(Button):
    def __init__(self, master, col, deselectArrowBtn, selectArrowBtn, **kw):
        Button.__init__(self,master=master, background = constants.BGCOLOR, activebackground = constants.BGCOLOR, **kw)
        self.deselectArrowBtn = deselectArrowBtn
        self.selectArrowBtn = selectArrowBtn

        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.config(image=self.deselectArrowBtn, bg=constants.BGCOLOR, bd=0, activebackground = constants.BGCOLOR, state='normal')

    #Eventfunctions of the Class. They change the image of the buttons depending on if you hover over it or not
    def on_enter(self, e):
        self.config(image=self.selectArrowBtn)

    def on_leave(self, e):
        self.config(image=self.deselectArrowBtn)

class myGUI:
    def __init__(self):
        #Declaration of the necessary objects
        self.game = Game()
        self.board = PlayingBoard()

        #tkinter relevant parameters/settings
        self.window = Tk()
        self.window.state('zoomed')
        self.window.title("Connect Four")
        self.window.configure(background = constants.BGCOLOR)

        self.circleArr: int = [[0 for j in range(self.board.column)] for i in range(self.board.row)] #Creates array for the images of the playingboard. Each position in the array is its own image
        self.arrowArr: int = [0]*self.board.column# Array for the row of interactable buttons above the playingboard

        #----Frames
        #Area to the left of the playingboard; displays whose turn it currently is
        self.leftFrame = Frame(self.window, width=400, height=720, bg=constants.BGCOLOR)
        self.leftFrame.grid(row=0, column=0, padx=(95,0), pady=5)

        #Area of the playingboard
        self.rightFrame = Frame(self.window, width=880, height=720, bg=constants.BGCOLOR)
        self.rightFrame.grid(row=0, column=1, padx=(160, 0), pady=(120,0))

        #Area of the buttons at the start of the game; left of the playingboard
        self.btnFrame = Frame(self.leftFrame, width=400, height=500,bg=constants.BGCOLOR)
        self.btnFrame.grid(row=1, column=0, pady=(30,0))
        #----Logo
        self.logo = PhotoImage(file="img/logo.png")
        Label(self.leftFrame, image=self.logo, bg=constants.BGCOLOR).grid(row=0, column=0, padx=5, pady=(70, 0))
        
        #----Select Buttons
        Label(self.btnFrame, text="Modus:", bg=constants.BGCOLOR, fg=constants.FONTCOLOR, font=constants.LABELFONT).grid(row=2, column=0, pady=(0, 3), sticky=SW)
        self.modeDiv = StringVar()   #Container, stores the value of specific widgets within themselves, "groupname" basically
        self.modeDiv.set(0)          #The first button will be selected
        self.modeOneBtn = Radiobutton(self.btnFrame, text="Spieler VS Spieler", variable=self.modeDiv, bg=constants.BLUEUNSELECTCOLOR, selectcolor=constants.BLUESELECTCOLOR, activebackground=constants.BLUECLICKCOLOR, fg=constants.FONTCOLOR, activeforeground=constants.FONTCOLOR, font=constants.BUTTONFONT)
        self.modeOneBtn.config(indicatoron=0, width=30, height=1, pady = 7,value=0, relief=FLAT)
        self.modeOneBtn.grid(row=3, column=0, pady= 5, ipady=0)
        self.modeTwoBtn = Radiobutton(self.btnFrame, text="Spieler VS CPU", variable=self.modeDiv, bg=constants.BLUEUNSELECTCOLOR, selectcolor=constants.BLUESELECTCOLOR, activebackground=constants.BLUECLICKCOLOR, fg=constants.FONTCOLOR, activeforeground=constants.FONTCOLOR, font=constants.BUTTONFONT)
        self.modeTwoBtn.config(indicatoron=0, width=30, height=1, pady = 7,value=1, relief=FLAT)
        self.modeTwoBtn.grid(row=4, column=0, pady= 5)

        Label(self.btnFrame, text="Wer beginnt?", bg=constants.BGCOLOR, fg=constants.FONTCOLOR, font=constants.LABELFONT).grid(row=5, column=0, pady=(20, 3), sticky=SW)
        self.turnDiv = StringVar()   #Container, stores the value of specific widgets within themselves, "groupname" basically
        self.turnDiv.set(1)          #The first button will be selected
        self.turnOneBtn = Radiobutton(self.btnFrame, text="Spieler 1 - Mensch", variable=self.turnDiv, bg=constants.ORANGEUNSELECTCOLOR, selectcolor=constants.ORANGESELECTCOLOR, activebackground=constants.ORANGECLICKCOLOR, fg=constants.FONTCOLOR, activeforeground=constants.FONTCOLOR, font=constants.BUTTONFONT)
        self.turnOneBtn.config(indicatoron=0, width=30, height=1, pady = 7,value=1)
        self.turnOneBtn.grid(row=6, column=0, pady= 5)
        self.turnTwoBtn = Radiobutton(self.btnFrame, text="Spieler 2 - Mensch/CPU", variable=self.turnDiv, bg=constants.ORANGEUNSELECTCOLOR, selectcolor=constants.ORANGESELECTCOLOR, activebackground=constants.ORANGECLICKCOLOR, fg=constants.FONTCOLOR, activeforeground=constants.FONTCOLOR, font=constants.BUTTONFONT)
        self.turnTwoBtn.config(indicatoron=0, width=30, height=1, pady = 7,value=2, relief="ridge")
        self.turnTwoBtn.grid(row=7, column=0, pady= 5)

        self.submitBtn = Button(self.btnFrame, text="Bestätigen", bg=constants.FONTCOLOR, fg=constants.BGCOLOR, font=constants.BUTTONFONT, activebackground=constants.SUBMITCLICKCOLOR, command = lambda: self.startGame())
        self.submitBtn.config(width=30, height=1, pady = 1)
        self.submitBtn.grid(row=8, column=0, pady=(25, 10))

        self.playerBox = Label(self.leftFrame)

        #----Draw Playingboard
        self.deselectArrowBtn = PhotoImage(file="img/deselectArrow.png")
        self.selectArrowBtn = PhotoImage(file="img/selectArrow.png")
        self.playingBoardCanv = Canvas(self.rightFrame, width=1000, height=720)

        #Function to draw a circle for the playingboard
        def create_circle(x, y, r, color, canvasName): #center coordinates, radius
            x0 = x - r
            y0 = y - r
            x1 = x + r
            y1 = y + r
            return canvasName.create_oval(x0, y0, x1, y1, fill=color, outline="")

        #Declaring of the Arrow Buttons at the top with the necessary function
        self.arrowArr[0] = HoverButton(self.rightFrame, 0, self.deselectArrowBtn, self.selectArrowBtn, command=lambda:self.startPlaceTokenThread(0))
        self.arrowArr[1] = HoverButton(self.rightFrame, 1, self.deselectArrowBtn, self.selectArrowBtn, command=lambda:self.startPlaceTokenThread(1))
        self.arrowArr[2] = HoverButton(self.rightFrame, 2, self.deselectArrowBtn, self.selectArrowBtn, command=lambda:self.startPlaceTokenThread(2))
        self.arrowArr[3] = HoverButton(self.rightFrame, 3, self.deselectArrowBtn, self.selectArrowBtn, command=lambda:self.startPlaceTokenThread(3))
        self.arrowArr[4] = HoverButton(self.rightFrame, 4, self.deselectArrowBtn, self.selectArrowBtn, command=lambda:self.startPlaceTokenThread(4))
        self.arrowArr[5] = HoverButton(self.rightFrame, 5, self.deselectArrowBtn, self.selectArrowBtn, command=lambda:self.startPlaceTokenThread(5))
        self.arrowArr[6] = HoverButton(self.rightFrame, 6, self.deselectArrowBtn, self.selectArrowBtn, command=lambda:self.startPlaceTokenThread(6))

        #Drawing of the circles in the playingboard
        self.x_Pos = 0
        self.y_Pos = 70
        for row in range(len(self.board.fieldArr)): 
            self.x_Pos = 0
            for col in range(len(self.board.fieldArr[row])): 
                self.x_Pos = self.x_Pos + 125
                self.circleArr[row][col] = create_circle(self.x_Pos, self.y_Pos, 50, constants.DEACTIVATEDTOKEN, self.playingBoardCanv)
            self.y_Pos = self.y_Pos + 110

        #Settings for the items within the right Frame/the drawn playingboard
        self.playingBoardCanv.config(bg=constants.BGCOLOR, bd=0,  highlightthickness=0)
        self.playingBoardCanv.grid(row=1, column=0, sticky=SW, pady=(105,0))

        #----MAINLOOP
        self.window.mainloop()

    def startGame(self):

        def createPlayers(mode): #Adds the necessary Player/Computer Objects depending on the chosen mode
            if mode == 0:
                self.game.playerList.append(Player())
                self.game.playerList.append(Player())
            elif mode == 1:
                self.game.playerList.append(Player())
                self.game.playerList.append(Computer()) 


        self.btnFrame.destroy() #Removes the buttons on the left when the "Start Game" button has been pressed

        #Changes the styling of the circles in the playingboard once the game has been started (they don't look deactivated now)
        for row in range(len(self.board.fieldArr)) : 
            for col in range(len(self.board.fieldArr[row])) : 
                self.playingBoardCanv.itemconfig(self.circleArr[row][col], fill=constants.ACTIVATEDTOKEN) #Change Method for Canvas objects
        self.playingBoardCanv.grid(pady=0)
        
        self.x_Pos = 80
        for col in range(self.board.column):
            self.arrowArr[col].grid(row=0, column=0, padx=self.x_Pos, pady=0, sticky=SW)
            self.x_Pos += 125


        #---Decide Mode
        mode = int(self.modeDiv.get())
        createPlayers(mode)
        #---Decide first player
        self.game.turnOf = int(self.turnDiv.get())

        #---- Player Message
        #Color for the playermessage on the left hand side
        if self.game.turnOf == 1:
            playerColor = constants.BLUESELECTCOLOR
        elif self.game.turnOf == 2:
            playerColor = constants.ORANGESELECTCOLOR

        #First styling/drawing of the player message + changing the text depending on whose turn it is
        if type(self.game.playerList[self.game.turnOf-1]) == Computer:
            self.playerBox.config(text='Bitte warten...', bg=playerColor, fg=constants.FONTCOLOR, font=constants.LABELFONT, width=25, height=3)
            self.playerBox.grid(row=2, column=0, pady=(120,271))
            self.placeToken(0) #0 ist a temp number
        elif type(self.game.playerList[self.game.turnOf-1]) == Player:
            self.playerBox.config(text='Spieler ' + str(self.game.turnOf) + ',\n wähle eine Spalte aus!', bg=playerColor, fg=constants.FONTCOLOR, font=constants.LABELFONT, width=25, height=3)
            self.playerBox.grid(row=2, column=0, pady=(120,271))


    def placeToken(self, inputCol):       
        #Decide input for KI
        if type(self.game.playerList[self.game.turnOf-1]) == Computer: #If it's the Computers turn
            inputCol, score = self.game.playerList[self.game.turnOf-1].minimax(self.board, self.game.difficulty, -math.inf, math.inf, True) #the 2 return values of the minimax function get saved in the correct variables

        #Actual placement of the token:
        if self.board.checkFullCol(inputCol) == False:            #Input needs to be in a column with free space -> Full == False/No
            self.game.playerList[self.game.turnOf-1].placeToken(self.board, inputCol)   #Player/Computer places the token
            self.colorToken(inputCol)                                                   #Update the colors of the tokens on the board
            self.game.checkWin(self.board, self.game.turnOf)                            #Check if the new token resulted in a winner
            self.game.checkDraw(self.board)                                             #If no winner, check for a draw

            #IF GAMEEND / gamestatus != 0
            if self.game.gameStatus == 1 or self.game.gameStatus == 2:                #Winner || Draw - Jump out of the function which has been in a loop
                self.gameEnd()
            elif self.game.gameStatus == 0:                                           #Continue Game by only changing the player
                self.game.changeTurn()

                #---- Player Message - Styling
                if self.game.turnOf == 1:
                    playerColor = constants.BLUESELECTCOLOR
                elif self.game.turnOf == 2:
                    playerColor = constants.ORANGESELECTCOLOR

                #Change the styling of the already drawn box on the left hand side during the game
                if type(self.game.playerList[self.game.turnOf-1]) == Computer:
                    self.playerBox.config(text='Bitte warten...', bg=playerColor, fg=constants.FONTCOLOR, font=constants.LABELFONT)
                elif type(self.game.playerList[self.game.turnOf-1]) == Player:
                    self.playerBox.config(text='Spieler ' + str(self.game.turnOf) + ',\n wähle eine Spalte aus!', bg=playerColor, fg=constants.FONTCOLOR, font=constants.LABELFONT)

                #CPU CHOOSES MOVE
                if type(self.game.playerList[self.game.turnOf-1]) == Computer:
                    #for i in range(len(self.arrowArr)):
                    #    self.arrowArr[i].config(state="Disabled")
                    self.placeToken(0) #0 is a temp number for the CPU, gets overwritten by decideKIToken()


    def colorToken(self, inputCol): #colors the tokens in the color of the player who placed a token there
        for row in range(self.board.row):
            if self.board.fieldArr[row][inputCol] == 1:
                self.playingBoardCanv.itemconfig(self.circleArr[row][inputCol], fill=constants.BLUESELECTCOLOR)
            elif self.board.fieldArr[row][inputCol] == 2:
                self.playingBoardCanv.itemconfig(self.circleArr[row][inputCol], fill=constants.ORANGESELECTCOLOR)

    def drawWinToken(self):
        for i in range(4):
            #Uses the positions of the winningPos Array
            row = self.board.winningPos[i][0]
            col = self.board.winningPos[i][1]
            self.playingBoardCanv.itemconfig(self.circleArr[row][col], outline='White', width=4) #Adds an outline to the winnertokens

    def gameEnd(self):
        for col in range(self.board.column):
            self.arrowArr[col].destroy()        #Destroy the buttons so that the user can't click them anymore
        
        if self.game.gameStatus == 1:
            self.drawWinToken()

            #Change the message in the box on the left
            self.playerBox.config(text="Spieler " + str(self.game.turnOf) + "\n hat das Spiel gewonnen!")
            self.playingBoardCanv.grid(row=1, column=0, sticky=SW, pady=(105,0))
        elif self.game.gameStatus == 2:
            self.playerBox.config(text="Unentschieden!", bg=constants.FONTCOLOR, fg=constants.BGCOLOR, font=constants.LABELFONT)
            self.playingBoardCanv.grid(row=1, column=0, sticky=SW, pady=(105,0))

    def startPlaceTokenThread(self, column):
        #thread which allows the changing of the message on the left while the AI decides its move 
        placeToken = threading.Thread(target = lambda: self.placeToken(column))
        placeToken.start()


if __name__ == "__main__":
    gui = myGUI()