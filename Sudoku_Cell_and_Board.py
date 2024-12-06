import pygame

class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.sketched = 0  #sketched value should be 0 in every cell and not shown in the beginning
        self.cell_size = 50 # cell is 50 units, whole screen/board is 450
        self.selected = False #Whether the cell is selected or not
    def set_cell_value(self, value):
        self.value = value
    def set_sketched_value(self, value):
        self.sketched = value
    def draw(self):
        x = self.row * self.cell_size    #sets up x and y coordinates for each cell
        y = self.col * self.cell_size
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, self.cell_size, self.cell_size))   #draws a white rectangle filled
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, self.cell_size, self.cell_size), 1)
        #^^^draws a black rectangle with a line thickness of 1 above the white rectangle^^^

        if self.value != 0:
            cell_font = pygame.font.Font(None, 20)  #sets up font to be 25 units, half of cell size
            cell_surf = cell_font.render(str(self.value), 0, (0, 0, 0))    #makes font color of value black
            self.screen.blit(cell_surf, (x + self.cell_size//2, y + self.cell_size // 2))     #prints/puts value text on top at the x or y value (hopefully a cell)

        if self.sketched != 0:
            cell_font = pygame.font.Font(None, 10) #sets up sketched value font to be smaller than value
            cell_surf = cell_font.render(str(self.sketched), 0, (158, 158, 158)) #font is grey
            self.screen.blit(cell_surf, (x + 5, y + 5)) #prints sketched value onto cell but it is slightly offset

        if self.selected:
            pygame.draw.rect(self.screen, (176, 50, 50), (x, y, self.cell_size, self.cell_size), 2)
            #if cell is in the selected state it makes a red rectangle on top of selected cell.


class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = 450
        self.height = 450
        self.screen = screen
        self.difficulty = difficulty
        self.board = [[Cell(0, i, j, screen) for j in range(9) for i in range(9)]]
        #makes a board through a list, all the items in the list are 0 and there are 81 zeros.
        self.cell_selected = None #variable for a specific selected cell
        self.board_data = [[0 for i in range(9)] for j in range(9)]
        #makes a board in the background that is all 0s at first

    def __str__(self):
        return str(self.board)

    def __repr__(self):
        return self.__str__()

    def draw(self):
        for row in self.board:
            for cell in row:
                cell.draw()
        pygame.draw.line(self.screen, (0, 0, 0), (150, 0), (150, 450), 3)
        pygame.draw.line(self.screen, (0, 0, 0), (300, 0), (300, 450), 3)
        pygame.draw.line(self.screen, (0, 0, 0), (0, 150), (450, 150), 3)
        pygame.draw.line(self.screen, (0, 0, 0), (0, 300), (450, 300), 3)
        #draws thicker lines every 3 cells

    def select(self, row, col):
        if self.cell_selected:
            self.cell_selected.selected = False
        self.cell_selected = self.board[row][col]
        self.cell_selected.selected = True
    def click(self, x, y):
        if 0 <= x <= 450 and 0 <= y <= 450:     #click has to be in the board (which is the whole screen)
            row = y // 50    #50 is the cell_size
            col = x // 50
            return row, col
        return None    #otherwise return none

    def clear(self):
        if self.cell_selected:  #if the cell is selected
            self.cell_selected.set_cell_value(0)   #calls function from Cell class
            self.cell_selected.set_sketched_value(0)  #to edit the cell value or the sketched value

    def sketch(self, value):
        if self.cell_selected:
            self.cell_selected.set_sketched_value(value)    #cell selected changes its value to sketched value

    def place_number(self, value):
        if self.cell_selected:
            self.cell_selected.set_cell_value(value)     #value of cell becomes number placed
            self.cell_selected.set_sketched_value(0)    #this becomes 0 so that it does not appear

    def reset_to_original(self):
        for row in range(9):
            for col in range(9):
                self.board[row][col].set_cell_value(0)
                self.board[row][col].set_sketched_value(0)

    def is_full(self):
        for row in self.board:
            for cell in row:
                if cell.value != 0:
                    return True
                else:
                    return False

    def update_board(self):
        for row in range(9):
            for col in range(9):
                self.board_data[row][col] = self.board[row][col].value

    def find_empty(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return row, col
        return None

    def check_board(self):
        pass
    #Im lost now
