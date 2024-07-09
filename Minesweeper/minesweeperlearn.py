import gymnasium as gym
from stable_baselines3 import A2C, PPO
from minesweeperenv import MinesweeperEnv
import os
import time

model_type = "PPO"

env = MinesweeperEnv(render_mode=None)
env.reset()

learning_rates = [0.00003, 0.00006, 0.0003, 0.0006, 0.003, 0.006, 0.03, 0.06, 0.3, 0.6]
for rate in learning_rates:
    models_dir = f"Minesweeper/models/{rate}"
    logdir = f"Minesweeper/logs/{rate}"

    if not os.path.exists(models_dir):
        os.makedirs(models_dir)

    if not os.path.exists(logdir):
        os.makedirs(logdir)

    model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=logdir, device="cuda", learning_rate=rate)

    model.learn(total_timesteps=1000000, reset_num_timesteps=False, tb_log_name=model_type)
    model.save(f"{models_dir}/{rate}")

env.close()