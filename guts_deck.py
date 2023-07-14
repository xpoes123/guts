# This program deals primarily with the deck itself and computing which hand is better

import random
from constants import *

class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    # Generates the deck that we are working with
    def build(self):
        for value in RANKS:
            for suit in SUITS:
                self.cards.append((value, suit))
  
    #Shuffles the deck lol
    def shuffle(self):
        random.shuffle(self.cards)
        
    # Deals out a singular card
    def deal(self):
        if len(self.cards) > 1:
            return self.cards.pop()
            
class Hand(Deck):
    def __init__(self):
        self.cards = []
        self.card_img = []

    # Adds a card to our cards array so our hand is defined
    def add_card(self, card):
        self.cards.append(card)

    # Returns the names of the card so it can be used to display in pygame
    def display_cards(self):
        for card in self.cards:
            cards = "".join((card[0], card[1]))
            if cards not in self.card_img:
                self.card_img.append(cards)

    # compares two hands between self and hand2
    # Returns 1 if self wins and -1 if opponent wins and 0 if it is a tie
    def comp_hand(self, hand2):
        # Checks if the hands are paired or not
        selfPair = False
        if self.cards[0][0] == self.cards[1][0]:
            selfPair = True

        opPair = False
        if hand2.cards[0][0] == hand2.cards[1][0]:
            opPair = True
        
        # Checks if one hand is better based on if a hand is paired or not
        if opPair and not selfPair:
            return -1
        elif selfPair and not opPair:
            return 1
        elif opPair and selfPair:
            # Checks the hierchy of cards given that they are paired
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
            
