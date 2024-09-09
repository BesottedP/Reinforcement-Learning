from blackjackenv import BlackJackEnv


env = BlackJackEnv()
episodes = 1000

for episode in range(episodes):
	done = False
	obs = env.reset()
	while done == False:
		random_action = env.action_space.sample()
		print("action",random_action)
		obs, reward, done, trunc, info = env.step(random_action)
		print('reward',reward)