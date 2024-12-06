from tabnanny import check

import pygame
import sys, time
from Sudoku_Cell_and_Board import *
from SudokuGenerator import *
import copy, random


def main():
    #Title Screen
    pygame.init()
    screen = pygame.display.set_mode((901, 1000))
    screen.fill("ivory")

    def show():
        pygame.display.update()

    def display_text(fontsize, textstr, location_tuple, color="black", BG_color = None):
        NewFont = pygame.font.Font(None, fontsize)
        NewText = NewFont.render(textstr, 0, color, BG_color)
        TextRect = NewText.get_rect(center=location_tuple)
        screen.blit(NewText, TextRect)
        show()
        return location_tuple[0], location_tuple[1]

    def create_rect(xlen, ylen, x, y, color):
        NewRect = pygame.Rect(x-50, y-50, xlen, ylen)
        pygame.draw.rect(screen, color, NewRect)
        show()


    #Set up title text
    display_text(100, "Welcome to Sudoku", (450, 300), "black")
    display_text(50, "Select Game Mode:", (450, 600), "navy")


    #Button Boxes
    Easy_x, Easy_y = display_text(60, "          ", (250, 700), "white", "green")
    Med_x, Med_y = display_text(80, "          ", (450, 700), "white", "yellow")
    Hard_x, Hard_y = display_text(60, "          ", (650, 700), "white", "red")

    #displaying text boxes


    display_text(50, "MEDIUM", (Med_x, Med_y), "white", "gold")
    display_text(50, "HARD", (Hard_x, Hard_y), "white", "darkred")
    display_text(50, "EASY", (Easy_x, Easy_y), "white", "seagreen")



    Title = True
    while Title:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = event.pos
                #CHeck "Easy" button press
                if Easy_x-50<x<Easy_x+50 and Easy_y-30<y<Easy_y+30:
                    display_text(60, "          ", (Easy_x, Easy_y), "white", "silver")
                    display_text(50, "EASY", (Easy_x, Easy_y), "white", "black")
                    Mode = "Easy"
                    Title = False

                elif Med_x-75<x<Med_x+75 and Med_y-30<y<Med_y+30:
                    display_text(80, "          ", (Med_x, Med_y), "white", "silver")
                    display_text(50, "MEDIUM", (Med_x, Med_y), "white", "black")
                    Mode = "Medium"
                    Title = False

                elif Hard_x-50<x<Hard_x+50 and Hard_y-30<y<Hard_y+30:
                    display_text(60, "          ", (Hard_x, Hard_y), "white", "silver")
                    display_text(50, "HARD", (Hard_x, Hard_y), "white", "black")
                    Mode = "Hard"
                    Title = False



    time.sleep(0.15)

    #Game Screen Functions and Data Values
    BG_dict = {"Easy": "aquamarine", "Medium": "khaki", "Hard": "pink"}
    Cell_dict = {"Easy": 30, "Medium": 40, "Hard": 50}
    x_center, y_center = -1, -2
    old_num = ""
    old_big_num = ""

    def draw_lines():
        #Draw Thin Lines
        for i in range(0,901, 100):
            pygame.draw.line(screen, "black", (i, 0), (i, 900), 2)
            pygame.draw.line(screen, "black", (0, i), (900, i), 2)

        #Draw Thick Lines
        for i in range(300, 900, 300):
            pygame.draw.line(screen, "black", (i, 0), (i, 900), 6)
            pygame.draw.line(screen, "black", (0, i), (900, i), 6)

        show()


    def draw_highlight_box(x, y, color="red", thickness = 6):
        pygame.draw.line(screen, color, (x-50, y-50), (x+50, y-50), thickness)
        pygame.draw.line(screen, color, (x - 50, y - 50), (x-50, y + 50), thickness)
        pygame.draw.line(screen, color, (x - 50, y + 50), (x + 50, y + 50), thickness)
        pygame.draw.line(screen, color, (x + 50, y - 50), (x + 50, y + 50), thickness)
        show()
        return x, y

    def draw_commands():
        #Boxes:
        A, B = display_text(80, "        ", (300, 950), "Black", "chocolate")
        C, D = display_text(80, "          ", (450, 950), "Black", "chocolate")
        E, F = display_text(80, "       ", (600, 950), "Black", "chocolate")

        display_text(60, "Reset", (300, 950), "Black", "orange")
        display_text(60, "Restart", (450, 950), "Black", "orange")
        display_text(60, "Quit", (600, 950), "Black", "orange")

        return A, B, C, D, E, F

    def draw_grey_nums(num, x, y):
        display_text(60, f"{old_num}", (x - 25, y - 25), BG_Color)
        display_text(60, f"{num}", (x-25, y-25), "purple")
        return num, True

    def draw_input_nums(num, x, y):
        display_text(100, " ", (x, y), BG_Color, BG_Color)
        display_text(100, f"{num}", (x, y), "blue")
        return num, True

    def draw_board_nums(num, x, y):
        display_text(100, " ", (x, y), BG_Color, BG_Color)
        display_text(100, f"{num}", (x, y), "black")
        return num, True

    def clear_square(x, y):
        create_rect(100, 100, x, y, BG_Color)
        draw_highlight_box(x, y)

    def fill_board(board):
        for i in range(9):
            for j in range(9):
                if board[i][j] != 0:
                    draw_board_nums(board[i][j], 50 + 100 * j, 50 + 100 * i)


    def check_endgame(board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return False
        return True

    def check_result(board, answer):
        for i in range(9):
            for j in range(9):
                if board[i][j] != answer[i][j]:
                    return False
        return True




    #Game Screen Action Commands
    BG_Color = BG_dict[Mode]
    Remov_num = Cell_dict[Mode]
    screen.fill(BG_Color)
    draw_lines()
    reset_x, reset_y, restart_x, restart_y, quit_x, quit_y = draw_commands()

    show()

    #Board Generation
    def Generate_Board():
        global SG, New_board, Greyed_board, Answer_key
        SG = SudokuGenerator(9, Remov_num)
        SG.fill_values()
        SG.print_board()
        New_board = SG.get_board()

        Answer_key = copy.deepcopy(New_board)
        SG.remove_cells()
        Greyed_board = copy.deepcopy(SG.get_board())
        fill_board(SG.get_board())

    Generate_Board()



    #Events Loop
    Game_Running = True
    Won = False

    while Game_Running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y<900:
                    if x_center >= 0 and y_center >= 0:
                        old_x, old_y = x_center, y_center
                        flag = False
                        draw_highlight_box(old_x, old_y, BG_Color, 6) #Erases lines around previous box
                    x_center = x//100 * 100 + 50
                    y_center = y//100 * 100 + 50
                    draw_lines() #redraws black lines
                    draw_highlight_box(x_center, y_center) #draws red highlight lines
                elif reset_x - 63 < x < reset_x + 63 and reset_y - 30 < y < reset_y + 30:
                    screen.fill(BG_Color)
                    draw_lines()
                    reset_x, reset_y, restart_x, restart_y, quit_x, quit_y = draw_commands()
                    Generate_Board()

                elif restart_x - 75 < x < restart_x + 75 and restart_y - 30 < y < restart_y + 30:
                    main()

                elif quit_x-55<x<quit_x+55 and quit_y-30<y<quit_y+30:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if 50 <= x_center < 850 and 50 <= y_center <= 850:
                        old_x, old_y = x_center, y_center
                        draw_highlight_box(old_x, old_y, BG_Color, 6) #Erases lines around previous box
                    x_center = (old_x+100)//100 * 100 + 50
                    y_center = old_y//100 * 100 + 50
                    draw_lines() #redraws black lines
                    draw_highlight_box(x_center, y_center) #draws red highlight lines
                if event.key == pygame.K_LEFT:
                    if 50 < x_center <= 850 and 50 <= y_center <= 850:
                        old_x, old_y = x_center, y_center
                        draw_highlight_box(old_x, old_y, BG_Color, 6) #Erases lines around previous box
                    x_center = (old_x-100)//100 * 100 + 50
                    y_center = old_y//100 * 100 + 50
                    draw_lines() #redraws black lines
                    draw_highlight_box(x_center, y_center) #draws red highlight lines
                if event.key == pygame.K_UP:
                    if 50 <= x_center <= 850 and 50 < y_center <= 850:
                        old_x, old_y = x_center, y_center
                        draw_highlight_box(old_x, old_y, BG_Color, 6) #Erases lines around previous box
                    x_center = old_x//100 * 100 + 50
                    y_center = (old_y-100)//100 * 100 + 50
                    draw_lines() #redraws black lines
                    draw_highlight_box(x_center, y_center) #draws red highlight lines
                if event.key == pygame.K_DOWN:
                    if 50 <= x_center <= 850 and 50 <= y_center < 850:
                        old_x, old_y = x_center, y_center
                        draw_highlight_box(old_x, old_y, BG_Color, 6) #Erases lines around previous box
                    x_center = old_x//100 * 100 + 50
                    y_center = (old_y+100)//100 * 100 + 50
                    draw_lines() #redraws black lines
                    draw_highlight_box(x_center, y_center) #draws red highlight lines
                if x_center >= 0 and y_center >= 0:
                    if 1<=event.key-48<=9:
                        x_num = int((x_center - 50) / 100)
                        y_num = int((y_center - 50) / 100)
                        if New_board[y_num][x_num] == 0:
                            clear_square(x_center, y_center)
                            draw_grey_nums(event.key-48, x_center, y_center)
                            Greyed_board[y_num][x_num] = event.key-48

                    if event.key == pygame.K_RETURN:
                        x_num = int((x_center - 50) / 100)
                        y_num = int((y_center - 50) / 100)
                        if Greyed_board[y_num][x_num] != 0:

                            clear_square(x_center, y_center)
                            draw_input_nums(Greyed_board[y_num][x_num], x_center, y_center)
                            New_board[y_num][x_num] = Greyed_board[y_num][x_num]

                            if check_endgame(New_board):
                                if check_result(New_board, Answer_key):
                                    Won = True
                                Game_Running = False






                    if event.key == pygame.K_DELETE:
                        x_num = int((x_center - 50) / 100)
                        y_num = int((y_center - 50) / 100)
                        if Greyed_board[y_num][x_num] != 0 and New_board[y_num][x_num] == 0:
                            clear_square(x_center, y_center)

    time.sleep(0.2)

    # Game Over Screen
    GameOver = True
    if Won:
        screen.fill("greenyellow")
        display_text(150, "You Win!!!", (450, 300), "chocolate")
        display_text(100, "             ", (450, 700), "black", "black")
        display_text(80, "Quit", (450, 700), "white")
        for i in range(5):
            randX = random.randrange(100, 800)
            randY = random.randrange(100, 900)
            display_text(200*(i+1), ":)", (randX, randY), "gold")
            time.sleep(0.3)
            display_text(200*(i+1), ":)", (randX, randY), "white")
            time.sleep(0.1)
            display_text(200*(i+1), ":)", (randX, randY), "black")
            time.sleep(0.1)
            display_text(200*(i+1), ":)", (randX, randY), "yellowgreen")
            display_text(150, "You Win!!!", (450, 300), "chocolate")
            display_text(100, "             ", (450, 700), "black", "black")
            display_text(80, "Quit", (450, 700), "white")
            time.sleep(0.3)
    else:
        screen.fill("slateblue")
        display_text(150, "You Lose...", (450, 300), "pink")
        display_text(100, "             ", (450, 700), "black", "black")
        display_text(80, "Restart", (450, 700), "white")


        for i in range(5):
            randX = random.randrange(100, 800)
            randY = random.randrange(100, 900)
            display_text(200*(i+1), ":(", (randX, randY), "plum")
            time.sleep(0.3)
            display_text(200*(i+1), ":(", (randX, randY), "white")
            time.sleep(0.1)
            display_text(200*(i+1), ":(", (randX, randY), "black")
            time.sleep(0.1)
            display_text(200*(i+1), ":(", (randX, randY), "darkslateblue")
            display_text(150, "You Lose...", (450, 300), "pink")
            display_text(100, "             ", (450, 700), "black", "black")
            display_text(80, "Restart", (450, 700), "white")
            time.sleep(0.3)
    show()

    while GameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if 320 < x < 580 and 660 < y < 740:
                    if Won:
                        pygame.quit()
                        sys.exit()
                    else:
                        main()


if __name__ == "__main__":
    main()
