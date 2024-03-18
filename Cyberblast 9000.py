import pygame
import sys
import math
import random
from random import randint

# Classes

class Brick:
    def __init__(self, pos, durability):
        # Initialisation d'une brique avec sa position et sa durabilité
        self.__rect = pygame.Rect(pos, brick_size)
        self.__durability = durability
    
    def rect(self):
        # Renvoie le rectangle représentant la brique
        return self.__rect
    
    def durability(self):
        return self.__durability
    
    def boom(self):
        # Réduit la durabilité de la brique lorsqu'elle est touchée par une explosion
        self.__durability -= 1

    def is_destroyed(self):
        # Vérifie si la brique est détruiteclass Brick:
        return self.__durability < 1

# Functions

def bomb_pos():
    # Calcule la position de la bombe en fonction de la position du joueur et de la grille
    player_center = pygame.Vector2(player.center)
    player_relative_pos = player_center - pygame.Vector2(game_window.topleft)
    grid_square_size = pygame.Vector2(brick_size[0] + 2, brick_size[1] + 2)
    player_relative_grid_pos = player_relative_pos.elementwise() // grid_square_size
    grid_square_top_left = player_relative_grid_pos.elementwise() * grid_square_size + pygame.Vector2(margin, margin)
    bomb_position = grid_square_top_left + pygame.Vector2(game_window.topleft) + pygame.Vector2(((brick_size[0] - bomb_size[0] +2)/2, (brick_size[1] - bomb_size[1] + 2)/2 ))
    return bomb_position

