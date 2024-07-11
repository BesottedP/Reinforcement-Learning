import gymnasium as gym
from stable_baselines3 import A2C, PPO
from minesweeperenv import MinesweeperEnv
import os
import time

model_type = "PPO"

env = MinesweeperEnv(render_mode="human")
env.reset()

models_dir = f"Minesweeper/models/att2"
logdir = f"Minesweeper/logs/att2"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)

#model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=logdir, device="cuda", n_steps=8192, batch_size=256)
model_path = f"{models_dir}/20350000.zip"
model = PPO.load(model_path, env=env, device ="cuda")

TIMESTEPS = 10000
for i in range(1, 10000):
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=model_type)
    model.save(f"{models_dir}/{TIMESTEPS*i}")

env.close()