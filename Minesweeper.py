import random
from tkinter import *
import tkinter.messagebox

class MinesweeperCell(Button):
    '''represents a Minesweeper Cell'''

    def __init__(self,master,coord):
        '''creates a new blank MinesweeperCell with (row,column) coord'''
        Button.__init__(self,width=3,height=2,text='',font = ('Arial',24)) #sets up the cell
        self.coord = coord  # (row,column) coordinate tuple
        self.bomb = False #automatically not a bomb
        self.master = master #master
        self.colormap = ['brown','blue','darkgreen','VioletRed4','purple','maroon','cyan','black','dim gray']
        # set up listeners
        self.bind('<Button-1>',self.highlight)
        self.bind('<Button-2>',self.user_bomb)
        self.bind('<Button-3>',self.user_bomb)

    def get_coord(self):
        '''returns the (row,column) coordinate of the cell'''
        return self.coord

    def is_bomb(self):
        '''returns True if the cell is the bomb, False if not'''
        return self.bomb

    def get_text(self):
        '''returns the text in the cell'''
        return self['text']

    def find_surrounding_bombs(self,numBombs):
        '''numBobs is an int representing the number of surrounding bombs
        makes self.numBombs the number of surrounding bombs of the cell'''
        self.numBombs = numBombs

    def make_bomb(self):
        '''makes the cell a bomb'''
        self.bomb = True

    def highlight(self,event):
        '''handler function for mouse click
        if bomb, game is lost. If not, the text is self.numBombs'''    
        if self.bomb == True: #if the cell is a bomb
            tkinter.messagebox.showerror('Minesweeper','KABOOM! You lose.',parent=self) #show an error
            self.master.game_lost() #use game lost function in Mineweeper Cell
        else:
            if self['text'] == '*': #if the cell was marked as a bomb
                self.master.add_bomb() #add a bomb back to the number of bombs
            self['foreground'] = self.colormap[self.numBombs] #changes text color 
            self['text'] = self.numBombs #changes text to the number of surrounding bombs
            self.master.check_win() #checks for a winner
 
    def user_bomb(self,event):
        '''handler function for a right click
        makes a text change to signify the user thinks it is a bomb'''
        if self['text'] == "*": 
            pass
        elif self['text'] in ['0','1','2','3','4','5','6','7','8']:
            pass #does nothing if there is already text
        else:
            self['text'] = "*" #text changes
            self.master.subtract_bomb() #subtracts a bomb
            self.master.check_win() #checks if there is a winner

    def show_bomb(self):
        '''used if the game is lost
        changes the text if the cell was actually a bomb'''
        if self.bomb == True: #if the cell is a bomb
            self['foreground'] = 'red' #text color is red
            self['text'] = 'B' #text is B

class MinesweeperGrid(Frame):
    '''object for a Minesweeper grid'''

    def __init__(self,master,columns,rows,bombs):
        '''MinesweeperGrid(master)
        creates a new blank Minesweeper grid'''
        # initialize a new Frame
        self.bombs = bombs #number of bombs to choose
        Frame.__init__(self,bg='black') #makes a frame
        self.grid() #puts frame in grid
        self.columns = columns #number of columns
        self.rows = rows #number of rows
        # put in lines between the cells
        # (odd numbered rows and columns in the grid)
        # create the cells
        self.cells = {} # set up dictionary for cells
        self.cellsList = [] #list of cells
        for row in range(1,rows+1):
            for column in range(1,columns+1):
                coord = (row,column) 
                self.cells[coord] = MinesweeperCell(self,coord) #makes cells
                self.cellsList.append(coord) #puts cells in cellslist
                # cells go in even-numbered rows/columns of the grid
                self.cells[coord].grid(row=row,column=column) #puts cells on grid
        self.bombslabel = Label(self,bg='white',text=str(self.bombs)) #mkaes bombs label
        self.bombslabel.grid(row=20,column=1) #puts bombslabel on grid
        for allbombs in range(self.bombs): #for all bombs
            bomb = random.randint(0,len(self.cellsList)-1) 
            bombcoords = self.cellsList[bomb] 
            self.cells[bombcoords].make_bomb() #make a random cell a bomb
            self.cellsList.pop() #takes the bomb cell out of the regular cell list
        self.units = {}  # set up list for units
        for row in range(1,rows+1):
            for column in range(1,columns+1): #for every coord
                coord = (row,column)
                surroundingCells = []
                for validrows in range(row-1,row+2):
                    for validcolumns in range(column-1,column+2):
                        #the row and column of the surroundings has to be at most 1 apart from the cell
                        if validrows >= 1 and validrows <= rows:
                            if validcolumns >= 1 and validcolumns <= columns: #tests if the cell is valid
                                validcoord = (validrows,validcolumns) #makes a cord tuple
                                if validcoord != coord: #disclude the cell itself
                                    surroundingCells.append(validcoord) #append it to surrounding cell
                self.units[coord] = surroundingCells #adds it to the units
        for cells in self.units: #for all cells
            bomb = 0 #number of bombs is 0
            for surroundings in self.units[cells]: #for the surroundings
                if self.cells[surroundings].is_bomb() == True: #if the surrounding is a bomb
                    bomb += 1 #add the surrounding bombs counter by 1
            self.cells[cells].find_surrounding_bombs(bomb)
            #use the find_surrounding_bombs function to find each cells' surrounding bombs

    def game_lost(self):
        '''called when the game is lost
        shows if all cells are actually a bomb'''
        for allcells in self.cells: #for all cells
            self.cells[allcells].show_bomb() #calls the show_bomb function for each cell

    def add_bomb(self):
        '''adds 1 to the number of bombs'''
        self.bombs += 1 #adds 1 
        self.bombslabel['text'] = str(self.bombs) #updates the label 

    def subtract_bomb(self):
        '''subtracts 1 to the number of bombs'''
        self.bombs -= 1 #subtracts 1 
        self.bombslabel['text'] = str(self.bombs) #updates the label 

    def check_win(self):
        '''checks if a win is on the board'''
        if self.bombs == 0: #if self.bombs is 0
            numUnFilled = 0 #the number of unfilled cells
            for allcells in self.cells: #for all cells
                if self.cells[allcells].get_text() == '': #if a cell is empty
                    numUnFilled += 1 #the number of unfilled goes up
            if numUnFilled == 0: #if all the cells are filled
                tkinter.messagebox.showinfo('Minesweeper','Congratulations -- you won!',parent=self) #congradulations message

   

def minesweeper(rows, columns, bombs):
    '''minesweeper()
    plays minesweeper'''
    root = Tk()
    root.title('Mineweeper')
    mg = MinesweeperGrid(root, rows, columns, bombs)
    root.mainloop()

minesweeper(12,10,15)
