import pygame
import sys
import math
import random

# Classes

class Brick:
    def __init__(self, pos, durability):
        # Initialisation d'une brique avec sa position et sa durabilité
        self.__rect = pygame.Rect(pos, brick_size)
        self.__types = durability
        self.__durability = durability
    
    def rect(self):
        # Renvoie le rectangle représentant la brique
        return self.__rect
    
    def types(self):
        return self.__types
    
    def durability(self):
        return self.__durability
    
    def boom(self):
        # Réduit la durabilité de la brique lorsqu'elle est touchée par une explosion
        self.__durability -= 1

    def is_destroyed(self):
        # Vérifie si la brique est détruiteclass Brick:
        return self.__durability < 1
   
class Powerup:
    def __init__(self, pos, powerup_type):
        self.__rect = pygame.Rect(pos, powerup_size)
        self.__powerup_type = powerup_type
             
    def rect(self):
        return self.__rect
    
    def get_powerup_type(self):
        return self.__powerup_type
    
    def use(self,score_number,radius,strenght,piercing,player_speed,bomb_max_number):
        score_number -= 10
        if self.__powerup_type == "coin" :
            score_number += 15
        if self.__powerup_type == "radius_up" :
            radius += 1
        if self.__powerup_type == "radius_down" :
            if radius > 2:
                radius -= 1
        if self.__powerup_type == "strenght_up" :
            strenght += 1
        if self.__powerup_type == "strenght_down" :
            if strenght > 1:
                strenght -= 1
        if self.__powerup_type == "piercing_up" :
            piercing += 1
        if self.__powerup_type == "piercing_down" :
            if piercing > 1:
                piercing -= 1
        if self.__powerup_type == "speed_up" :
            player_speed += 10
        if self.__powerup_type == "speed_down":
            player_speed -= 10
        if self.__powerup_type == "bomb_number" :
            bomb_max_number += 1
            
