from customEnv import CustomEnv


env = CustomEnv()
episodes = 50

for episode in range(episodes):
	done = False
	obs = env.reset()
	while done == False:
		random_action = env.action_space.sample()
		print("action",random_action)
		obs, reward, done, trunc, info = env.step(random_action)
		print('reward',reward)