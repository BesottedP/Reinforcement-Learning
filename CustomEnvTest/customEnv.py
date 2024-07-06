import gymnasium as gym
import numpy as np
from gymnasium import spaces
import random as rand

class CustomEnv(gym.Env):
    """Custom Environment that follows gym interface."""

    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self):
        super().__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(100)
        # Example for using image as input (channel-first; channel-last also works):
        self.observation_space = spaces.Discrete(200)
    def step(self, action):
        self.terminated = False

        if(action == self.number):
            self.reward = 100
            self.terminated = True
            observation = 0
        else:
            observation = (self.number - action)
            self.reward = -(abs(observation))
            observation = observation + 100

        observation = np.array(observation)

        return observation, self.reward, self.terminated, False, {}

    def reset(self, seed=None, options=None):
        self.number = rand.randint(0, 99)
        observation = 0
        observation = np.array(observation)

        return observation, {}

    def render(self):
        ...

    def close(self):
        ...