import gymnasium as gym
import numpy as np
from gymnasium import spaces
import random as rand

GAME_SIZE = 24
NUM_MINES = 100

class MinesweeperEnv(gym.Env):
    """Custom Environment that follows gym interface."""

    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self):
        super().__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.MultiDiscrete([GAME_SIZE, GAME_SIZE])
        # Example for using image as input (channel-first; channel-last also works):
        self.observation_space = spaces.Box(low=-500, high=500, shape=((GAME_SIZE*GAME_SIZE),), dtype=np.float64)

    def place_mines(self, board, start_row, start_col):
        num_bombs = 0
        while num_bombs != NUM_MINES:
            rand_row = rand.randint(0,GAME_SIZE-1)
            rand_col = rand.randint(0,GAME_SIZE-1)
            if(rand_row >= start_row -1 and rand_row <= start_row + 1 and
            rand_col >= start_col -1 and rand_col <= start_col + 1):
                continue
            if(board[rand_row][rand_col] != -1):
                board[rand_row][rand_col] = -1
                num_bombs += 1

    def set_num_mines(self, board):
        for row in range(0, GAME_SIZE):
            for col in range(0, GAME_SIZE):
                num_adj_mines = 0
                for adj_row in range(-1,2):
                    for adj_col in range(-1,2):
                        check_col = col + adj_col
                        check_row = row + adj_row
                        if((check_col == -1 or check_row == -1)
                        or (check_col == GAME_SIZE or check_row == GAME_SIZE)
                            or (adj_col == 0 and adj_row == 0)):
                            continue
                        elif(board[check_row][check_col] == -1):
                            num_adj_mines += 1
                if(board[row][col] != -1):
                    board[row][col] = num_adj_mines

    def reveal_empty_tiles(self, master_board, player_board, row, col):
        self.num_tiles_left
        for adj_row in range(-1,2):
                for adj_col in range(-1,2):
                    check_row = row + adj_row
                    check_col = col + adj_col
                    if((check_col == GAME_SIZE or check_row == GAME_SIZE)
                        or (check_col == -1 or check_row == -1)):
                            continue
                    if(self.player_board[check_row][check_col] == -5 and (self.master_board[check_row][check_col] != -1)):
                        self.player_board[check_row][check_col] = self.master_board[check_row][check_col]
                        self.num_tiles_left -= 1
                        if(self.player_board[check_row][check_col] == 0):
                            self.reveal_empty_tiles(self.master_board, self.player_board, check_row, check_col)

    def make_move(self, master_board, player_board, row, col):
        if(self.first_move == True):
            master_board[row, col] = -2
            self.place_mines(master_board, row, col)
            self.set_num_mines(master_board)
            self.reveal_empty_tiles(master_board, player_board, row, col)
            player_board[row, col] = master_board[row , col]
            self.first_move = False
            return 0, False
        if(self.player_board[row][col] != -5):
            return -1, True
        if(self.master_board[row][col] == -1):
            self.player_board[row][col] = self.master_board[row][col]
            # print("You hit a mine! Game over...")
            # print(self.player_board)
            return -50, True
        self.reveal_empty_tiles(self.master_board, self.player_board, row, col)
        if(self.num_tiles_left == 0):
            print("You win!")
            print(self.player_board)
            return 1000, True
        # print(self.player_board)
        return 476-self.num_tiles_left, False
        

    def step(self, action):

        row = action[0]
        col = action[1]
        self.reward, self.terminated = self.make_move(self.master_board, self.player_board, row, col)

        board = np.array(self.player_board)
        observation = board.flatten()
        observation = np.array(observation)

        #return observation
        return observation, self.reward, self.terminated, False, {}

    def reset(self, seed=None, options=None):
        self.first_move = True
        self.num_tiles_left = (GAME_SIZE*GAME_SIZE) - NUM_MINES
        self.master_board = np.zeros((GAME_SIZE, GAME_SIZE))
        self.player_board = np.full((GAME_SIZE, GAME_SIZE), -5)

        board = np.array(self.player_board)
        observation = board.flatten()

        return observation, {}

    def render(self):
        ...

    def close(self):
        ...

