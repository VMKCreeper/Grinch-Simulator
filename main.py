import pygame
import pickle
import variables
from game import Game
from present import Present
from player import Player
from timer import Timer
from pygame.locals import *

try:
    with open('highscore.pkl', 'rb') as f:
        highscore = pickle.load(f)
        f.close()
except:  # first time opening file
    highscore = [0, 0]

pygame.init()

game = Game()
p = Present()

# SCREEN PROPERTIES
size = (variables.WIDTH, variables.HEIGHT)
screen = pygame.display.set_mode(size)

# BOUNDARY
platform = [pygame.Rect(-1, 500, 1, 250),
            pygame.Rect(variables.WIDTH, 750, 1, 50)]

# COLLISION TILES
slime = []
collisionTile = [1, 4, 5, 6, 9, 10]
game.collision_tiles(collisionTile, platform, slime)

# ABILITY SELECTOR
# 125, 150
p1_coords = [[1350, 420], [1475, 420], [1600, 420], [1725, 420]]
p2_coords = [[1350, 580], [1475, 580], [1600, 580], [1725, 580]]

p1_buttons = [pygame.Rect((i), (100, 100)) for i in p1_coords]
p2_buttons = [pygame.Rect((i), (100, 100)) for i in p2_coords]

# MAIN MENU BUTTONS
main_menu_buttons = []
for i, y_offset in enumerate(range(400, 701, 150)):
    main_menu_buttons.append(pygame.Rect(750, y_offset, 400, 100))

# PAUSE BUTTONS
pause_buttons = []
for i, y_offset in enumerate(range(375, 676, 150)):
    pause_buttons.append(pygame.Rect(750, y_offset, 400, 100))

# GAME LOGIC
current_screen = 0
gamemode = 0
menu = 0

def reset(seconds: int) -> None:
    global p1, p2
    global snow_speed, timer, pause, menu, cd_timer, game_timer
    p1 = Player(200, 300, [K_w, K_a, K_d, K_s])
    p2 = Player(1800, 300, [K_i, K_j, K_l, K_k])
    snow_speed = 2
    game_timer = Timer(seconds)
    pause = False
    menu = 0
    cd_timer = Timer(4)
    p.present_reset(gamemode, p1, p2)
    game.new = False
    game.x = 0