def bomb_explosion(bomb, bricks_list, radius, power, strenght):
    # Génère une liste de rectangles représentant l'explosion de la bombe
    explosion_trail = []
    explosion_size = (57, 57)
    explosion_trail.append(pygame.Rect(bomb.centerx - explosion_size[0] // 2, bomb.centery - explosion_size[1] // 2, explosion_size[0], explosion_size[1]))
    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        for i in range(1, radius):
            power_left = power
            collided_with_block = False
            explosion_x = bomb.centerx + dx * i * brick_size[0] - explosion_size[0] // 2
            explosion_y = bomb.centery + dy * i * brick_size[1] - explosion_size[1] // 2
            explosion_rect = pygame.Rect(explosion_x, explosion_y, explosion_size[0], explosion_size[1])
            for brick in bricks_list:
                if explosion_rect.colliderect(brick.rect()):
                    if power_left > 0:
                        for _ in range(strenght):
                            brick.boom()
                        power_left -= 1
                    else:
                        collided_with_block = True
                        break
            if explosion_rect.collidelist(unbreakables_list) != -1:
                break
            explosion_trail.append(explosion_rect)
            if collided_with_block or power_left <= 0:
                break
    return explosion_trail

def brick_number(floor_number):
    min_bricks = floor_number+floor_number//15
    max_bricks = floor_number+floor_number//10
    min_bricks = max(min(min_bricks, 133),50)
    max_bricks = min(max(max_bricks, 50),133)
    return random.randint(min_bricks, max_bricks)

def brick_durability(floor_number):
    rand = random.random()
    p = 1-(math.exp(-floor_number))**0.025
    d3 = round((p / 100 * (30 + floor_number//5)), 2)
    d2 = round((p / 100 * (70 - floor_number//5)), 2)
    if rand < d3:
        return 3
    elif rand < d2 + d3:
        return 2
    else:
        return 1

def gen_bricks(num_bricks, player_pos, floor_key, floor_number):
    # Génère une liste de briques
    bricks_list = []
    for i in range(0, 13):
        for j in range(0, 13):
            brick_pos = ((1 + margin + (game_size[0]-margin*2) / 13 * i + game_window_pos.x), (1 + margin + (game_size[1]-margin*2) / 13 * j + game_window_pos.y))
            brick = Brick(brick_pos, brick_durability(floor_number))
            if not brick.rect().contains(floor_key) and brick.rect().collidelistall(unbreakables_list) == []:
                bricks_list.append(brick)
    player_temp_rect = pygame.Rect(player_pos, (brick_size[0]*2, brick_size[1]*2))
    bricks_list = [brick for brick in bricks_list if not player_temp_rect.colliderect(brick.rect())]
    return random.sample(bricks_list, min(num_bricks, len(bricks_list)))

def gen_floor(floor_number,player_pos):
    # Génère la structure de l'étage
    key_grid_pos = (randint(0, 6) * 2, randint(0, 6) * 2)
    key_size = (25,25)
    key_x = margin/2 + game_window_pos.x + (key_grid_pos[0] * (game_size[0]-margin) / 13) + ((game_size[0]-margin) / 13 - key_size[0]) / 2
    key_y = margin/2 + game_window_pos.y + (key_grid_pos[1] * (game_size[1]-margin) / 13) + ((game_size[1]-margin) / 13 - key_size[1]) / 2
    floor_key = pygame.Rect((key_x, key_y),key_size)
    bricks_list = gen_bricks(brick_number(floor_number), player_pos, floor_key, floor_number)
    return floor_key, bricks_list

def floor_timer(floor_number):
    floor_time = 180 - floor_number-floor_number//2
    floor_time = max(floor_time, 30)
    return floor_time
    
def timer_str(timer_counter):
    # Convertit le compteur de temps en une chaîne de caractères au format "mm:ss"
    timer_minutes = timer_counter // 60
    timer_secondes = timer_counter % 60
    if timer_minutes > 0:
        if timer_secondes >= 10:
            timer_str = str(timer_minutes) + ':' + str(timer_secondes)
        else:
            timer_str = str(timer_minutes) + ':0' + str(timer_secondes)
    else:
        if timer_secondes >= 10:
            timer_str = str(timer_secondes)
        else:
            timer_str = '0' + str(timer_secondes)
    return timer_str

# Initializations

pygame.init()

screen = pygame.display.set_mode((1000, 900))
pygame.display.set_caption('Cyberblast 9000')

screenx = 1000
screeny = 900

game_background = pygame.image.load("game_background.png")
menu_background = pygame.image.load("menu_background.png")
arena_background = pygame.image.load("arena2_background.png")

button_size = (500,100)
play_button = pygame.Rect((screenx / 2 - button_size[0]/2 , 2.5 * screeny / 5 - button_size[1]/2) , button_size)
info_button = pygame.Rect((screenx / 2 - button_size[0]/2 , 3.25 * screeny / 5 - button_size[1]/2) , button_size)
exit_button = pygame.Rect((screenx / 2 - button_size[0]/2 , 4 * screeny / 5 - button_size[1]/2) , button_size)

game_size = (750, 750)
game_window_pos = pygame.Vector2((screenx - game_size[0]) / 2, (screeny - game_size[1]) / 1.5)
game_window = pygame.Rect(game_window_pos, game_size)
margin = 9/2

player_size = (50, 50)
player_starting_pos = pygame.Vector2(game_window_pos)
player = pygame.Rect(player_starting_pos, player_size)

direction = {pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0), pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1)}

bomb_size = (25,25)

brick_size = (55, 55)
unbreakables_pos_list = [[((1 + margin + (game_size[0]-margin*2) / 13 * i + game_window_pos.x), (1 + margin + (game_size[1]-margin*2) / 13 * j + game_window_pos.y)) for i in range(1, 13, 2)] for j in range(1, 13, 2)]
unbreakables_pos_list = sum(unbreakables_pos_list, [])

unbreakables_list = [pygame.Rect(pos, brick_size) for pos in unbreakables_pos_list]

clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000) 

police = pygame.font.SysFont('chalkduster.ttf', 40)
title_police = pygame.font.SysFont('chalkduster.ttf', 130)

key_pressed_state = {}

dt = 0

# Boucle principale

playing = True
in_game = False

while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if not in_game:
        click = pygame.mouse.get_pressed()
        if click[0]:
            if play_button.collidepoint(pygame.mouse.get_pos()):
                in_game = True
                game_over = False
                score_number = 10
                floor_number = 1
                timer_counter = floor_timer(floor_number)
                key_pressed_state = {}
                bomb_timer = -1
                bomb = None
                explosion_trail_timer = -1
                explosion_trail = []
                floor_key, bricks_list = gen_floor(floor_number,player_starting_pos)
                player.topleft = player_starting_pos
                    
            elif exit_button.collidepoint(pygame.mouse.get_pos()):
                playing = False
                
        title = title_police.render("Cyberblast 9000", True, (255, 255, 255))
        title_rect = title.get_rect()
        screen.blit(menu_background, (0, 0))
        screen.blit(title, (screenx / 2 - title_rect.centerx, screeny / 5 - title_rect.centery))
        pygame.draw.rect(menu_background, "black", play_button)
        pygame.draw.rect(menu_background, "black", info_button)
        pygame.draw.rect(menu_background, "black", exit_button)
        pygame.display.update()
    else:
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    if timer_counter > 0:
                        timer_counter -= 1
                    else:
                        game_over, in_game = True, False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and bomb is None:
                        bomb = pygame.Rect(bomb_pos(), bomb_size)
                        bomb_timer = 0
                    elif event.key in direction:
                        key_pressed_state[event.key] = True
                elif event.type == pygame.KEYUP:
                     key_pressed_state[event.key] = False

            player_speed = 200
            player_velocity = pygame.Vector2(0, 0)
            for key, state in key_pressed_state.items():
                if state and key in direction:
                    if key in [pygame.K_LEFT, pygame.K_RIGHT]:
                        player_velocity.x += direction[key][0] * player_speed * dt
                    elif key in [pygame.K_UP, pygame.K_DOWN]:
                        player_velocity.y += direction[key][1] * player_speed * dt

            temp_player = player.move(player_velocity.x, 0)
            if game_window.contains(temp_player) and temp_player.collidelistall(unbreakables_list+[brick.rect() for brick in bricks_list]) == []:
                player.x = temp_player.x

            temp_player = player.move(0, player_velocity.y)
            if game_window.contains(temp_player) and temp_player.collidelistall(unbreakables_list+[brick.rect() for brick in bricks_list]) == []:
                player.y = temp_player.y

            if bomb_timer >= 0:
                bomb_timer += dt
            if bomb_timer >= 1.5:
                explosion_trail = bomb_explosion(bomb, bricks_list, 3, 2, 2)
                bomb = None
                bomb_timer = -1
                explosion_trail_timer = 0

            if explosion_trail_timer >= 0:
                explosion_trail_timer += dt
            if explosion_trail_timer >= 0.5:
                for brick in bricks_list:
                        if brick.is_destroyed():
                            bricks_list.remove(brick)
                            score_number += 10
                explosion_trail_timer = -1
                explosion_trail = []

            if player.colliderect(floor_key):
                floor_number += 1
                score_number += 500
                floor_key, bricks_list = gen_floor(floor_number,player.topleft)
                timer_counter = floor_timer(floor_number)
            if player.collidelistall(explosion_trail):
                game_over, in_game = True, False

            score = police.render(str(score_number), True, (255, 255, 255))
            score_rect = score.get_rect()
            score_center_point = (screenx // 2, 75 // 2)
            score_pos = (score_center_point[0] - score_rect.width // 2, score_center_point[1] - score_rect.height // 2)

            timer = police.render(timer_str(timer_counter), True, (255, 255, 255))
            timer_rect = timer.get_rect()
            timer_center_point = (92.5, 75 // 2)
            timer_pos = (timer_center_point[0] - timer_rect.width // 2, timer_center_point[1] - timer_rect.height // 2)

            floor = police.render(f"Floor : {floor_number}", True, (255, 255, 255))
            floor_rect = floor.get_rect()
            floor_center_point = (screenx-145 , 75 // 2)
            floor_pos = (floor_center_point[0] + 45 - floor_rect.width // 2, floor_center_point[1] - floor_rect.height // 2)

            screen.blit(game_background, (0, 0))
            screen.blit(score, score_pos)
            screen.blit(timer, timer_pos)
            screen.blit(floor, floor_pos)
            game_background.blit(arena_background, game_window_pos)
            for unbreakables_bricks in unbreakables_list:
                pygame.draw.rect(game_background, "purple", unbreakables_bricks)
            for brick in bricks_list:
                match brick.durability():
                    case 1:
                        pygame.draw.rect(game_background, pygame.Color("#ffffff"), brick.rect())
                    case 2:
                        pygame.draw.rect(game_background, pygame.Color("#a8a7a7"), brick.rect())
                    case 3:
                        pygame.draw.rect(game_background, pygame.Color("#707070"), brick.rect())
            for explosion in explosion_trail:
                if game_window.contains(explosion):
                    pygame.draw.rect(game_background, "orange", explosion)
            pygame.draw.rect(game_background, "yellow", floor_key)
            pygame.draw.rect(game_background, "green", player)
            if bomb:
                pygame.draw.rect(game_background, "red", bomb)

            pygame.display.update()

    dt = clock.tick(60) / 1000

pygame.quit()
sys.exit()
