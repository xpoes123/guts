import pygame
from constants import *
from guts_deck import *
import sys
import time
import math

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption('Guts')
screen.fill(background_color)
pygame.draw.rect(screen, grey, pygame.Rect(0, 0, 250, 700))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def game_texts(text, x, y):
    TextSurf, TextRect = text_objects(text, textfont)
    TextRect.center = (x, y)
    screen.blit(TextSurf, TextRect)
    pygame.display.update()

def chip_texts(text, x, y, amt):
    text = text + " " +  str(amt)
    TextSurf, TextRect = text_objects(text, textfont)
    TextRect.center = (x, y)
    screen.blit(TextSurf, TextRect)
    pygame.display.update()


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 != None:
            action()
            time.sleep(0.1)
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    TextSurf, TextRect = text_objects(msg, font)
    TextRect.center = ((x + (w/2)), (y + (h/2)))
    screen.blit(TextSurf, TextRect)

class Play:
    def __init__(self):
        self.deck = Deck()

        self.dealer = Hand()
        self.player = Hand()

        self.playerChips = 1000
        self.playerBet = 10
        self.opChips = 1000
        self.opBet = 10
        self.pot = 0

        self.dealAction = False
        self.action = True

        self.opHold = False

        self.deck.shuffle()

    def deal(self):
        # Resetting previous rounds things
        self.dealAction = True
        if not self.action:
            return
        self.action = False
        self.deck.shuffle()
        screen.fill(background_color)
        pygame.draw.rect(screen, grey, pygame.Rect(0, 0, 250, 700))

        self.dealer = Hand()
        self.player = Hand()

        # Betting things
        self.pot = 0
        self.playerChips -= self.playerBet
        self.opChips -= self.opBet
        self.pot += self.playerBet + self.opBet

        for i in range(2):
            self.dealer.add_card(self.deck.deal())
            self.player.add_card(self.deck.deal())

        self.dealer.display_cards()
        self.player.display_cards()
        self.player_card = 1

        dealer_card = pygame.image.load('img/back.png').convert()
        dealer_card_2 = pygame.image.load('img/back.png').convert()
            
        player_card = pygame.image.load('img/' + self.player.card_img[0] + '.png').convert()
        player_card_2 = pygame.image.load('img/' + self.player.card_img[1] + '.png').convert()

        
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

    def hold(self):
        self.action = True
        if not self.dealAction:
            return
        self.dealAction = False
        print("Okehios")
        self.opHold = bool(random.choice([True, False]))
        if(self.opHold == True):
            op_card = pygame.image.load('img/' + self.dealer.card_img[0] + '.png').convert()
            op_card_2 = pygame.image.load('img/' + self.dealer.card_img[1] + '.png').convert()
            screen.blit(op_card, (400, 200))
            screen.blit(op_card_2, (550, 200))
            val = self.player.comp_hand(self.dealer)
            print(val)
            if val == 1:
                game_texts("You win! " + str(self.pot), 775, 250)
                self.playerChips += self.pot
                self.opBet = self.pot
                self.playerBet = ANTE
                self.pot = 0
            elif val == -1:
                game_texts("You lose", 775, 250)
                self.opChips += self.pot
                self.playerBet = self.pot
                self.opBet = ANTE
                self.pot = 0
            else:
                game_texts("You tie! " + str(math.floor(self.pot/2)), 775, 250)
                self.opChips += self.pot/2
                self.playerChips += self.pot/2
                self.pot = 0
        else:
            game_texts("You win! " + str(self.pot), 775, 250)
            self.playerChips += self.pot
            self.playerBet = ANTE
            self.opBet = ANTE
            self.pot = 0

    def fold(self):
        self.action = True
        if not self.dealAction:
            return
        self.dealAction = False
        self.opHold = bool(random.choice([True, False]))
        if(self.opHold):
            game_texts("You tie! " + str(math.floor(self.pot/2)), 775, 250)
            self.opChips += self.pot/2
            self.playerChips += self.pot/2
            self.pot = 0
        else:
            game_texts("You lose", 775, 250)
            self.opChips += self.pot
            self.playerBet = ANTE
            self.opBet = ANTE
            self.pot = 0



    def exit(self):
        sys.exit()
        
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

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    button("Deal", 30, 100, 150, 50, light_slat, dark_slat, play_guts.deal)
    button("Hold", 30, 200, 150, 50, light_slat, dark_slat, play_guts.hold)
    button("Fold", 30, 300, 150, 50, light_slat, dark_slat, play_guts.fold)
    button("EXIT", 30, 500, 150, 50, light_slat, dark_red, play_guts.exit)
    pygame.display.flip()