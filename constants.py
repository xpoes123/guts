# Program that stores all the variables that I may reference multiple times.

import pygame as pygame

display_width = 1200
display_height = 700

background_color = (34,139,34)
grey = (220,220,220)
black = (0,0,0)
green = (0, 200, 0)
red = (255,0,0)
light_slat = (119,136,153)
dark_slat = (47, 79, 79)
dark_red = (255, 0, 0)
pygame.init()
fontName = "calibri"
font = pygame.font.SysFont(fontName, 20)
textfont = pygame.font.SysFont(fontName, 35)


SUITS = ['C', 'S', 'H', 'D']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)

ANTE = 10
STARTSTACK = 300
