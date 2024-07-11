import gymnasium as gym
from stable_baselines3 import A2C, PPO
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines3.common.utils import set_random_seed
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.env_util import make_vec_env
import os
import time

env_id = "CartPole-v1"
num_cpu = 8

models_dir = f"CartPole/models/{num_cpu}"
logdir = f"CartPole/logs/{num_cpu}"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)

vec_env = make_vec_env(env_id, n_envs=num_cpu)
vec_env.reset()

model = PPO("MlpPolicy", vec_env, verbose=1, tensorboard_log=logdir)
# model_path = f"{models_dir}/90000.zip"
# model = PPO.load(model_path, env=env)

TIMESTEPS = 100000
for i in range(1, 10):
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO")
    model.save(f"{models_dir}/{TIMESTEPS*i}")

vec_env.close()
