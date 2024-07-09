import gymnasium as gym
from stable_baselines3 import A2C, PPO
import os
import time

models_dir = f"CartPole/models/PPO-{int(time.time())}"
logdir = f"CartPole/logs-{int(time.time())}"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)

env = gym.make("CartPole-v1")
env.reset()

model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=logdir)
# model_path = f"{models_dir}/90000.zip"
# model = PPO.load(model_path, env=env)

TIMESTEPS = 10000
for i in range(1, 10):
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO")
    model.save(f"{models_dir}/{TIMESTEPS*i}")

env.close()
