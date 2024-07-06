import gymnasium as gym
from stable_baselines3 import A2C, PPO
from minesweeperenv import MinesweeperEnv
import os
import time

model_type = "PPO"

models_dir = f"Minesweeper/models/{model_type}-{int(time.time())}"
logdir = f"Minesweeper/logs/{model_type}-{int(time.time())}"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)

env = MinesweeperEnv(render_mode=None)
env.reset()

model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=logdir)
# models_dir = "Minesweeper/models/PPO-1718429027"
# logdir = "Minesweeper/logs/PPO-1718429027"
# model_path = f"{models_dir}/680000.zip"
# model = PPO.load(model_path, env=env)

TIMESTEPS = 10000
for i in range(1, 100000):
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=model_type)
    model.save(f"{models_dir}/{TIMESTEPS*i}")

env.close()