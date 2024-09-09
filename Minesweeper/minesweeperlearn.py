from gymnasium.envs.registration import register
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from minesweeperenv import MinesweeperEnv
import os

model_type = "PPO"

register(id='Minesweeper-v0', entry_point='minesweeperenv:MinesweeperEnv')
env = make_vec_env("Minesweeper-v0", n_envs=16)

# env = MinesweeperEnv(render_mode="human")
env.reset()

models_dir = f"Minesweeper/models/Easy"
logdir = f"Minesweeper/logs/Easy"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)

model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=logdir, device="cuda")

# custom_objects = { 'learning_rate': 0.0004 }
model_path = f"{models_dir}/2900000.zip"
model = PPO.load(model_path, env=env, device ="cuda")

TIMESTEPS = 1000000
for i in range(1, 100000):
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=model_type)
    model.save(f"{models_dir}/{(TIMESTEPS*i)+2900000}")

env.close()