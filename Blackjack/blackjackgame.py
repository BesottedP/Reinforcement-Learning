import random

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

#Setting up the game
cards = ['2', '3', '4', '5', '6', '7', '8', '9' , '10', 'J', 'Q', 'K', 'A']
cards_num = ['2', '3', '4', '5', '6', '7', '8', '9', '10']
deck = cards * 16
random.shuffle(deck)

dealer_cards = []
player_cards = []

dealer_shows = '-1'

#Dealing out initial cards
player_cards.append(deck.pop())
dealer_cards.append(deck.pop())
dealer_shows = dealer_cards[0]
player_cards.append(deck.pop())
dealer_cards.append(deck.pop())

player_score = calculate_score(player_cards)
dealer_score = calculate_score(dealer_cards)

print(f"Your hand: {player_cards}, total score: {player_score}")
print(f"Dealers card: {dealer_shows}")

if(player_score == 21):
    print("You win by blackjack!")
    exit()

while True:
    decision = input("Hit or Stay? [H/S]\n")
    if decision != 'H' and decision != 'S':
        continue
    if decision == 'H':
        player_cards.append(deck.pop())
        player_score = calculate_score(player_cards)
        print(f"You drew a {player_cards[len(player_cards) - 1]}, your total score is: {player_score}")
        
        if(player_score > 21):
            print("You Lost")
            exit()
        if(player_score == 21):
            print("player wins!")
            exit()
    else:
        print(f"dealers other card is: {dealer_cards[1]}, dealer's total score is: {dealer_score}")
        while True:
            if(dealer_score > player_score):
                print("You Lost")
                exit()
            if(dealer_score < 17):
                dealer_cards.append(deck.pop())
                dealer_score = calculate_score(dealer_cards)
                print(f"Dealer drew a {dealer_cards[len(dealer_cards) - 1]}, their total score is: {dealer_score}")
                if(dealer_score > 21):
                    print('You win!')
                    exit()
            elif(dealer_score == player_score):
                print("You tied!")
                exit()
            else:
                print("You win!")
                exit()
        
        

