from minesweeperenv import MinesweeperEnv
env = MinesweeperEnv(render_mode="human")
episodes = 1000

for episode in range(episodes):
	done = False
	obs = env.reset()
	while done == False:
		random_action = env.action_space.sample()
		print("action",random_action)
		obs, reward, done, trunc, info = env.step(random_action)
		print('reward',reward)