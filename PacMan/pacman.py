import gymnasium as gym
from stable_baselines3 import PPO
import os
import time

model_type = "PPO"

models_dir = f"PacMan/models/{model_type}-CNN_GPU"
logdir = f"PacMan/logs/{model_type}-CNN_GPU"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)

env = gym.make("ALE/Breakout-v5")
env.reset()

# model = PPO("CnnPolicy", env, verbose=1, tensorboard_log=logdir, device="cuda")
model_path = f"{models_dir}/810000.zip"
model = PPO.load(model_path, env=env, device ="cuda")

TIMESTEPS = 10000
for i in range(1, 10000):
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=model_type)
    model.save(f"{models_dir}/{TIMESTEPS*i}")

env.close()