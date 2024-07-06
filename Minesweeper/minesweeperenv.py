import gymnasium as gym
import numpy as np
from gymnasium import spaces
import random as rand
import pygame 
import time

GAME_SIZE = 7
NUM_MINES = 5

class MinesweeperEnv(gym.Env):
    """Custom Environment that follows gym interface."""

    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self, render_mode):
        super().__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.MultiDiscrete([GAME_SIZE, GAME_SIZE])
        # Example for using image as input (channel-first; channel-last also works):
        self.observation_space = spaces.Box(low=-500, high=500, shape=((GAME_SIZE*GAME_SIZE),), dtype=np.float64)

        self.size = GAME_SIZE  # The size of the square grid
        self.window_size = 800  # The size of the PyGame window

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        pygame.font.init()
        self.text_font = pygame.font.SysFont(None, 30)
        self.window = None
        self.clock = None

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
        if self.render_mode == "human":
            self.render()
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
            # print("You win!")
            # print(self.player_board)
            return 1000, True
        reward = (((GAME_SIZE*GAME_SIZE)-NUM_MINES)-self.num_tiles_left) - self.prev_reward
        return reward, False
        

    def step(self, action):

        row = action[0]
        col = action[1]
        self.reward, self.terminated = self.make_move(self.master_board, self.player_board, row, col)
        self.prev_reward = self.reward

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

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.window.blit(img, (x, y))
        
    def render(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode(
                (self.window_size, self.window_size)
            )
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface((self.window_size, self.window_size))
        canvas.fill((255, 255, 255))
        pix_square_size = (
            self.window_size / self.size
        )  # The size of a single grid square in pixels

        for x in range(self.size + 1):
            pygame.draw.line(
                canvas,
                0,
                (0, pix_square_size * x),
                (self.window_size, pix_square_size * x),
                width=3,
            )
            pygame.draw.line(
                canvas,
                0,
                (pix_square_size * x, 0),
                (pix_square_size * x, self.window_size),
                width=3,
            )

        self.window.blit(canvas, canvas.get_rect())
        
        for x in range(GAME_SIZE):
            for y in range(GAME_SIZE):
                color = (0, 0, 0)
                if(self.player_board[x][y] != -5):
                    match self.player_board[x][y]:
                        case 0: color = (255, 255, 255)
                        case 1: color = (0, 0, 255)
                        case 2: color = (0, 255, 0)
                        case 3: color = (255, 0, 0)
                        case 4: color = (93, 63, 211)
                        case 5: color = (255, 165, 0)
                        case 6: color = (0, 255, 255)
                        case 7: color = (0, 0, 0)
                        case 8: color = (169, 169, 169)

                    self.draw_text(str(self.player_board[x][y]), self.text_font, color, (x*80)+30, (y*80)+30)

        pygame.event.pump()
        pygame.display.update()

        self.clock.tick(self.metadata["render_fps"])
        time.sleep(1)

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()

