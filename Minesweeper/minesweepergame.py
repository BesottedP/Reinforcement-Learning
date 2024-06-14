import random as rand
import numpy as np

NUM_MINES = 50

def place_mines(board, start_row, start_col):
    num_bombs = 0
    while num_bombs != NUM_MINES:
        rand_row = rand.randint(0,9)
        rand_col = rand.randint(0,9)
        if(rand_row >= start_row -1 and rand_row <= start_row + 1 and
           rand_col >= start_col -1 and rand_col <= start_col + 1):
            continue
        if(board[rand_row][rand_col] != -1):
            board[rand_row][rand_col] = -1
            num_bombs += 1

def set_num_mines(board):
    for row in range(0, 10):
        for col in range(0, 10):
            num_adj_mines = 0
            for adj_row in range(-1,2):
                for adj_col in range(-1,2):
                    check_col = col + adj_col
                    check_row = row + adj_row
                    if((check_col == -1 or check_row == -1)
                       or (check_col == 10 or check_row == 10)
                        or (adj_col == 0 and adj_row == 0)):
                        continue
                    elif(board[check_row][check_col] == -1):
                        num_adj_mines += 1
            if(board[row][col] != -1):
                board[row][col] = num_adj_mines

def reveal_empty_tiles(master_board, player_board, row, col):
    global num_tiles_left
    for adj_row in range(-1,2):
            for adj_col in range(-1,2):
                check_row = row + adj_row
                check_col = col + adj_col
                if((check_col == 0 or check_row == 0)
                       or (check_col == 11 or check_row == 11)):
                        continue
                if(player_board[check_row-1][check_col-1] == '*' and (master_board[check_row-1][check_col-1] != -1)):
                    player_board[check_row-1][check_col-1] = master_board[check_row-1][check_col-1]
                    num_tiles_left -= 1
                    if(player_board[check_row-1][check_col-1] == '0'):
                        reveal_empty_tiles(master_board, player_board, check_row, check_col)

def make_move(master_board, player_board, row, col):
    if(master_board[row][col] == -1):
        player_board[row][col] = master_board[row][col]
        print("You hit a mine! Game over...")
        print(player_board)
        quit()
    reveal_empty_tiles(master_board, player_board, row+1, col+1)
    print(player_board)
    if(num_tiles_left == 0):
        print("You win!")
        print(player_board)
        quit()

num_tiles_left = 100 - NUM_MINES
master_board = np.zeros((10, 10))
player_board = np.full((10, 10), "*")
start_row, start_column = map(int, input("Enter a row and column to start ").split())
master_board[start_row-1 , start_column-1] = -2
place_mines(master_board, start_row-1, start_column-1)
set_num_mines(master_board)
print(master_board)
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
reveal_empty_tiles(master_board, player_board, start_row, start_column)
player_board[start_row-1, start_column-1] = master_board[start_row-1 , start_column-1]
print(player_board)
while (True):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    while True:
        print(num_tiles_left)
        row, column = map(int, input("Enter a row and column ").split())
        if(player_board[row-1][column-1] == '*'):
            break
    make_move(master_board, player_board, row-1, column-1)


#TODO array number one should shows all the information on the board, and is created after the player makes the first move
#In each tile it should show the number of bombs touching
