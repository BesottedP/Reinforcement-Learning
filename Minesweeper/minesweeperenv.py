import gymnasium as gym
import numpy as np
from gymnasium import spaces
from gymnasium.envs.registration import register
import random as rand
import pygame 
import time
import math

#Testing: 5x5, 3
#Very easy: 7x7, 5
#Easy: 9x9, 10
#Intermediate: 16x16, 40
#Hard: 22x22, 100

GAME_SIZE = 9
NUM_MINES = 10

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
        self.observation_space = spaces.Box(low=-1, high=8, shape=(GAME_SIZE, GAME_SIZE), dtype=np.int8)

        self.size = GAME_SIZE  # The size of the square grid
        self.window_size = 800  # The size of the PyGame window

        # assert render_mode is None or render_mode in self.metadata["render_modes"]
        # self.render_mode = render_mode
        self.render_mode = None

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
        for row in range(GAME_SIZE):
            for col in range(GAME_SIZE):
                # Skip cells that contain a mine
                if board[row][col] == -1:
                    continue
                num_adj_mines = 0
                # Iterate over all neighbors in the 3x3 area around the current cell
                for adj_row in range(max(0, row - 1), min(GAME_SIZE, row + 2)):
                    for adj_col in range(max(0, col - 1), min(GAME_SIZE, col + 2)):
                        if (adj_row == row and adj_col == col):
                            continue  # Skip the current cell itself
                        if board[adj_row][adj_col] == -1:
                            num_adj_mines += 1

                # Set the number of adjacent mines for this cell
                board[row][col] = num_adj_mines

    def reveal_empty_tiles(self, row, col):
        if(self.player_board[row][col] == -1):
            self.player_board[row][col] = self.master_board[row][col]
            self.num_tiles_left -= 1
            if(self.player_board[row][col] == 0):
                for adj_row in range(-1,2):
                        for adj_col in range(-1,2):
                            check_row = row + adj_row
                            check_col = col + adj_col
                            if((check_col == GAME_SIZE or check_row == GAME_SIZE)
                                or (check_col == -1 or check_row == -1)):
                                    continue
                            self.reveal_empty_tiles(check_row, check_col)
    
    def made_a_guess(self, row, col):
        for adj_row in range(-1, 2):
            for adj_col in range(-1, 2):
                check_row = row + adj_row
                check_col = col + adj_col
                if((check_col >= GAME_SIZE or check_row >= GAME_SIZE) or (check_col <= -1 or check_row <= -1)):
                    continue
                if(self.player_board[check_row, check_col] != -1):
                    return False
        return True

    def spreadCalc(self, player_board, row, col):
        award = 0
        for adj_row in range(-3, 4):
            for adj_col in range(-3, 4):
                # Calculate the absolute position of the cell to check
                check_row = row + adj_row
                check_col = col + adj_col

                # Skip out-of-bounds cells or the center cell itself
                if check_row < 0 or check_row >= GAME_SIZE or check_col < 0 or check_col >= GAME_SIZE or (adj_row == 0 and adj_col == 0):
                    continue

                # Skip cells that do not meet the condition
                if player_board[check_row][check_col] == -1:
                    continue

                # Use absolute values for distance calculation
                distance = max(abs(adj_row), abs(adj_col))

                # Award points based on the distance
                if distance == 1:
                    award += 0.5
                elif distance == 2:
                    award += 0.2
                elif distance == 3:
                    award += 0.1
        return award


    def make_move(self, master_board, player_board, row, col):
        if self.first_move:
            # Initialize the game on the first move
            master_board[row, col] = -2
            self.place_mines(master_board, row, col)
            self.set_num_mines(master_board)
            self.reveal_empty_tiles(row, col)
            player_board[row, col] = master_board[row, col]
            self.first_move = False
            
            # Check if the game is won immediately after first move
            if self.num_tiles_left == 0:
                return 20, True

            if self.render_mode == "human":
                self.render()
            return 0, False
        
        # Check if the move is invalid
        if player_board[row][col] != -1:
            self.num_invalids += 1
            if self.num_invalids >= 6:
                if self.render_mode == "human":
                    print("Too many invalid moves! Game over...")
                    self.render()
                return -10, True
            if self.render_mode == "human":
                print("Invalid move! Try again.")
                self.render()
            return -3, False
        
        # Check if the move hits a mine
        if master_board[row][col] == -1:
            player_board[row][col] = -1
            if self.render_mode == "human":
                print("You hit a mine! Game over...")
                self.render()
            return -20, True
        
        # Process a guess
        if self.made_a_guess(row, col):
            self.reveal_empty_tiles(row, col)
            reward = -1.5
            if self.render_mode == "human":
                print("Made a guess")
                self.render()
            return reward, False

        # Calculate spread award and update board
        spread_award = self.spreadCalc(player_board, row, col)
        self.reveal_empty_tiles(row, col)

        # Check for win condition
        if self.num_tiles_left == 0:
            if self.render_mode == "human":
                print("You win!")
                self.render()
            return 20, True
        
        # Return current reward
        reward = spread_award
        if self.render_mode == "human":
            self.render()
        return reward, False
            

    def step(self, action):

        row = action[0]
        col = action[1]
        self.reward, self.terminated = self.make_move(self.master_board, self.player_board, row, col)

        board = np.array(self.player_board, dtype=np.int8)
        observation = board
        observation = np.array(observation)

        if(self.render_mode == "human"):
            self.render()

        #return observation
        return observation, self.reward, self.terminated, False, {}

    def reset(self, seed=None, options=None):
        self.first_move = True
        self.num_invalids = 0;
        self.num_tiles_left = (GAME_SIZE*GAME_SIZE) - NUM_MINES
        self.master_board = np.zeros((GAME_SIZE, GAME_SIZE))
        self.player_board = np.full((GAME_SIZE, GAME_SIZE), -1)

        board = np.array(self.player_board, dtype=np.int8)
        observation = board

        if(self.render_mode == "human"):
            self.render()

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
                if(self.player_board[x][y] != -1):
                    match self.player_board[x][y]:
                        case 0: color = (128, 128, 128)
                        case 1: color = (0, 0, 255)
                        case 2: color = (0, 255, 0)
                        case 3: color = (255, 0, 0)
                        case 4: color = (93, 63, 211)
                        case 5: color = (255, 165, 0)
                        case 6: color = (0, 255, 255)
                        case 7: color = (0, 0, 0)
                        case 8: color = (169, 169, 169)

                    if(self.master_board[x][y] == -1):
                        color = (0, 0, 0)

                    self.draw_text(str(self.player_board[x][y]), self.text_font, color, (x*pix_square_size)+(pix_square_size/2), (y*pix_square_size)+(pix_square_size/2))

        pygame.event.pump()
        pygame.display.update()

        self.clock.tick(self.metadata["render_fps"])
        time.sleep(0.75)

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()