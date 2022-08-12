from tkinter import *
import tkinter.font as font
import math
import Client

WINDOW = None
CLIENT = None
GAME_WINDOW = None
END_WINDOW = None

current_x, current_y = 0,0
currentBox = (-1, -1) # col, row
lockedBoxes = [[0 for x in range(8)] for y in range(8)]
boxAreas = [[0 for x in range(8)] for y in range(8)]

class MainView(Frame):
    def __init__(self, *args, **kwargs):
        container = Frame()
        container.grid(row=0, column=0, sticky='nsew')
        self.listing = {}
        for p in (HomePage, GamePage, EndPage):
            page_name = p.__name__
            frame = p(parent=container, controller=self)
            frame.grid(row=0, column=0, sticky='nsew')
            self.listing[page_name] = frame

        self.up_frame('HomePage')

    def up_frame(self, page_name):
        page = self.listing[page_name]
        page.event_generate("<<ShowFrame>>")
        page.tkraise()

    def get_frame(self, page_name):
        page = self.listing[page_name]
        return page

class HomePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Deny and Conquer", font=("Helvetica", 50))
        label.pack()
        buttonFont = font.Font(family='Helvetica', size=16, weight='bold')
        btn = Button(self, text="Start", font=buttonFont, height=5,
                     width=15, command=lambda: controller.up_frame('GamePage'))
        def connectToServer(event=None):
            CLIENT.connect()
        btn.bind('<Button-1>', connectToServer)
        btn.pack()

class EndPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Game Over", font=("Helvetica", 50))
        label.pack()
        buttonFont = font.Font(family='Helvetica', size=16, weight='bold')
        btn = Button(self, text = "Disconnect", font=buttonFont, height=5, width=15, command=lambda: end())
        btn.pack()

        def end():
            CLIENT.sendMessage("END")
            WINDOW.destroy()

    def winUpdate(self, arg):
        label2txt = "Player won: " + arg
        label2 = Label(self, text=label2txt, font=("Helvetica", 40), fg=str(arg).lower())
        label2.pack()