pygame.display.set_caption("Grinch Simulator")
clock = pygame.time.Clock()
# -------- Main Program Loop -----------
done = False
while not done:
    # --- Main event loop ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == MOUSEBUTTONDOWN:
            if current_screen == 0:
                for button in main_menu_buttons:
                    if button.collidepoint(event.pos):
                        if main_menu_buttons.index(button) == 2:
                            if menu == 0:
                                menu = 1
                            else:
                                menu = 0
                        elif menu == 0:
                            gamemode = main_menu_buttons.index(button)
                            reset(60 + main_menu_buttons.index(button) * 30)
                            current_screen = 1
                        elif menu == 1:
                            gamemode = main_menu_buttons.index(button) + 2
                            reset(120)
                            current_screen = 1

            elif current_screen == 1 and gamemode > 1:
                for button in p1_buttons:
                    if button.collidepoint(event.pos):
                        p1.ability_type = p1_buttons.index(button)
                for button in p2_buttons:
                    if button.collidepoint(event.pos):
                        p2.ability_type = p2_buttons.index(button)
    
            elif current_screen == 3:
                if pause_buttons[1].collidepoint(event.pos):
                    reset(60 + 30 * gamemode)
                    current_screen = 1
                elif pause_buttons[2].collidepoint(event.pos):
                    current_screen = 0
            elif pause:
                if pause_buttons[0].collidepoint(event.pos):
                    pause = False
                    snow_speed = 2
                elif pause_buttons[1].collidepoint(event.pos):
                    reset(60 + 30 * gamemode)
                    current_screen = 1
                elif pause_buttons[2].collidepoint(event.pos):
                    current_screen = 0

        elif current_screen == 1:
            if event.type == KEYDOWN:  #start game from instruction
                if event.key == K_SPACE:
                    current_screen = 2
                elif event.key == K_ESCAPE:
                    current_screen = 0

        elif current_screen == 2:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # Pause
                    pause = True
                    snow_speed = 0
            if cd_timer.initial <= 0:
                p1.key_inputs(event, gamemode, p2)
                p2.key_inputs(event, gamemode, p1)

    screen.fill(variables.BLUE)

    if current_screen == 0:  # MENU
        game.draw_snow(screen, 2)
        title = variables.title_font.render("Grinch Simulator", True, variables.GREEN)
        text_rect = title.get_rect(center = (variables.WIDTH // 2, 150))
        screen.blit(title, [text_rect.x, text_rect.y])
        screen.blit(pygame.transform.scale(variables.present_img, [500, 500]), [700, 350])
        if menu == 0:
            m_text = ["Demo", "Highscore", "2 Player"]
        elif menu == 1:
            m_text = ["1v1", "Co-op mode", "Back"]

        for i, y_offset in enumerate(range(450, 751, 150)):
            pygame.draw.rect(screen, variables.WHITE, main_menu_buttons[i])
            message = variables.font.render(m_text[i], True, variables.BLACK)
            text_rect = message.get_rect(center = (variables.WIDTH // 2, y_offset))
            screen.blit(message, [text_rect.x, text_rect.y])

        screen.blit(pygame.transform.scale(variables.player1, [400, 500]), [50, 350])
        screen.blit(pygame.transform.scale(pygame.transform.flip(variables.player2, True, False), [400, 500]), [1450, 350])

    elif current_screen == 1: # INSTRUCTIONS
        # FIX LATER
        screen.blit(variables.instructions_background, [0, 0])    
        instructions_text = [
        ["Demo Game", "Goal: Collect 10 presents before the timer hits 0!", "  use           to move.", "Press Space to begin"],
        ["Highscore Mode", "Goal: Collect as many presents as you can in 1.5 Minute!", "  use           to move.", "Press Space to begin"],
        ["1v1 Mode", "Goal: Collect more presents than your opponent!", "  use           to Move", "  use           to Move", "Press Space to begin"],
        ["Co-op Mode", "Goal: Collect as many presents as you can in 2 Minutes!", "  use           to Move",  " use           to Move", "Press Space to Begin"]
        ]
        
        y_offset = 50
        for i in range(len(instructions_text[gamemode])):
            if i == 0:
                text = variables.font.render(instructions_text[gamemode][i], True, variables.GREEN2)
            else:
                text = variables.font.render(instructions_text[gamemode][i], True, variables.BLACK)
            text_rect = text.get_rect(center = (variables.WIDTH // 2, y_offset))
            screen.blit(text, [text_rect.x, text_rect.y])
            y_offset += 200

        screen.blit(pygame.transform.scale(variables.wasd, [250, 170]), [775, 350])
        screen.blit(pygame.transform.scale(variables.player1, [100, 125]), [550, 380])
        if gamemode == 2 or gamemode == 3:
            game.draw_ability_list(screen, p1_coords, p2_coords, p1, p2)
            screen.blit(pygame.transform.scale(variables.ijkl, [215, 135]), [790, 565])
            screen.blit(pygame.transform.scale(variables.player2, [100, 125]), [550, 595])

    elif current_screen == 2:  # MAIN GAME
        if not pause:
            if cd_timer.countdown():
                p1.player_updates(platform, slime)
                if gamemode == 2 or gamemode == 3:
                    p2.player_updates(platform, slime)
                    p1.ability()
                    p2.ability()
                    
                p.apply_gravity()
                p.present_collision(gamemode, slime, platform, p1, p2)

                # game end
                if game.check_win(gamemode, p1, p2, game_timer, highscore):
                    current_screen = 3

        # Drawing
        game.draw_snow(screen, snow_speed)
        game.draw_map(screen)

        # top mid design
        pygame.draw.polygon(screen, variables.WHITE, ([475, 0], [525, 100], [1375, 100], [1425, 0]))
        pygame.draw.polygon(screen, variables.GREY, ([475, 0], [525, 100], [1375, 100], [1425, 0]), 5)

        # Timer text
        clock_t = variables.game_text.render(f"<{game_timer.convert_to_datetime(2, 7)}>", True, variables.BLACK)
        text_rect = clock_t.get_rect(center = (variables.WIDTH / 2, 25))
        screen.blit(clock_t, [text_rect.x, text_rect.y + 25])

        # Score counter / Players
        ptext = variables.font.render("P1", True, variables.RED)
        screen.blit(ptext, [530, 10])
        p_counter = variables.font_two.render(f"Presents: {p1.score}", True, variables.BLACK)
        screen.blit(p_counter, [625, 35])
        p1.drawCharacter(variables.player1, screen)

        if gamemode == 2 or gamemode == 3:
            ptext = variables.font.render("P2", True, variables.BLUE2)
            screen.blit(ptext, [1285, 10])
            p_counter = variables.font_two.render(f"Presents: {p2.score}", True, variables.BLACK)
            screen.blit(p_counter, [1100, 35])
            p2.drawCharacter(variables.player2, screen)

            # ability icons
            game.ability_icons(screen, p1, 350, 5)
            game.ability_icons(screen, p2, 1450, 5)

        # Present
        screen.blit(variables.present_img, (p.present.x, p.present.y))

        #countdown
        if cd_timer.initial >= 0:
            if cd_timer.initial < 1:
                countdown_text = variables.title_font.render("GO!", True, variables.ORANGE)
            else:
                countdown_text = variables.title_font.render(cd_timer.convert_to_datetime(6, 7), True, variables.ORANGE)
            text_rect = countdown_text.get_rect(center = (variables.WIDTH / 2, 500))
            screen.blit(countdown_text, [text_rect.x, text_rect.y])

        if pause:
            # opacity
            s = pygame.Surface((variables.WIDTH, variables.HEIGHT))
            s.set_alpha(150)
            s.fill(variables.BLACK)
            screen.blit(s, (0, 0))
            
            text = ["Resume", "Restart", "Main Menu"]
            for i, y_offset in enumerate(range(425, 751, 150)):
                pygame.draw.rect(screen, variables.WHITE, pause_buttons[i])
                message = variables.font.render(text[i], True, variables.BLACK)
                text_rect = message.get_rect(center = (variables.WIDTH / 2, y_offset))
                screen.blit(message, (text_rect.x, text_rect.y))

    elif current_screen == 3: # END SCREEN
        screen.blit(variables.end_background, [0, 0])
        if gamemode == 0:  
            if p1.score == 10:
                result = variables.font.render("You won!", True, variables.BLACK) 
                score = variables.font.render(f"Time elapsed: {game_timer.get_elapsed_time(60, 5, 10)} seconds", True, variables.BLACK)
            else:
                result = variables.font.render("You lost", True, variables.BLACK)  
                score = variables.font.render(f"Presents collected: {p1.score}", True, variables.BLACK)

        elif gamemode == 1:
            result = variables.font.render(f"Presents collected: {p1.score}", True, variables.BLACK)

            if game.new:
                score = variables.font.render(f"New highscore: {highscore[0]}", True, variables.BLACK)
            else:
                score = variables.font.render(f"Highscore: {highscore[0]}", True, variables.BLACK)

        elif gamemode == 2:
            if p1.score > p2.score:  # PLAYER 1 WIN
                result = variables.font.render("Player 1 Wins!", True, variables.BLACK)
            elif p2.score > p1.score: # PLAYER 2 WIN
                result = variables.font.render("Player 2 Wins!", True, variables.BLACK)
            else:
                result = variables.font.render("It's a tie!", True, variables.BLACK)

            score = variables.font.render(f"Player 1: {p1.score}   |   Player 2: {p2.score}", True, variables.BLACK)

        elif gamemode == 3:
            result = variables.font.render(f"Presents collected: {p1.score + p2.score}", True, variables.BLACK)
            if game.new:
                score = variables.font.render(f"New highscore: {highscore[1]}", True, variables.BLACK)
            else:
                score = variables.font.render(f"Highscore: {highscore[1]}", True, variables.BLACK)

        # blitting text
        text_rect = result.get_rect(center = (variables.WIDTH / 2, 200))
        screen.blit(result, (text_rect.x, text_rect.y))
        text_rect = score.get_rect(center = (variables.WIDTH / 2, 350))
        screen.blit(score, (text_rect.x, text_rect.y))

        text = ["Restart", "Main Menu"]
        for i, y_offset in enumerate(range(575, 726, 150)):
            pygame.draw.rect(screen, variables.WHITE, pause_buttons[i + 1])
            message = variables.font.render(text[i], True, variables.BLACK)
            text_rect = message.get_rect(center = (variables.WIDTH / 2, y_offset))
            screen.blit(message, (text_rect.x, text_rect.y))

        # Easter egg
        if p1.score == 8 and p2.score == 6:
            text = variables.font_two.render("Shoutouts David Bi for the player models", True, variables.BLACK)
            screen.blit(text, [1275, 950])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

with open('highscore.pkl', 'wb') as f:
    pickle.dump(highscore, f)
    f.close()
