import gym
from stable_baselines3 import A2C, PPO
import os
import time

model_type = "PPO"

models_dir = f"models/{model_type}-{int(time.time())}"
logdir = f"logs/{model_type}-{int(time.time())}"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)

env = gym.make("MountainCar-v0", render_mode = "human")
env.reset()

# model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=logdir)
models_dir = "Mountain/models/PPO-1717903579"
model_path = f"{models_dir}/5070000"
model = PPO.load(model_path, env=env)

TIMESTEPS = 10000
for i in range(1, 10000):
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=model_type)
    model.save(f"{models_dir}/{TIMESTEPS*i}")

env.close()