class GamePage(Frame):

    def __init__(self, parent, controller):
        global WINDOW
        global CONTROL2
        CONTROL2 = controller

        Frame.__init__(self, parent)

        canvas = Canvas(self, background='yellow', width=1200, height=900)
        canvas.grid(row=0, column=0)
        WINDOW.update()
        # boxAreas = [[0 for x in range(8)] for y in range(8)]
        col_width = canvas.winfo_width()/8
        row_height = canvas.winfo_height()/8
        self.mycanvas = canvas
        self.myColWidth = col_width
        self.myRowHeight = row_height

        def getBox(event):
            col_width = self.mycanvas.winfo_width()/8
            row_height = self.mycanvas.winfo_height()/8
            # Calculate column and row number
            col = int(event.x//col_width)
            row = int(event.y//row_height)
            return (col, row)

        def locate_xy(event):
            global current_x, current_y
            global currentBox
            current_x, current_y = event.x, event.y
            currentBox = getBox(event)
            if boxAreas[currentBox[1]][currentBox[0]] >= 0 and lockedBoxes[currentBox[1]][currentBox[0]] == 0:
                lockBox(currentBox[0], currentBox[1])

        def addLine(event):
            global current_x, current_y
            box = getBox(event)
            if box == currentBox and boxAreas[box[1]][box[0]] >= 0 and lockedBoxes[currentBox[1]][currentBox[0]] == 0:
                c = CLIENT.getColor()
                self.mycanvas.create_line(
                    (current_x, current_y, event.x, event.y), fill=c, width=5)
                fillArea(lineLength(current_x, current_y,
                         event.x, event.y) * 5, box[0], box[1])
                current_x, current_y = event.x, event.y

        def lineLength(x0, y0, x1, y1):
            xdiff = (x1 - x0)**2
            ydiff = (y1 - y0)**2
            return math.sqrt(xdiff+ydiff)

        def fillArea(linelen, col, row):
            boxAreas[row][col] += linelen
            if boxAreas[row][col]/(col_width*row_height) >= 0.5:
                boxAreas[row][col] = -1
                claimBox(col, row)

        def clearBox(event):
            if boxAreas[currentBox[1]][currentBox[0]] >= 0 and lockedBoxes[currentBox[1]][currentBox[0]] == 0:
                boxAreas[currentBox[1]][currentBox[0]] = 0
                unlockBox(currentBox[0], currentBox[1])
                self.mycanvas.create_rectangle(currentBox[0]*col_width, currentBox[1]*row_height, (
                    currentBox[0]+1)*col_width, (currentBox[1]+1)*row_height, fill='white')

        def lockBox(col, row):
            # box = getBox(event)
            # Send packet to temporarily lock ownership of this box to player
            msg = f'LOCK {col} {row} {CLIENT.getColor()}'
            CLIENT.sendMessage(msg)

        def unlockBox(col, row):
            # box = getBox(event)
            #locked_boxAreas[box[0]][box[1]] = 0
            # Tell other players that this box is unlocked
            msg = f'UNLOCK {col} {row} {CLIENT.getColor()}'
            CLIENT.sendMessage(msg)

        def claimBox(col, row):
            # box = getBox(event)
            msg = f'CLAIM {col} {row} {CLIENT.getColor()}'
            CLIENT.sendMessage(msg)
            checkEndgame()

        def checkEndgame():
            gameEnd = True
            for i in range(8):
                for j in range(8):
                    if boxAreas[i][j] >= 0:
                        gameEnd = False
            # Send end state to Server
            if gameEnd:
                CLIENT.sendMessage("ENDPAGE")
                controller.up_frame('EndPage')

        def makeBoxes(event):
            for i in range(8):
                for j in range(8):
                    boxAreas[i][j] = 0
                    self.mycanvas.create_rectangle(
                        j*col_width, i*row_height, (j+1)*col_width, (i+1)*row_height, outline="black", fill="white")

        self.mycanvas.bind('<Button-1>', locate_xy)
        self.mycanvas.bind('<B1-Motion>', addLine)
        self.mycanvas.bind('<ButtonRelease-1>', clearBox)
        self.bind("<<ShowFrame>>", makeBoxes)

    def fillBox(self, col, row, color):
        col = int(col)
        row = int(row)
        boxAreas[row][col] = -1
        self.mycanvas.create_rectangle(col*self.myColWidth, row*self.myRowHeight,
                                       (col+1)*self.myColWidth, (row+1)*self.myRowHeight, fill=str(color).lower())

    def lockPlayersBox(self, col, row, opponent_color):
        col = int(col)
        row = int(row)
        lockedBoxes[row][col] = 1
        self.mycanvas.create_text(col*self.myColWidth + 75, row*self.myRowHeight +
                                  56, text="DRAWING...", fill=opponent_color, font=('Helvetica 15 bold'))
        # print(lockedBoxes[row][col] == 1)

    def unlockPlayersBox(self, col, row):
        col = int(col)
        row = int(row)
        lockedBoxes[row][col] = 0
        self.mycanvas.create_rectangle(col*self.myColWidth, row*self.myRowHeight,
                                       (col+1)*self.myColWidth, (row+1)*self.myRowHeight, fill='white')
        print("unlocking Boxes: ", col, row, lockedBoxes[row][col] == 0)

    def bringUpEnd(self):
        CONTROL2.up_frame('EndPage')

def startGUI():
    global WINDOW
    global CLIENT
    global GAME_WINDOW
    global END_WINDOW

    WINDOW = Tk()
    WINDOW.geometry("1200x900")
    WINDOW.rowconfigure(0, weight=1)
    WINDOW.columnconfigure(0, weight=1)
    WINDOW.resizable(False,False)

    main = MainView(WINDOW)
    GAME_WINDOW = main.get_frame("GamePage")
    END_WINDOW = main.get_frame("EndPage")

    CLIENT = Client.Client()
    CLIENT.setGameWindow(GAME_WINDOW)
    CLIENT.setEndWindow(END_WINDOW)
    # main.pack(side="top", fill="both", expand=True)

    WINDOW.mainloop()

startGUI()