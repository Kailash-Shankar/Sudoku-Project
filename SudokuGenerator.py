import math, random



class SudokuGenerator:
    # initializing the variables and assigning them
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.board = [[0 for i in range(row_length)] for j in range(row_length)]
        self.removed_cells = removed_cells
        self.box_length = int(math.sqrt(row_length))



    # returing the board as a list
    def get_board(self):
        return self.board



    # print the board to console
    def print_board(self):
        for row in self.board:
            print(" ".join(str(cell) for cell in row))


    # make sure numb is valid and not aready in the row/boolean return
    def valid_in_row(self, row, num):
        return num not in self.board[row]


    # same as above but column edition
    def valid_in_col(self, col, num):
        for row in range(self.row_length):
            if self.board[row][col] == num:
                return False
        return True


    # check if num can be placed in subgrid of board w no repeat/iterate through to crosscheck
    def valid_in_box(self, row_start, col_start, num):
        for i in range(3):
            for j in range(3):
                if self.board[row_start + i][col_start + j] == num:
                    return False
        return True


    #Returns if it is valid to enter num at (row, col) in the board.
    def is_valid(self,row, col, num):
        #row
        for i in range(self.row_length):
            if self.board[row][i] == num:
                return False

        #column
        for i in range(self.row_length):
            if self.board[i][col] == num:
                return False

        #3x3
        row_start = row - row % 3
        col_start = col - col % 3

        for i in range(3):
            for j in range(3):
                if self.board[row_start + i][col_start + j] == num:
                    return False

        return True

    #Randomly fills in values in the 3x3 box
    def fill_box(self, row_start, col_start):
        unused_in_box = list(range(1,10))

        for i in range(3):
            for j in range(3):
                num = random.choice(unused_in_box)
                self.board[row_start + i][col_start + j] = num
                unused_in_box.remove(num)

    #Fills the three boxes along the main diagonal of the board
    def fill_diagonal(self):
        for i in range(0, self.row_length, 3):
            self.fill_box(i, i)

    #Given
    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    #Given
    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    #Removes the appropriate number of cells from the board
    def remove_cells(self):
        removed = 0
        while removed < self.removed_cells:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                removed += 1

    #Given
    def generate_sudoku(size, removed):
        sudoku = SudokuGenerator(size, removed)
        sudoku.fill_values()
        board = sudoku.get_board()
        sudoku.remove_cells()
        board = sudoku.get_board()
        return board

