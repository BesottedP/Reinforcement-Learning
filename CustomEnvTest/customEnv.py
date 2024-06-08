import gymnasium as gym
import numpy as np
from gymnasium import spaces
import random as rand

def gen_random():
    random_num = rand.randint(1, 13)
    if(random_num > 10):
        random_num = 10
    return random_num

def calculate_score(hand):
    hand_score = 0
    for card in hand:
        card_num = str(card)
        if card_num == "J" or card_num == "Q" or card_num == "K":
            hand_score += 10
        elif str(card) == "A":
            if hand_score > 10:
                hand_score += 1
            else:
                hand_score += 11
        else:
            hand_score += int(card)
    return hand_score

class CustomEnv(gym.Env):
    """Custom Environment that follows gym interface."""

    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self):
        super().__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(2)
        # Example for using image as input (channel-first; channel-last also works):
        self.observation_space = spaces.MultiDiscrete([32, 32])
    def step(self, action):
        self.terminated = False
        self.reward = 0

        if(action == 0):
            self.terminated = True
            if(self.score > self.opp_score):
                self.reward = 100
            elif(self.score > self.opp_score or self.score > 21):
                self.reward = -100
            else:
                self.reward = 0
        elif(action == 1):
            self.score += gen_random()
            if(self.score > 21):
                self.reward = -100
                self.terminated = True



        observation = [self.score, self.opp_score]
        observation = np.array(observation)

        return observation, self.reward, self.terminated, False, {}

    def reset(self, seed=None, options=None):
        self.score = gen_random() + gen_random()
        self.opp_score = gen_random() + gen_random()
        observation = [self.score, self.opp_score]
        observation = np.array(observation)

        return observation, {}

    def render(self):
        ...

    def close(self):
        ...