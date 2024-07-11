from minesweeperenv import MinesweeperEnv
env = MinesweeperEnv(render_mode="human")
episodes = 1000

for episode in range(episodes):
	done = False
	obs = env.reset()
	while done == False:
		# row, col = input("Enter a row and column: ").split()
		# random_action = [int(col), int(row)]
		random_action = env.action_space.sample()
		print("action",random_action)
		obs, reward, done, trunc, info = env.step(random_action)
		print('reward',reward)