class Bomb:
    def __init__(self, pos):
        self.__rect = pygame.Rect(pos, bomb_size)
        self.__pos = pos
        self.__timer = 0
        self.__timer_explosion = -1
        self.__explosion_trail = []
        
    def rect(self):
        return self.__rect
    
    def get_pos(self):
        return self.__pos
    
    def timer(self):
        return self.__timer
        
    def timer_increment(self):
        self.__timer += dt
    
    def explosion_timer_start(self):
        self.__timer_explosion = 0
        self.__timer = -1
        self.__rect = pygame.Rect(0,0,0,0)
    
    def explosion_timer(self):
        return self.__timer_explosion
    
    def explosion_timer_increment(self):
        self.__timer_explosion += dt
        
    def explosion(self, bricks_list, radius, piercing, strenght):
        explosion_size = (57, 57)
        self.__explosion_trail.append(pygame.Rect(self.__rect.centerx - explosion_size[0] // 2, self.__rect.centery - explosion_size[1] // 2, explosion_size[0], explosion_size[1]))
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            for i in range(1, radius):
                piercing_left = piercing
                collided_with_block = False
                explosion_x = self.__rect.centerx + dx * i * brick_size[0] - explosion_size[0] // 2
                explosion_y = self.__rect.centery + dy * i * brick_size[1] - explosion_size[1] // 2
                explosion_rect = pygame.Rect(explosion_x, explosion_y, explosion_size[0], explosion_size[1])
                for brick in bricks_list:
                    if explosion_rect.colliderect(brick.rect()):
                        if piercing_left > 0:
                            for _ in range(strenght):
                                brick.boom()
                            piercing_left -= 1
                        else:
                            collided_with_block = True
                            break
                if explosion_rect.collidelist(unbreakables_list) != -1:
                    break
                self.__explosion_trail.append(explosion_rect)
                if collided_with_block or piercing_left <= 0:
                    break
                
    def get_explosion_trail(self):
        return self.__explosion_trail
    
# Functions

def relative_pos(relative_rect_size, rect):
    # Calcule la position de la bombe en fonction de la position du joueur et de la grille
    rect_center = pygame.Vector2(rect.center)
    rect_relative_pos = rect_center - pygame.Vector2(game_window.topleft)
    grid_square_size = pygame.Vector2(brick_size[0] + 2, brick_size[1] + 2)
    rect_relative_grid_pos = rect_relative_pos.elementwise() // grid_square_size
    grid_square_top_left = rect_relative_grid_pos.elementwise() * grid_square_size + pygame.Vector2(margin, margin)
    relative_rect_position = grid_square_top_left + pygame.Vector2(game_window.topleft) + pygame.Vector2(((brick_size[0] - relative_rect_size[0] +2)/2, (brick_size[1] - relative_rect_size[1] + 2)/2 ))
    return relative_rect_position

def powerup_appear(score_number,radius,strenght,piercing,player_speed,bomb_max_number):
    rand = random.random()
    power_up = None
    if rand < 0.2:
        rand_power_up = random.random()
        if rand_power_up < 0.075:
            power_up = random.choice(["strenght_down", "piercing_down", "radius_down", "speed_down"])
        elif rand_power_up < 0.1:
            power_up = random.choice(["bomb_number", "piercing_up"])
        elif rand_power_up < 0.3:
            power_up = random.choice(["strenght_up", "radius_up"])
        elif rand_power_up < 0.5:
            power_up = "speed_up"
        else:
            power_up = "coin"
    return power_up

def brick_number(floor_number):
    min_bricks = floor_number+floor_number//15
    max_bricks = floor_number+floor_number//10
    min_bricks = max(min(min_bricks, 100),50)
    max_bricks = min(max(max_bricks, 50),100)
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
    key_grid_pos = (random.randint(0, 6) * 2, random.randint(0, 6) * 2)
    key_size = (25,25)
    key_x = margin/2 + game_window_pos.x + (key_grid_pos[0] * (game_size[0]-margin) / 13) + ((game_size[0]-margin) / 13 - key_size[0]) / 2
    key_y = margin/2 + game_window_pos.y + (key_grid_pos[1] * (game_size[1]-margin) / 13) + ((game_size[1]-margin) / 13 - key_size[1]) / 2
    floor_key = pygame.Rect((key_x, key_y),key_size)
    bricks_list = gen_bricks(brick_number(floor_number), player_pos, floor_key, floor_number)
    trap = ((random.choice(bricks_list)).rect()).copy()
    return trap, floor_key, bricks_list

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

game_background = pygame.image.load("image/game_background.png")
menu_background = pygame.image.load("image/menu_background.png")
arena_background = pygame.image.load("image/arena_background.png")
key_sprite = pygame.image.load("image/key.png")
key_sprite.set_colorkey((0, 255, 0))
trapdoor_sprite = pygame.image.load("image/trapdoor.png")
brick_1hit_sprite = pygame.image.load("image/1hit_brick.png")
brick_2hit_1_sprite = pygame.image.load("image/2hit_1_brick.png")
brick_2hit_2_sprite = pygame.image.load("image/2hit_2_brick.png")
brick_3hit_1_sprite = pygame.image.load("image/3hit_1_brick.png")
brick_3hit_2_sprite = pygame.image.load("image/3hit_2_brick.png")
brick_3hit_3_sprite = pygame.image.load("image/3hit_3_brick.png")
indestructible_brick_sprite = pygame.image.load("image/indestructible_brick.png")

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
key_size = (25,25)
powerup_size = (20,20)
key_picked_up = False

brick_size = (55, 55)
unbreakables_pos_list = [[((1 + margin + (game_size[0]-margin*2) / 13 * i + game_window_pos.x), (1 + margin + (game_size[1]-margin*2) / 13 * j + game_window_pos.y)) for i in range(1, 13, 2)] for j in range(1, 13, 2)]
unbreakables_pos_list = sum(unbreakables_pos_list, [])

unbreakables_list = [pygame.Rect(pos, brick_size) for pos in unbreakables_pos_list]

FPS = 60
clock = pygame.time.Clock()
clock.tick(FPS)

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
                score_number = 500
                floor_number = 50
                timer_counter = floor_timer(floor_number)
                key_pressed_state = {}
                powerup_on_grid = []
                bomb_on_grid = []
                bomb_max_number = 3
                explosion_on_grid = []
                trap, floor_key, bricks_list = gen_floor(floor_number,player_starting_pos)
                player.topleft = player_starting_pos
                radius, piercing, strenght = 2,1,1
                    
            elif exit_button.collidepoint(pygame.mouse.get_pos()):
                playing = False
                
        screen.blit(menu_background, (0, 0))
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
                    if event.key == pygame.K_SPACE and len(bomb_on_grid) < bomb_max_number and relative_pos(bomb_size, player) not in [bomb.get_pos() for bomb in bomb_on_grid]:
                        bomb_on_grid.append(Bomb(relative_pos(bomb_size, player)))
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
            
            for bomb in bomb_on_grid:
                if bomb.timer() >= 0:
                    bomb.timer_increment()
                if bomb.timer() >= 1.5:
                    bomb.explosion(bricks_list, radius, piercing, strenght)
                    bomb.explosion_timer_start()
                if bomb.explosion_timer() >= 0:
                    bomb.explosion_timer_increment()
                if bomb.explosion_timer() >= 0.5:
                    for brick in bricks_list:
                        if brick.is_destroyed():
                            powerup = powerup_appear(score_number,radius,strenght,piercing,player_speed,bomb_max_number)
                            if powerup != None:
                                powerup_on_grid.append(Powerup(relative_pos(powerup_size,brick.rect()), powerup))
                            bricks_list.remove(brick)
                    bomb_on_grid.remove(bomb)
            
            if player.colliderect(floor_key):
                key_picked_up = True
            if player.colliderect(trap) and key_picked_up:
                floor_number += 1
                score_number += 100
                trap, floor_key, bricks_list = gen_floor(floor_number,player.topleft)
                timer_counter = floor_timer(floor_number)
            for bomb in bomb_on_grid:
                if player.collidelistall(bomb.get_explosion_trail()):
                    game_over, in_game = True, False
            for powerup in powerup_on_grid:
                if player.colliderect(powerup):
                    powerup.use(score_number,radius,strenght,piercing,player_speed,bomb_max_number)
                    powerup_on_grid.remove(powerup)
                    
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
                game_background.blit(indestructible_brick_sprite, unbreakables_bricks)
            for brick in bricks_list:
                if brick.types() == 1 :
                    game_background.blit(brick_1hit_sprite, brick.rect())
                elif brick.types() == 2 :
                    if brick.durability() == 1:
                        game_background.blit(brick_2hit_1_sprite, brick.rect())
                    elif brick.durability() == 2:
                        game_background.blit(brick_2hit_2_sprite, brick.rect())
                elif brick.types() == 3 :
                    if brick.durability() == 1:
                        game_background.blit(brick_3hit_1_sprite, brick.rect())
                    elif brick.durability() == 2:
                        game_background.blit(brick_3hit_2_sprite, brick.rect())
                    elif brick.durability() == 3:
                        game_background.blit(brick_3hit_3_sprite, brick.rect())
            if trap.collidelist(bricks_list) == -1:
                game_background.blit(trapdoor_sprite, brick.rect())
            if not key_picked_up:
                game_background.blit(key_sprite, floor_key)
            for powerup in powerup_on_grid:
                pygame.draw.rect(game_background, "cyan", powerup.rect())
            pygame.draw.rect(game_background, "green", player)
            for bomb in bomb_on_grid:
                pygame.draw.rect(game_background, "red", bomb.rect() )
                for explosion in bomb.get_explosion_trail():
                    if game_window.contains(explosion):
                        pygame.draw.rect(game_background, "orange", explosion)
            pygame.display.update()
            clock.tick(FPS)

    dt = round((clock.tick(FPS) / 1000) , 2)

pygame.quit()
sys.exit()
