import pickle
import pygame
import random
import math
import variables
from player import Player
from timer import Timer
from typing import List

class Game:
    def __init__(self) -> None: # RYAN
        with open('map.pkl', 'rb') as f:
            self.map = pickle.load(f)
            f.close()

        self.snow_list = []
        for _ in range(500):
            self.snow_list.append(pygame.Vector3(random.randrange(variables.WIDTH),
                                                 random.randrange(variables.HEIGHT),
                                                 random.randrange(1, 10)))
        
        self.new = False

    def draw_snow(self, surface: pygame.Surface, snow_speed: int) -> None: # RYAN
        for snow in self.snow_list:
            pygame.draw.circle(surface, variables.WHITE, (snow.x, snow.y), 5 * snow.z//10)
            snow.y += snow_speed * snow.z / 10
            
            if snow.y > variables.HEIGHT:
                snow.y = random.randrange(-100, -200, -100)
                snow.x = random.randrange(variables.WIDTH)


    def draw_map(self, surface: pygame.Surface) -> None: # MAX
        """Draws the map onto the screen
        
        surface (pygame.display.set_mode()): Surface to be drawn on
        """
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == 0:
                    continue
                surface.blit(pygame.transform.scale(variables.textures[self.map[i][j] - 1], (50, 50)), (j * 50, i * 50, 50, 5))

    def ability_icons(self, surface: pygame.Surface, player: Player, x: int, y: int) -> None: # MAX
        icon = variables.abilities[player.ability_type]
        if player.cd.initial <= 0:
            icon.set_alpha(255)
        elif player.duration:
            icon.set_alpha(100)

        if player.toggle:
            self.x += 1
            icon.set_alpha(77 * math.cos(0.1*self.x) + 177)
 
        surface.blit(pygame.transform.scale(variables.abilities[player.ability_type], (100, 100)), [x, y])

        if player.cd.initial > 0:
            text = variables.cd_text.render(player.cd.convert_to_datetime(5, 7), True, variables.WHITE)
            surface.blit(text, [x + 25, y + 30])

    def collision_tiles(self, collisionTile: List[pygame.Rect], platform: List[pygame.Rect], slime: List[pygame.Rect]) -> None: # MAX
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                for k in range(len(collisionTile)):
                    if self.map[i][j] == collisionTile[k]:
                        platform.append(pygame.Rect(j * 50, i * 50, 50, 50))
                    elif self.map[i][j] == 3:
                        slime.append(pygame.Rect(j * 50, i * 50, 50, 50))
    
    def check_win(self, gamemode: int, p1: Player, p2: Player, game_timer: Timer, highscore: List[int]) -> bool: # MAX
        """ Checks if the player has won or lost
        Args:
            gamemode (int): Interger representing gamemode
            p1 (Player): 
            p2 (Player): 
            game_timer (Timer): 
            highscore (List): List of highscores to be updated
            
        Returns:
            bool: True if the game has ended
        """
        if gamemode == 0:
            if p1.score == 10 or game_timer.countdown():
                return True
        elif gamemode == 1:
            if game_timer.countdown():
                if p1.score > highscore[0]:
                    highscore[0] = p1.score
                    self.new = True
                return True
        elif gamemode == 2:
            if game_timer.countdown():
              return True
        elif gamemode == 3:
            if game_timer.countdown():
                if p1.score + p2.score > highscore[1]:
                    highscore[1] = p1.score + p2.score
                    self.new = True
                return True
    
    def draw_ability_list(self, surface: pygame.Surface, p1_coords_list: List[int], p2_coords_list: List[int], p1: Player, p2: Player) -> None: # RYAN
        for i in range(len(variables.abilities)):
            # fixes opacity bug
            variables.abilities[i].set_alpha(255)
            surface.blit(pygame.transform.scale(variables.abilities[i], (100, 100)), p1_coords_list[i])
            surface.blit(pygame.transform.scale(variables.abilities[i], (100, 100)), p2_coords_list[i])

            pygame.draw.rect(surface, variables.BLUE, [p1_coords_list[p1.ability_type][0], p1_coords_list[p1.ability_type][1], 100, 100], 3)
            pygame.draw.rect(surface, variables.BLUE, [p2_coords_list[p2.ability_type][0], p2_coords_list[p2.ability_type][1], 100, 100], 3)

        text = variables.font_two.render("Use key S/K to activate ability", True, variables.BLACK)
        surface.blit(text, [1350, 720])

        text = variables.font_three.render("    None     Double Jump    Speed       Jumpboost", True, variables.BLACK)
        surface.blit(text, [1350, 370])
