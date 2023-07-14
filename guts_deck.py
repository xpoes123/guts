import random
from constants import *

class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for value in RANKS:
            for suit in SUITS:
                self.cards.append((value, suit))
  
    def shuffle(self):
        self.build()
        random.shuffle(self.cards)
        
    def deal(self):
        if len(self.cards) > 1:
            return self.cards.pop()
            
class Hand(Deck):
    def __init__(self):
        self.cards = []
        self.card_img = []

    def add_card(self, card):
        self.cards.append(card)

    def display_cards(self):
        for card in self.cards:
            cards = "".join((card[0], card[1]))
            if cards not in self.card_img:
                self.card_img.append(cards)

    # compares two hands between self and hand2
    # Returns 1 if self wins and -1 if opponent wins and 0 if it is a tie
    def comp_hand(self, hand2):
        print(self.cards[0], self.cards[1])
        print(hand2.cards[0], hand2.cards[1])

        # Checks if the hands are paired or not
        selfPair = False
        if self.cards[0][0] == self.cards[1][0]:
            selfPair = True
        opPair = False
        if hand2.cards[0][0] == hand2.cards[1][0]:
            opPair = True
        if opPair and not selfPair:
            return -1
        elif selfPair and not opPair:
            return 1
        elif opPair and selfPair:
            if RANKS.index(self.cards[0][0]) > RANKS.index(hand2.cards[0][0]):
                return 1
            elif RANKS.index(self.cards[0][0]) == RANKS.index(hand2.cards[0][0]):
                return 0
            return -1
        
        else:
            # Calculates the rankings of each individual card
            selfMax = max(RANKS.index(self.cards[0][0]), RANKS.index(self.cards[1][0]))
            selfMin = min(RANKS.index(self.cards[0][0]), RANKS.index(self.cards[1][0]))
            opMax =  max(RANKS.index(hand2.cards[0][0]), RANKS.index(hand2.cards[1][0]))
            opMin =  min(RANKS.index(hand2.cards[0][0]), RANKS.index(hand2.cards[1][0]))
            if(selfMax > opMax):
                return 1
            elif(selfMax < opMax):
                return -1
            elif(selfMin > opMin):
                return 1
            elif(selfMin < opMin):
                return -1
            return 0
            