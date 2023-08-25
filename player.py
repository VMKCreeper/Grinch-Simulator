# MAX
import pygame
import variables
from pygame.locals import *
from timer import Timer
from typing import List

class Player:
    def __init__(self, x: int, y: int, keys: List[str]) -> None:
        self.rect = pygame.Rect(x, y, 40, 50)
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 5.5
        self.gravity = 0.8
        self.score = 0
        self.jump = 15
        self.ability_type = 0
        self.keys = keys
        self.num_jump = 0
        self.double_jump = False
        self.bhop = False
        self.Ground = False
        self.toggle = False
        self.flip = False
        self.duration = Timer(5)
        self.cd = Timer(0)

    def drawCharacter(self, img: pygame.image, surface: pygame.Surface) -> None:
        if self.flip:
            image = pygame.transform.flip(img, True, False)
        else:
            image = img
        surface.blit(image, [self.rect.x, self.rect.y])

        if self.rect.x < 0:
            surface.blit(image, [variables.WIDTH + self.rect.x, self.rect.y])
        elif self.rect.x > 1860:
            surface.blit(image, [self.rect.x - variables.WIDTH, self.rect.y])

    def ability(self) -> None:
        """Gets the abilities and applies them"""
        if self.cd.countdown():
            if self.toggle:
                if self.ability_type == 1:
                    self.double_jump = True
                    if self.Ground:
                        self.num_jump = 2
                elif self.ability_type == 2:
                    self.speed = 8
                elif self.ability_type == 3:
                    self.jump = 25
                
                if self.duration.countdown():
                    self.jump = 15
                    self.speed = 5.5
                    self.gravity = 0.8
                    self.cd = Timer(15)
                    self.duration = Timer(5)
                    self.double_jump = False
                    self.toggle = False
                    self.snowball = False

    def player_updates(self, platform: List[pygame.Rect], slime: List[pygame.Rect]) -> None:
        """Applies updates to the player class
        
        Args:
            platform (List): List of solid blocks
            slime (List): List of slime blocks
        
        """
        #gravity
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

        # on ground?
        if self.direction.y != 0.8 and self.direction.y != 0:
            self.Ground = False

        # Platform logic
        for testplat in platform:
            if self.rect.colliderect(testplat) and self.direction.y > 0:
                self.Ground = True

        # collision
        for testplat in platform:
            if self.rect.colliderect(testplat):
                if self.direction.y > 0:
                    self.rect.bottom = testplat.top
                    self.direction.y = 0  # RESET
                elif self.direction.y < 0:
                    self.rect.top = testplat.bottom
                    self.direction.y = 0

        self.rect.x += self.direction.x

        for testplat in platform:
            if self.rect.colliderect(testplat):
                if self.direction.x < 0:
                    self.rect.left = testplat.right
                elif self.direction.x > 0:
                    self.rect.right = testplat.left

        # bhop
        if self.bhop:
            if self.Ground:
                self.direction.y = -(self.jump)

        # spring 
        for slimes in slime:
            if self.rect.colliderect(slimes):
                    self.direction.y = -25

        # split screen
        if self.rect.x < -39:
            self.rect.x = 1860
        elif self.rect.x > 1899:
            self.rect.x = 0

    def key_inputs(self, event: pygame.event, gamemode: int, player: 'Player') -> None:
        if event.type == KEYDOWN:
            if event.key == self.keys[0]:
                if self.Ground:
                    self.direction.y = -(self.jump)
                elif self.num_jump == 1 and self.double_jump:
                    self.direction.y = -(self.jump)
                    self.num_jump = 0
                self.bhop = True
                if gamemode == 2 or gamemode == 3:
                    self.num_jump -= 1
                    # footstool
                    if self.rect.colliderect(player.rect):
                        self.direction.y = -15
                        player.direction.y = 15
                
            if event.key == self.keys[1]:
                self.direction.x = -(self.speed)
                self.flip = True
            elif event.key == self.keys[2]:
                self.direction.x = self.speed
                self.flip = False
            elif event.key == self.keys[3] and self.cd.initial <= 0 and self.ability_type != 0:
                self.toggle = True
        if event.type == KEYUP:
            if event.key == self.keys[0]:
                self.bhop = False
            elif event.key == self.keys[1] and self.direction.x < 0:
                self.direction.x = 0
            elif event.key == self.keys[2] and self.direction.x > 0:
                self.direction.x = 0
