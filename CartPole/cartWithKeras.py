import gym
import random
import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers.legacy import Adam

from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

env = gym.make('CartPole-v1', render_mode = 'human')

states = env.observation_space.shape[0]
actions = env.action_space.n

# episodes = 10
# for episode in range(1, episodes+1):
#     state = env.reset()
#     done = False
#     score = 0

#     while not done:
#         env.render()
#         action = random.choice([0,1])
#         n_state, reward, done, info = env.step(action)
#         score+=reward
#     print('Episode:{} Score:{}'.format(episode,score))

model = Sequential()
model.add(Flatten(input_shape=(1,states)))
model.add(Dense(24, activation='relu'))
model.add(Dense(24, activation='relu'))
model.add(Dense(actions, activation='linear'))

agent = DQNAgent(
    model = model,
    memory = SequentialMemory(limit=5000, window_length=1),
    policy = BoltzmannQPolicy(),
    nb_actions = actions,
    nb_steps_warmup=10,
    target_model_update=0.01
)

agent.compile(Adam(learning_rate=0.001), metrics=["mae"])
agent.fit(env, nb_steps=1000, visualize=False, verbose=1)

results = agent.test(env, nb_episodes=10, visualize=True)
print(np.mean(results.history["episode reward"]))

agent.save_weights("agent_weights.h5f", overwrite=True)

env.close()
