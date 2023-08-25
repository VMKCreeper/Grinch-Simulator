import pygame

# Screen Properties
WIDTH = 1900
HEIGHT = 1000

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (37, 197, 223)
RED = (254, 22, 35)
GREEN = (0, 255, 0)
GREEN2 = (168, 29, 40)
BLUE2 = (24, 92, 165)
GREY = (80, 80, 80)
ORANGE = (255, 98, 0)

# Images
textures = [
    pygame.image.load('images/ground.png'),
    pygame.image.load('images/oak.png'),
    pygame.image.load('images/slime.png'),
    pygame.image.load('images/stonebrick.png'),
    pygame.image.load('images/branch.png'),
    pygame.image.load('images/oak.png'),
    pygame.image.load('images/sun.png'),
    pygame.image.load('images/leaves.png'),
    pygame.image.load('images/cred.png'),
    pygame.image.load('images/cwhite.png'),
    pygame.image.load('images/chimney.png'),
    pygame.image.load('images/birch.png'),
    pygame.image.load('images/glass.png')
]

abilities = [
    pygame.image.load('images/noability.png'),
    pygame.image.load('images/doublejump.png'),
    pygame.image.load('images/speed.png'),
    pygame.image.load('images/jump.png')
]

player1 = pygame.image.load('images/p1.png')
player2 = pygame.image.load('images/p2.png')
present_img = pygame.image.load('images/present.png')
instructions_background = pygame.image.load('images/instructions.png')
end_background = pygame.image.load('images/endscreen.png')
wasd = pygame.image.load('images/WASD.png')
ijkl = pygame.image.load('images/IJKL.png')

# Fonts

pygame.font.init()

font = pygame.font.SysFont('Tahoma', 70)
font_two = pygame.font.SysFont('Couriernew', 25)
font_three = pygame.font.SysFont('Times New Roman', 25)
cd_text = pygame.font.SysFont('Consolas', 50, True)
game_text = pygame.font.SysFont('Times New Roman', 80)
title_font = pygame.font.SysFont('Default', 300)
