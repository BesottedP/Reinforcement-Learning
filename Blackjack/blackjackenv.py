import gymnasium as gym
import numpy as np
from gymnasium import spaces
import random


class BlackJackEnv(gym.Env):
    """Custom Environment that follows gym interface."""

    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self):
        super().__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.MultiDiscrete([2, 2, 5])
        # Example for using image as input (channel-first; channel-last also works):
        self.observation_space = spaces.MultiDiscrete([23, 12, 100001])

    def deal_cards(self):
        self.cards = ['2', '3', '4', '5', '6', '7', '8', '9' , '10', 'J', 'Q', 'K', 'A']
        self.deck = self.cards * 16
        random.shuffle(self.deck)

        self.dealer_cards = []
        self.dealer_shown_cards = []
        self.player_cards = []

        #Dealing out initial cards
        self.player_cards.append(self.deck.pop())
        self.dealer_cards.append(self.deck.pop())
        self.dealer_shown_cards.append(self.dealer_cards[0])
        self.player_cards.append(self.deck.pop())
        self.dealer_cards.append(self.deck.pop())

        self.player_score = calculate_score(self.player_cards)
        self.dealer_score = calculate_score(self.dealer_cards)

        #print(f"Your hand: {self.player_cards}, total score: {self.player_score}")
        #print(f"Dealers card: {self.dealer_shown_cards[0]}")
    
    def play_move(self, action):
        if action[0] == 0:
                self.player_cards.append(self.deck.pop())
                self.player_score = calculate_score(self.player_cards)
                #print(f"You drew a {self.player_cards[len(self.player_cards) - 1]}, your total score is: {self.player_score}")
                
                if(self.player_score > 21):
                    #print("You Bust")
                    self.money -= self.wager
                    #print(f"You lost ${self.wager}, you currently have ${self.money}")
                    self.in_progress = False
        else:
            #print(f"dealers other card is: {self.dealer_cards[1]}, dealer's total score is: {self.dealer_score}")
            while self.in_progress == True:
                if(self.dealer_score < 17 or self.dealer_score < self.player_score):
                    self.dealer_cards.append(self.deck.pop())
                    self.dealer_score = calculate_score(self.dealer_cards)
                    #print(f"Dealer drew a {self.dealer_cards[len(self.dealer_cards) - 1]}, their total score is: {self.dealer_score}")
                    if(self.dealer_score > 21):
                        #print("The dealer bust, you win!")
                        self.in_progress = False
                        self.money += (self.wager * 1.5)
                        #print(f"You won ${(self.wager * 1.5)}, you currently have ${self.money}")
                elif(self.dealer_score > self.player_score):
                    #print("The dealer scored higher")
                    self.in_progress = False
                    self.money -= self.wager
                    #print(f"You lost ${self.wager}, you currently have ${self.money}")
                elif(self.dealer_score == self.player_score):
                    #print("You tied")
                    #print(f"you currently have ${self.money}")
                    self.in_progress = False

    def step(self, action):
        self.reward = 0
        self.terminated = False

        if(self.in_progress == True):
            self.play_move(action)
        else:
            if(action[1] == 0):
                self.terminated = True
                self.reward = self.money
                #print(f"cashing out with ${self.money}")
            elif(self.money == 0):
                self.terminated = True
                self.reward = self.money
                #print("You are out of money")
            else:
                match action[2]:
                    case 0:
                        self.wager = 10000
                    case 1:
                        self.wager = 5000
                    case 2:
                        self.wager = 2500
                    case 3:
                        self.wager = 1000
                    case 4:
                        self.wager = 500
                if(self.wager > self.money):
                    self.wager = self.money
                self.deal_cards()
                if(self.player_score == 21):
                    #print("You win by blackjack!")
                    self.money += (self.wager * 1.5)
                    #print(f"You won ${(self.wager * 1.5)}, you currently have ${self.money}")
                    self.in_progress = False
                self.in_progress = True

        if(self.in_progress):
            observation = [calculate_score(self.player_cards), calculate_score(self.dealer_shown_cards), self.money]
        else:
            observation = [0, 0, self.money]

        observation = np.array(observation)

        #return observation
        return observation, self.reward, self.terminated, False, {}

    def reset(self, seed=None, options=None):
        self.in_progress = False
        self.money = 10_000

        observation = [0, 0, self.money]
        observation = np.array(observation)

        return observation, {}

    def render(self):
        ...

    def close(self):
        ...

def calculate_score(hand):
    hand_score = 0
    for card in hand:
        card_num = str(card)
        if card_num == "J" or card_num == "Q" or card_num == "K":
            hand_score += 10
        elif str(card) == "A":
            if hand_score > 10:
                hand_score += 1
            else:
                hand_score += 11
        else:
            hand_score += int(card)
    return hand_score

#Message for push