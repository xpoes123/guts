# Also legacy code, can be used to figure out multi card or player logic

from guts_deck import *

deck = Deck()
deck.shuffle()

player = Hand()
dealer = Hand()

for i in range(2):
    player.add_card(deck.deal())
    dealer.add_card(deck.deal())

print(player.cards)
print(dealer.cards)

player.add_card(deck.deal())

print(player.cards)

player.calc_hand()
dealer.calc_hand()
