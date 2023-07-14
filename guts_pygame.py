import pygame
from constants import *
from guts_deck import *
import sys
import time
import math

# Pygame boilerplate
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Guts')
screen.fill(background_color)
pygame.draw.rect(screen, grey, pygame.Rect(0, 0, 250, 700))

# Functions required for printing text
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def game_texts(text, x, y):
    TextSurf, TextRect = text_objects(text, textfont)
    TextRect.center = (x, y)
    screen.blit(TextSurf, TextRect)
    pygame.display.update()

def chip_texts(text, x, y, amt):
    text = text + " " +  str(math.floor(amt))
    TextSurf, TextRect = text_objects(text, textfont)
    TextRect.center = (x, y)
    screen.blit(TextSurf, TextRect)
    pygame.display.update()

# Responsible for managing button presses and drawing the buttons
def button(msg, x, y, w, h, ic, ac, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # Checks if the mouse is currently where the button is at
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        # Draws the box for the button
        pygame.draw.rect(screen, ac, (x, y, w, h))
        # Checks if the button was clicked when mouse is hovering over button
        if click[0] == 1 != None:
            action()
            # Attempt to try and prevent the button from multi clicking. 
            # Ideally I want to find a better solution because it causes the game to refresh in a weird way.
            time.sleep(0.1)
    else:
        # Draws the box for the button
        pygame.draw.rect(screen, ic, (x, y, w, h))

    # Prints the text for the buttons
    TextSurf, TextRect = text_objects(msg, font)
    TextRect.center = ((x + (w/2)), (y + (h/2)))
    screen.blit(TextSurf, TextRect)

# Class for the main logic of the game
class Play:
    def __init__(self):
        self.deck = Deck()

        self.dealer = Hand()
        self.player = Hand()

        self.playerChips = STARTSTACK
        self.playerBet = ANTE
        self.opChips = STARTSTACK
        self.opBet = ANTE
        self.pot = 0

        self.dealAction = False
        self.action = True

        self.opHold = False

        self.deck.shuffle()

    # Deals cards for the game and keeps track of betting logistics amongst other logistical stuff
    def deal(self):
        # Resetting previous rounds things
        self.dealAction = True
        # Ensures that deal can't be pressed before an action was given
        if not self.action:
            return
        self.action = False
        # Since we keep using blit, we need to redraw the canvas. This is causing issues but oh well
        # Could potentially be fixed if we drew everything at the same time, but not sure how much that will help
        screen.fill(background_color)
        pygame.draw.rect(screen, grey, pygame.Rect(0, 0, 250, 700))

        # Checks if the game should be over by condition of someone being bankrupt
        if self.opChips <= self.opBet:
            game_texts("!!!YOU WIN!!!", 500, 500)
            time.sleep(5)
            sys.exit()
        elif self.playerChips <= self.playerBet:
            game_texts("!!!YOU LOSE!!!", 500, 500)
            time.sleep(5)
            sys.exit()

        # Resets the important data that we need for this hand
        self.dealer = Hand()
        self.player = Hand()
        self.deck = Deck()
        self.deck.shuffle()

        # Deals with the logistics of betting in this round
        self.pot = 0
        self.playerChips -= self.playerBet
        self.opChips -= self.opBet
        self.pot += self.playerBet + self.opBet

        # Deals the hole cards for both players
        for i in range(2):
            self.dealer.add_card(self.deck.deal())
            self.player.add_card(self.deck.deal())

        # Displays all the cards and text that we currently need
        self.dealer.display_cards()
        self.player.display_cards()
        self.player_card = 1

        dealer_card = pygame.image.load(path + 'img/back.png').convert()
        dealer_card_2 = pygame.image.load(path + 'img/back.png').convert()
            
        player_card = pygame.image.load(path + 'img/' + self.player.card_img[0] + '.png').convert()
        player_card_2 = pygame.image.load(path + 'img/' + self.player.card_img[1] + '.png').convert()

        game_texts("Op's hand is:", 500, 150)
        chip_texts("Op chip count is:", 500, 75, self.opChips)
        chip_texts("Op bet this round:", 1000, 75, self.opBet)

        screen.blit(dealer_card, (400, 200))
        screen.blit(dealer_card_2, (550, 200))

        game_texts("Your hand is:", 500, 400)
        chip_texts("Your chip count is:", 500, 650, self.playerChips)
        chip_texts("Your bet this round:", 1000, 650, self.playerBet)

        chip_texts("Pot Size:", 800, 505, self.pot)
        
        screen.blit(player_card, (300, 450))
        screen.blit(player_card_2, (410, 450))

    # Action for the button if player decides to hold
    def hold(self):
        self.action = True
        # Checks to see if dealer button was pressed first
        if not self.dealAction:
            return
        self.dealAction = False

        # Randomly generates if the computer will hold.
        # This can be made to a better method but I'm not implementing that tonight
        self.opHold = bool(random.choice([True, False]))

        # If the computer holds
        if(self.opHold):
            # Displays the cards for the computer since they held
            op_card = pygame.image.load(path + 'img/' + self.dealer.card_img[0] + '.png').convert()
            op_card_2 = pygame.image.load(path + 'img/' + self.dealer.card_img[1] + '.png').convert()
            screen.blit(op_card, (400, 200))
            screen.blit(op_card_2, (550, 200))

            # Checks to see who the winner is. If player wins then it is 1, if computer wins then -1, tie is 0.
            val = self.player.comp_hand(self.dealer)
            if val == 1:
                game_texts("You win! " + str(self.pot), 775, 250)
                # Deals with the logistics of winning/losing the pot
                self.playerChips += self.pot
                self.opBet = self.pot
                self.playerBet = ANTE
                self.pot = 0
            elif val == -1:
                game_texts("You lose", 775, 250)
                # Deals with the logistics of winning/losing the pot
                self.opChips += self.pot
                self.playerBet = self.pot
                self.opBet = ANTE
                self.pot = 0
            else:
                game_texts("You tie! " + str(math.floor(self.pot/2)), 775, 250)
                # Deals with the logistics of tying the pot
                self.opChips += self.pot/2
                self.playerChips += self.pot/2
                self.pot = 0
        else:
            game_texts("You win! " + str(self.pot), 775, 250)
            # Deals with the logistics of winning/losing the pot
            self.playerChips += self.pot
            self.playerBet = ANTE
            self.opBet = ANTE
            self.pot = 0

    # Action for the button if player decides to fold
    def fold(self):
        self.action = True
        # Checks to see if dealer button was pressed first
        if not self.dealAction:
            return
        self.dealAction = False

        # Randomly generates if the computer will hold.
        # This can be made to a better method but I'm not implementing that tonight
        self.opHold = bool(random.choice([True, False]))

        # If the computer holds
        if(self.opHold):
            game_texts("You tie! " + str(math.floor(self.pot/2)), 775, 250)
            # Deals with the logistics of tying the pot
            self.opChips += self.pot/2
            self.playerChips += self.pot/2
            self.pot = 0
        else:
            game_texts("You lose", 775, 250)
            # Deals with the logistics of winning/losing the pot
            self.opChips += self.pot
            self.playerBet = ANTE
            self.opBet = ANTE
            self.pot = 0

    # Action for the exit button
    def exit(self):
        sys.exit()
        
    # Legacy code, might add some funcationality later
    def play_or_exit(self):
        game_texts("Play again press Deal!", 200, 80)
        time.sleep(3)
        self.player.value = 0
        self.op.value = 0
        self.deck = Deck()
        self.op = Hand()
        self.player = Hand()
        self.deck.shuffle()
        screen.fill(background_color)
        pygame.draw.rect(screen, grey, pygame.Rect(0, 0, 250, 700))
        pygame.display.update()
        
play_guts = Play()
running = True

# Action for pygame to continously display
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    button("Deal", 30, 100, 150, 50, light_slat, dark_slat, play_guts.deal)
    button("Hold", 30, 200, 150, 50, light_slat, dark_slat, play_guts.hold)
    button("Fold", 30, 300, 150, 50, light_slat, dark_slat, play_guts.fold)
    button("EXIT", 30, 500, 150, 50, light_slat, dark_red, play_guts.exit)
    pygame.display.flip()
