# RYAN
import random
import pygame
import variables
from typing import List
from player import Player

class Present:
    def __init__(self) -> None:
        self.present = pygame.Rect(0, 0, 50, 50)
        self.present_gravity = 0
        
    def present_reset(self, gamemode: int, p1: Player, p2: Player) -> None:
        """Resets the present location after getting collected
        
        Args:
            gamemode (int): interger representing gamemode
            p1 (Player): Player class
            p2 (Player): Player class
        """
        if gamemode == 2:
            if random.randrange(4) == 0:
                self.present.x = (p1.rect.x + p2.rect.x) // 2
            else:
                self.present.x = random.randrange(0, variables.WIDTH, 50)
        else:
            self.present.x = random.randrange(0, variables.WIDTH, 50)

        self.present.y = random.randrange(0, variables.HEIGHT - 50, 50)
        self.present_gravity = 0

    def present_collision(self, gamemode: int, slime: List[pygame.Rect], plat: List[pygame.Rect], p1: Player, p2: Player) -> None:
        """Checks if present collides with player or platform and applies updates
        Args:
            gamemode (int): integer representing gamemode
            slime: (List): List of pygame.Rect for collision
            plat: (List): List of pygame.Rect for collision
            p1 (Player): Player class
            p2 (Player): Player class
        """
        for platform in plat:
            if platform.colliderect(self.present):
                self.present.bottom = platform.top
                self.present_gravity = 0

        if p1.rect.colliderect(self.present):
            p1.score += 1
            self.present_reset(gamemode, p1, p2)
        elif p2.rect.colliderect(self.present):
            if gamemode > 1:
                p2.score += 1
                self.present_reset(gamemode, p1, p2)

        for slimes in slime:
            if slimes.colliderect(self.present):
                self.present_gravity = -13

    def apply_gravity(self) -> None:
        self.present_gravity += 0.4
        self.present.y += self.present_gravity
