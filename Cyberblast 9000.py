import math
import os
import random
import sys

import pygame


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
        if powerup_type in ["shield", "poison"]:
            self.__effect = True
        else:
            self.__effect = False
        self.__powerup_type = powerup_type
        self.__timer = 0

    def rect(self):
        return self.__rect

    def is_effect(self):
        return self.__effect

    def timer(self):
        return self.__timer

    def timer_increment(self):
        self.__timer += dt

    def get_powerup_type(self):
        return self.__powerup_type

    def use_effect(self,score_number):
        return score_number - 10
        
    def use(self, score_number, radius, strenght, piercing, player_speed, bomb_max_number):
        
        if not self.__effect:
            if self.__powerup_type == "coin":
                coin_pickup_sfx.play()
                score_number += 5
            else :
                item_pickup_sfx.play()
                score_number -= 10
                if self.__powerup_type == "radius_up":
                    
                    radius += 1
                elif self.__powerup_type == "radius_down":
                    if radius > 2:
                        radius -= 1
                elif self.__powerup_type == "strenght_up":
                    strenght += 1
                elif self.__powerup_type == "strenght_down":
                    if strenght > 1:
                        strenght -= 1
                elif self.__powerup_type == "piercing_up":
                    piercing += 1
                elif self.__powerup_type == "piercing_down":
                    if piercing > 1:
                        piercing -= 1
                elif self.__powerup_type == "speed_up":
                    player_speed += 25
                elif self.__powerup_type == "speed_down":
                    player_speed -= 25
                elif self.__powerup_type == "bomb_number_up":
                    bomb_max_number += 1
                elif self.__powerup_type == "bomb_number_down":
                    if bomb_max_number > 1:
                        bomb_max_number -= 1
            return (score_number, radius, strenght, piercing, player_speed, bomb_max_number)

    def sprite(self):
        if self.__powerup_type == "coin":
            return coin_sprite
        elif self.__powerup_type == "radius_up":
            return rangeup_sprite
        elif self.__powerup_type == "radius_down":
            return rangedown_sprite
        elif self.__powerup_type == "strenght_up":
            return strenghtup_sprite
        elif self.__powerup_type == "strenght_down":
            return strenghtdown_sprite
        elif self.__powerup_type == "piercing_up":
            return piercingup_sprite
        elif self.__powerup_type == "piercing_down":
            return piercingdown_sprite
        elif self.__powerup_type == "speed_up":
            return speedup_sprite
        elif self.__powerup_type == "speed_down":
            return speeddown_sprite
        elif self.__powerup_type == "bomb_number_up":
            return bombup_sprite
        elif self.__powerup_type == "bomb_number_down":
            return bombdown_sprite
        elif self.__powerup_type == "shield":
            return shield_sprite
        elif self.__powerup_type == "poison":
            return poison_sprite


class Bomb:
    def __init__(self, pos):
        self.__rect = pygame.Rect(pos, bomb_size)
        self.__pos = pos
        self.__timer = 0
        self.__timer_explosion = -1
        self.__explosion_trail = []
        self.__out = False

    def rect(self):
        return self.__rect

    def get_pos(self):
        return self.__pos
    
    def test_if_out(self,player_obj):
        if not self.__out:
            self.__out = not(player_obj.colliderect(self.__rect))
    
    def got_out(self):
        return self.__out

    def timer(self):
        return self.__timer

    def timer_increment(self):
        self.__timer += dt

    def explosion_timer_start(self):
        self.__timer_explosion = 0
        self.__timer = -1

    def explosion_timer(self):
        return self.__timer_explosion

    def explosion_timer_increment(self):
        self.__timer_explosion += dt

    def explosion(self, bricks_list, radius, piercing, strenght):
        self.__explosion_trail.append(
            pygame.Rect(self.__rect.centerx - explosion_size[0] // 2, self.__rect.centery - explosion_size[1] // 2,
                        explosion_size[0], explosion_size[1]))
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


"""
animations[0] = Regard de face
animations[1] = Marche devant 1
animations[2] = Marche devant 2
animations[3] = Marche droite 1
animations[4] = Marche droite 2
animations[5] = Marche gauche 1
animations[6] = Marche gauche 2
animations[7] = Marche derrière 1
animations[8] = Marche derrière 2
"""


class Perso:
    def __init__(self, classe, pos):
        self.__class = classe
        if classe == 'krieger':
            self.__animations = [krieger_sprite]*9
        elif classe == 'huvud':
            self.__animations = [huvud_idle_sprite, huvud_walkfront1_sprite, huvud_walkfront2_sprite,
                                 huvud_walkright1_sprite, huvud_walkright2_sprite, huvud_walkleft1_sprite, huvud_walkleft2_sprite,
                                 huvud_walkback1_sprite, huvud_walkback2_sprite]
        elif classe == 'bosui':
            self.__animations = [bosui_sprite]*9
        elif classe == 'sowa':
            self.__animations = [sowa_sprite]*9
        
        self.__rect = pygame.Rect(pos, player_size)
        self.__effect = None
        self.__timer_effect = -1
        self.__timer_capa = -1
        self.__sprite = self.__animations[0]
        self.__current_anim = 0

    def give_effect(self, effect):
        self.__effect = effect
        self.__timer_effect = 0

    def reset_effect(self):
        self.__effect = None
        self.__timer_effect = -1

    def timer_effect_increment(self):
        self.__timer_effect += dt

    def get_timer_effect(self):
        return self.__timer_effect

    def get_effect(self):
        return self.__effect

    def rect(self):
        return self.__rect

    def current_anim(self):
        return self.__current_anim

    def sprite(self):
        return self.__sprite

    def set_sprite(self, sprite):
        self.__sprite = self.__animations[sprite + self.__current_anim]

    def next_anim(self, nb_frame):
        if nb_frame == 0:
            self.__current_anim = (self.__current_anim + 1) % 2


class Ennemy:
    def __init__(self, pos, speed, classe):
        self.__classe = classe
        self.__rect = pygame.Rect(pos, ennemy_size)
        self.__velocity = 1
        self.__speed = 100
        self.__x = pos[0]
        self.__y = pos[1]
        self.__target = relative_pos(ennemy_size, self.__rect ,1)
        self.__target_x = pos[0]
        self.__target_y = pos[1]
        self.__path = []
    
    def rect(self):
        return self.__rect
    
    def get_path(self):
        return self.__path
    
    def update(self):
        if self.__path != [] or (self.__target_x, self.__target_y) != (self.__x,self.__y):
            if pygame.Rect(self.__rect.topleft, (1,1)).collidepoint((self.__target_x,self.__target_y)) :
                self.__target = self.__path.pop(0)
                self.__target_x, self.__target_y = relative_pos(ennemy_size, ennemy, 0, (self.__target[0], self.__target[1]))
            
            if self.__y < self.__target_y:
                self.__y += self.__velocity * self.__speed * dt
                if self.__y > self.__target_y:
                    self.__y = self.__target_y
            elif self.__y > self.__target_y:
                self.__y -= self.__velocity * self.__speed * dt
                if self.__y < self.__target_y:
                    self.__y = self.__target_y
            if self.__x < self.__target_x:
                self.__x += self.__velocity * self.__speed * dt
                if self.__x > self.__target_x:
                    self.__x = self.__target_x
            elif self.__x > self.__target_x:
                self.__x -= self.__velocity * self.__speed * dt
                if self.__x < self.__target_x:
                    self.__x = self.__target_x
                    
            self.__rect.update((self.__x, self.__y), ennemy_size)
        else :
            self.__target_x, self.__target_y = self.__x,self.__y
    
    def get_target(self):
        return pygame.Rect(self.__target_x, self.__target_y, 50, 50)
    
    def target_reached(self):
        return pygame.Rect(self.__rect.topleft, (1,1)).collidepoint((self.__target_x,self.__target_y))
    
    def set_path(self, player, bricks_grid):
        player_grid_x, player_grid_y = relative_pos(player_size, player ,1)
        ennemy_grid_x,ennemy_grid_y = relative_pos(ennemy_size, self.__rect ,1)
        self.__path = a_star_pathfinding((int(ennemy_grid_x),int(ennemy_grid_y)), (int(player_grid_x),int(player_grid_y)), bricks_grid)
        if self.__path != []:
            self.__target = self.__path.pop(0)
            self.__target_x, self.__target_y = relative_pos(ennemy_size, None, 0, (self.__target[0], self.__target[1]))
            
# Functions

def relative_pos(relative_rect_size, rect , use = 0, grid_pos = None):
    # Calcule la position de la bombe en fonction de la position du joueur et de la grille
    if grid_pos == None:
        rect_center = pygame.Vector2(rect.center)
        rect_relative_pos = rect_center - pygame.Vector2(game_window.topleft)
        grid_square_size = pygame.Vector2(brick_size[0] + 2, brick_size[1] + 2)
        rect_relative_grid_pos = rect_relative_pos.elementwise() // grid_square_size
    else:
        grid_square_size = pygame.Vector2(brick_size[0] + 2, brick_size[1] + 2)
        rect_relative_grid_pos = pygame.Vector2(grid_pos[0],grid_pos[1])
    grid_square_top_left = rect_relative_grid_pos.elementwise() * grid_square_size + pygame.Vector2(margin, margin)
    relative_rect_position = grid_square_top_left + pygame.Vector2(game_window.topleft) + pygame.Vector2(((brick_size[0] - relative_rect_size[0] + 2) / 2, (brick_size[1] - relative_rect_size[1] + 2) / 2))
    if use == 0:
        return relative_rect_position
    else:
        return rect_relative_grid_pos.x , rect_relative_grid_pos.y


def powerup_appear():
    rand = random.random()
    power_up = None
    if rand < 0.15:
        rand_power_up = random.random()
        if rand_power_up < 0.075:
            power_up = random.choice(["strenght_down", "piercing_down", "radius_down", "speed_down", "poison", "bomb_number_down"])
        elif rand_power_up < 0.1:
            power_up = random.choice(["bomb_number_up", "piercing_up"])
        elif rand_power_up < 0.3:
            power_up = random.choice(["strenght_up", "radius_up", "shield"])
        elif rand_power_up < 0.5:
            power_up = "speed_up"
        else:
            power_up = "coin"
    return power_up


def brick_number(floor_number):
    min_bricks = floor_number + floor_number // 15
    max_bricks = floor_number + floor_number // 10
    min_bricks = max(min(min_bricks, 100), 50)
    max_bricks = min(max(max_bricks, 50), 100)
    return random.randint(min_bricks, max_bricks)


def brick_durability(floor_number):
    rand = random.random()
    p = 1 - (math.exp(-floor_number)) ** 0.025
    d3 = round((p / 100 * (30 + floor_number // 5)), 2)
    d2 = round((p / 100 * (70 - floor_number // 5)), 2)
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
            brick_pos = ((1 + margin + (game_size[0] - margin * 2) / 13 * i + game_window_pos.x),
                         (1 + margin + (game_size[1] - margin * 2) / 13 * j + game_window_pos.y))
            brick = Brick(brick_pos, brick_durability(floor_number))
            if not brick.rect().contains(floor_key) and brick.rect().collidelistall(unbreakables_list) == []:
                bricks_list.append(brick)
    player_temp_rect = pygame.Rect(player_pos, (brick_size[0] * 2, brick_size[1] * 2))
    bricks_list = [brick for brick in bricks_list if not player_temp_rect.colliderect(brick.rect())]
    return random.sample(bricks_list, min(num_bricks, len(bricks_list)))

def gen_ennemy(player, bricks_list, floor_number):
    p = 1 - ((math.exp(-floor_number)) ** 0.025)
    print(p)
    ennemies_list = list()
    bricks_grid = convert_bricks_to_grid(bricks_list)
    available_coords = [[((i*2, j*2) if ((i*2, j*2) not in bricks_grid) else None) for i in range(7)] for j in range(7)]
    available_coords = sum(available_coords, [])
    for _ in range (random.randint(1, max(1, floor_number//10))):
        if available_coords:
            rand = random.random()
            if rand < p:
                ennemy_grid_pos = random.choice(available_coords)
                available_coords.remove(ennemy_grid_pos)
                ennemy_x, ennemy_y = relative_pos(ennemy_size, None, 0, ennemy_grid_pos)
                ennemy = Ennemy((ennemy_x, ennemy_y) , 150 , "Test")
                ennemy.set_path(player,bricks_grid)
                if len(ennemy.get_path()) > 7 or ennemy.get_path() == []:
                    ennemies_list.append(ennemy)
    return ennemies_list

def gen_key():
    key_size = (25, 25)
    key_grid_pos = (random.randint(0, 6) * 2, random.randint(0, 6) * 2)
    key_x = margin / 2 + game_window_pos.x + (key_grid_pos[0] * (game_size[0] - margin) / 13) + ((game_size[0] - margin) / 13 - key_size[0]) / 2
    key_y = margin / 2 + game_window_pos.y + (key_grid_pos[1] * (game_size[1] - margin) / 13) + ((game_size[1] - margin) / 13 - key_size[1]) / 2
    floor_key = pygame.Rect((key_x, key_y), key_size)
    return floor_key

def gen_floor(floor_number, player_pos, player_obj):
    # Génère la structure de l'étage
    floor_key = gen_key()
    while player_obj.rect().colliderect(floor_key):
        floor_key = gen_key()
    bricks_list = gen_bricks(brick_number(floor_number), player_pos, floor_key, floor_number)
    trap = ((random.choice(bricks_list)).rect()).copy()
    ennemies_list = gen_ennemy(player, bricks_list, floor_number)
    return trap, floor_key, bricks_list, ennemies_list

def floor_timer(floor_number):
    floor_time = 180 - floor_number - floor_number // 2
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

def save_score(dictionary, fn="./score.txt", top_n=10):
    with open(fn, "w") as f:
        sorted_scores = sorted(dictionary.items(), key=lambda x: int(x[1][0]), reverse=True)
        for idx, (name, score) in enumerate(sorted_scores[:top_n]):
            f.write(f"{name}: score:{score[0]}, floor:{score[1]}\n")

def load_score(fn="./score.txt"):
    hs = {}
    try:
        with open(fn, "r") as f:
            for line in f:
                name, _, data = line.partition(": score:")
                if name and data:
                    score_str, _, floor_str = data.partition(", floor:")
                    score = int(score_str)
                    floor = int(floor_str)
                    hs[name] = [score, floor]
    except FileNotFoundError:
        return {}
    return hs

def best(dico) :
    best_floor = 0
    for _,floor in dico.values() :
        if floor > best_floor :
            best_floor = floor
    return best_floor

def display_scores(dictionary, player_name=""):
    text_surface = police4.render("Scoreboard", True, (255, 255, 255))
    text_surface_rect = text_surface.get_rect()
    screen.blit(text_surface, (screenx / 2 - text_surface_rect.width // 2, screeny / 5 - text_surface_rect.height // 2))
    text_y = screeny / 5 * 2
    sorted_scores = sorted(dictionary.items(), key=lambda x: int(x[1][0]), reverse=True)
    for idx, (name, score) in enumerate(sorted_scores[:10]):
        score_text = f"{name}: Score: {score[0]}, Floor: {score[1]}"
        if name == player_name:
            text_surface = police.render(score_text, True, (0, 191, 255))
        else:
            text_surface = police.render(score_text, True, (255, 255, 255))
        text_surface_rect = text_surface.get_rect()
        screen.blit(text_surface, (screenx / 2 - text_surface_rect.width // 2, text_y - text_surface_rect.height // 2))
        text_y += 50
    
def convert_bricks_to_grid(bricks_list):
    bricks_grid = [[1 if (j%2 == 1 and i%2 == 1) else 0 for i in range(13)] for j in range(13)]
    for brick in bricks_list:
        relative_gris_pos_x , relative_gris_pos_y  = relative_pos(brick_size, brick.rect(),1)
        bricks_grid[int(relative_gris_pos_x)][int(relative_gris_pos_y)] = 1
    return bricks_grid

def heuristic_cost_estimate(start, goal):
    return math.sqrt((goal[0] - start[0])**2 + (goal[1] - start[1])**2)

def get_neighbors(cell, grid):
    height = len(grid)
    width = len(grid[0])
    i, j = cell
    neighbors = []
    
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_i, new_j = i + di, j + dj
        if 0 <= new_i < height and 0 <= new_j < width and grid[new_i][new_j] != 1:
            neighbors.append((new_i, new_j))
    
    return neighbors

def a_star_pathfinding(start, goal, grid):
    open_list = [start]
    closed_list = []
    came_from = {}
    
    g_score = {(i, j): float('inf') for i in range(len(grid)) for j in range(len(grid[0]))}
    g_score[start] = 0
    
    f_score = {(i, j): float('inf') for i in range(len(grid)) for j in range(len(grid[0]))}
    f_score[start] = heuristic_cost_estimate(start, goal)
    
    while open_list:
        current = min(open_list, key=lambda cell: f_score[cell])
        
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.insert(0, current)
            return path
        
        open_list.remove(current)
        closed_list.append(current)
        
        for neighbor in get_neighbors(current, grid):
            if neighbor in closed_list:
                continue
            
            tentative_g_score = g_score[current] + 1
            
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic_cost_estimate(neighbor, goal)
                
                if neighbor not in open_list:
                    open_list.append(neighbor)
    
    return []
        
# Initializations

pygame.init()

screen = pygame.display.set_mode((1000, 900))
pygame.display.set_caption('Cyberblast 9000')

screenx = 1000
screeny = 900

screen_shade = pygame.Surface((screenx, screeny)).convert_alpha()
screen_shade.fill((0, 0, 0, 100))

current_dir = os.path.dirname(__file__)

score_dict = load_score()
PB = best(score_dict)
sowa_unlocked = False
huvud_unlocked = False
bosui_unlocked = False
if PB >= 20 :
    sowa_unlocked = True
    huvud_unlocked = True
    bosui_unlocked = True
elif PB >= 10 :
    huvud_unlocked = True
    bosui_unlocked = True
elif PB >= 5 :
    bosui_unlocked = True

game_background = pygame.image.load(os.path.join(current_dir, "image/background/game_background.png"))
menu_background = pygame.image.load(os.path.join(current_dir, "image/background/menu_background.png")).convert()
blank_background = pygame.image.load(os.path.join(current_dir, "image/background/blank_background.png")).convert()
krieger_background = pygame.image.load(os.path.join(current_dir, "image/background/krieger_background.png")).convert()
huvud_background = pygame.image.load(os.path.join(current_dir, "image/background/huvud_background.png")).convert()
bosui_background = pygame.image.load(os.path.join(current_dir, "image/background/bosui_background.png")).convert()
sowa_background = pygame.image.load(os.path.join(current_dir, "image/background/sowa_background.png")).convert()
arena_background = pygame.image.load(os.path.join(current_dir, "image/background/arena_background.png")).convert()

key_sprite = pygame.image.load(os.path.join(current_dir, "image/key.png")).convert()
key_sprite.set_colorkey(key_sprite.get_at((0, 0)))
trapdoor_sprite = pygame.image.load(os.path.join(current_dir, "image/trapdoor.png")).convert()

brick_1hit_sprite = pygame.image.load(os.path.join(current_dir, "image/bricks/1hit_brick.png")).convert()
brick_2hit_1_sprite = pygame.image.load(os.path.join(current_dir, "image/bricks/2hit_1_brick.png")).convert()
brick_2hit_2_sprite = pygame.image.load(os.path.join(current_dir, "image/bricks/2hit_2_brick.png")).convert()
brick_3hit_1_sprite = pygame.image.load(os.path.join(current_dir, "image/bricks/3hit_1_brick.png")).convert()
brick_3hit_2_sprite = pygame.image.load(os.path.join(current_dir, "image/bricks/3hit_2_brick.png")).convert()
brick_3hit_3_sprite = pygame.image.load(os.path.join(current_dir, "image/bricks/3hit_3_brick.png")).convert()
indestructible_brick_sprite = pygame.image.load(os.path.join(current_dir, "image/bricks/indestructible_brick.png")).convert()

bomb_sprite = pygame.image.load(os.path.join(current_dir, "image/explosion/bomb_sprite.png")).convert()
bomb_sprite.set_colorkey(bomb_sprite.get_at((0, 0)))
center_explosion_sprite = pygame.image.load(os.path.join(current_dir, "image/explosion/explosion_sprite0.png")).convert()
horizontal_explosion_sprite = pygame.image.load(os.path.join(current_dir, "image/explosion/explosion_sprite2.png")).convert()
vertical_explosion_sprite = pygame.image.load(os.path.join(current_dir, "image/explosion/explosion_sprite1.png")).convert()

coin_sprite = pygame.image.load(os.path.join(current_dir, "image/items/coin_sprite.png")).convert()
coin_sprite.set_colorkey(coin_sprite.get_at((0, 0)))
rangeup_sprite = pygame.image.load(os.path.join(current_dir, "image/items/rangeup_sprite.png")).convert()
strenghtup_sprite = pygame.image.load(os.path.join(current_dir, "image/items/strenghtup_sprite.png")).convert()
speedup_sprite = pygame.image.load(os.path.join(current_dir, "image/items/speedup_sprite.png")).convert()
bombup_sprite = pygame.image.load(os.path.join(current_dir, "image/items/bombup_sprite.png")).convert()
piercingup_sprite = pygame.image.load(os.path.join(current_dir, "image/items/piercingup_sprite.png")).convert()
shield_sprite = pygame.image.load(os.path.join(current_dir, "image/items/shield_sprite.png")).convert()
rangedown_sprite = pygame.image.load(os.path.join(current_dir, "image/items/rangedown_sprite.png")).convert()
strenghtdown_sprite = pygame.image.load(os.path.join(current_dir, "image/items/strenghtdown_sprite.png")).convert()
speeddown_sprite = pygame.image.load(os.path.join(current_dir, "image/items/speeddown_sprite.png")).convert()
bombdown_sprite = pygame.image.load(os.path.join(current_dir, "image/items/bombdown_sprite.png")).convert()
piercingdown_sprite = pygame.image.load(os.path.join(current_dir, "image/items/piercingdown_sprite.png")).convert()
poison_sprite = pygame.image.load(os.path.join(current_dir, "image/items/poison_sprite.png")).convert()

playbouton_sprite = pygame.image.load(os.path.join(current_dir, "image/bouton/play_bouton.png")).convert()
extrabouton_sprite = pygame.image.load(os.path.join(current_dir, "image/bouton/extra_bouton.png")).convert()
quitbouton_sprite = pygame.image.load(os.path.join(current_dir, "image/bouton/quit_bouton.png")).convert()
startbouton_sprite = pygame.image.load(os.path.join(current_dir, "image/bouton/start_bouton.png")).convert()

kriegerbouton_sprite = pygame.image.load(os.path.join(current_dir, "image/bouton/krieger_bouton.png")).convert()
if sowa_unlocked :
    sowabouton_sprite = pygame.image.load(os.path.join(current_dir, "image/bouton/sowa_bouton.png")).convert()
else :
    sowabouton_sprite =  pygame.image.load(os.path.join(current_dir, "image/bouton/lockedsowa_bouton.png")).convert()
if bosui_unlocked :
    bosuibouton_sprite = pygame.image.load(os.path.join(current_dir, "image/bouton/bosui_bouton.png")).convert()
else :
    bosuibouton_sprite = pygame.image.load(os.path.join(current_dir, "image/bouton/lockedbosui_bouton.png")).convert()
if huvud_unlocked :
    huvudbouton_sprite = pygame.image.load(os.path.join(current_dir, "image/bouton/huvud_bouton.png")).convert()
else :
    huvudbouton_sprite = pygame.image.load(os.path.join(current_dir, "image/bouton/lockedhuvud_bouton.png")).convert()

select_sprite = pygame.image.load(os.path.join(current_dir, "image/bouton/select_bouton.png")).convert_alpha()

huvud_idle_sprite = pygame.image.load(os.path.join(current_dir, "image/huvud/idle_front.png")).convert()
huvud_idle_sprite.set_colorkey(huvud_idle_sprite.get_at((0, 0)))
huvud_walkfront1_sprite = pygame.image.load(os.path.join(current_dir, "image/huvud/walk_front1.png")).convert()
huvud_walkfront1_sprite.set_colorkey(huvud_walkfront1_sprite.get_at((0, 0)))
huvud_walkfront2_sprite = pygame.image.load(os.path.join(current_dir, "image/huvud/walk_front2.png")).convert()
huvud_walkfront2_sprite.set_colorkey(huvud_walkfront2_sprite.get_at((0, 0)))
huvud_walkleft1_sprite = pygame.image.load(os.path.join(current_dir, "image/huvud/walk_left1.png")).convert()
huvud_walkleft1_sprite.set_colorkey(huvud_walkleft1_sprite.get_at((0, 0)))
huvud_walkleft2_sprite = pygame.image.load(os.path.join(current_dir, "image/huvud/walk_left2.png")).convert()
huvud_walkleft2_sprite.set_colorkey(huvud_walkleft2_sprite.get_at((0, 0)))
huvud_walkright1_sprite = pygame.image.load(os.path.join(current_dir, "image/huvud/walk_right1.png")).convert()
huvud_walkright1_sprite.set_colorkey(huvud_walkright1_sprite.get_at((0, 0)))
huvud_walkright2_sprite = pygame.image.load(os.path.join(current_dir, "image/huvud/walk_right2.png")).convert()
huvud_walkright2_sprite.set_colorkey(huvud_walkright2_sprite.get_at((0, 0)))
huvud_walkback1_sprite = pygame.image.load(os.path.join(current_dir, "image/huvud/walk_back1.png")).convert()
huvud_walkback1_sprite.set_colorkey(huvud_walkback1_sprite.get_at((0, 0)))
huvud_walkback2_sprite = pygame.image.load(os.path.join(current_dir, "image/huvud/walk_back2.png")).convert()
huvud_walkback2_sprite.set_colorkey(huvud_walkback2_sprite.get_at((0, 0)))

krieger_sprite = pygame.image.load(os.path.join(current_dir, "image/krieger/krieger.png")).convert()
sowa_sprite = pygame.image.load(os.path.join(current_dir, "image/sowa/sowa.png")).convert()
bosui_sprite = pygame.image.load(os.path.join(current_dir, "image/bosui/bosui.png")).convert()

button_size = (500, 100)
play_button = pygame.Rect((screenx / 2 - button_size[0] / 2, 2.5 * screeny / 5 - button_size[1] / 2), button_size)
info_button = pygame.Rect((screenx / 2 - button_size[0] / 2, 3.25 * screeny / 5 - button_size[1] / 2), button_size)
exit_button = pygame.Rect((screenx / 2 - button_size[0] / 2, 4 * screeny / 5 - button_size[1] / 2), button_size)


character_button_size = (200, 150)
character_button_size_buffed = (230, 150) 
krieger_button = pygame.Rect((75,50), character_button_size_buffed)
bosui_button = pygame.Rect((290,50), character_button_size_buffed)
huvud_button = pygame.Rect((510,50), character_button_size_buffed)
sowa_button = pygame.Rect((725,50), character_button_size)
start_button = pygame.Rect((screenx / 2 - button_size[0] / 2,750), button_size)

l_bomb_sfx = [pygame.mixer.Sound("music/bullet_shot1.wav"),pygame.mixer.Sound("music/bullet_shot2.wav"),pygame.mixer.Sound("music/bullet_shot3.wav")]
for sfx in l_bomb_sfx :
    pygame.mixer.Sound.set_volume(sfx,0.5)
bomb_sfx = random.choice(l_bomb_sfx)
die_sfx = pygame.mixer.Sound("music/death_burst_large_2.wav")
pygame.mixer.Sound.set_volume(die_sfx,0.5)
item_pickup_sfx = pygame.mixer.Sound("music/pickup_dime_01.wav")
pygame.mixer.Sound.set_volume(item_pickup_sfx,0.6)
coin_pickup_sfx = pygame.mixer.Sound("music/pickup_penny_02.wav")
pygame.mixer.Sound.set_volume(coin_pickup_sfx,0.6)
bg_music = pygame.mixer.music.load('music/soundtrack.mp3')
pygame.mixer.music.play(-1)


game_size = (750, 750)
game_window_pos = pygame.Vector2((screenx - game_size[0]) / 2, (screeny - game_size[1]) / 1.5)
game_window = pygame.Rect(game_window_pos, game_size)
margin = 9 / 2

player_starting_pos = pygame.Vector2(game_window_pos)
player_size = (50, 50)
classe = 'krieger'
player_obj = Perso(classe, player_starting_pos)
player = player_obj.rect()

direction = {pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0), pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1)}

ennemy_size = (50, 50)
explosion_size = (57, 57)
bomb_size = (25, 25)
key_size = (25, 25)
powerup_size = (21, 21)
key_picked_up = False

brick_size = (55, 55)
unbreakables_pos_list = [[((1 + margin + (game_size[0] - margin * 2) / 13 * i + game_window_pos.x), (1 + margin + (game_size[1] - margin * 2) / 13 * j + game_window_pos.y)) for i in range(1, 13, 2)] for j in range(1, 13, 2)]
unbreakables_pos_list = sum(unbreakables_pos_list, [])

unbreakables_list = [pygame.Rect(pos, brick_size) for pos in unbreakables_pos_list]

FPS = 60
clock = pygame.time.Clock()
clock.tick(FPS)

pygame.time.set_timer(pygame.USEREVENT, 1000)

grid_width = 13

police = pygame.font.Font('PressStart2P.ttf', 16)
police2 = pygame.font.Font('PressStart2P.ttf', 35)
police3 = pygame.font.Font('PressStart2P.ttf', 45)
police4 = pygame.font.Font('PressStart2P.ttf', 70)

key_pressed_state = {}
score_dict = load_score()

dt = 0

# Boucle principale

playing = True
in_game = False
in_menu = 1
end_menu = -1

while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_score(score_dict)
            pygame.quit()
            sys.exit()
    if not in_game:
        if in_menu == 1:
            click = pygame.mouse.get_pressed()
            if click[0]:
                if play_button.collidepoint(pygame.mouse.get_pos()):
                    in_game = True
                    game_over = False
                    character_selected = False
                    score_number = 500
                    floor_number = 20
                    timer_counter = floor_timer(floor_number)
                    key_pressed_state = {}
                    powerup_on_grid = []
                    bomb_on_grid = []
                    bomb_max_number = 1
                    explosion_on_grid = []
                    trap, floor_key, bricks_list, ennemies_list = gen_floor(floor_number, player_starting_pos, player_obj)
                    bricks_grid = convert_bricks_to_grid(bricks_list)
                    player.topleft = player_starting_pos
                    player_speed, speed_malus = 200, 200
                    radius, piercing, strenght = 2, 1, 1
                    nb_frame = 0

                elif info_button.collidepoint(pygame.mouse.get_pos()):
                    in_menu += 1
                    pygame.time.wait(200)

                elif exit_button.collidepoint(pygame.mouse.get_pos()):
                    save_score(score_dict)
                    playing = False
                    pygame.time.wait(200)

            screen.blit(menu_background, (0, 0))
            screen.blit(playbouton_sprite, play_button)
            screen.blit(extrabouton_sprite, info_button)
            screen.blit(quitbouton_sprite, exit_button)
            pygame.display.update()
        elif in_menu == 2:
            click = pygame.mouse.get_pressed()
            if click[0]:
                in_menu -= 1
                pygame.time.wait(200)
            screen.blit(menu_background, (0, 0))
            pygame.display.update()
    else:
        character_background = blank_background
        selected_buton = None
        while not character_selected:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_score(score_dict)
                    pygame.quit()
                    sys.exit()
            click = pygame.mouse.get_pressed()
            if click[0]:
                if krieger_button.collidepoint(pygame.mouse.get_pos()):
                    character_background = krieger_background
                    classe = 'krieger'
                    selected_buton = krieger_button
                elif huvud_button.collidepoint(pygame.mouse.get_pos()) and huvud_unlocked :
                    character_background = huvud_background
                    classe = 'huvud'
                    selected_buton = huvud_button
                elif sowa_button.collidepoint(pygame.mouse.get_pos()) and sowa_unlocked :
                    character_background = sowa_background
                    classe = 'sowa'
                    selected_buton = sowa_button
                elif bosui_button.collidepoint(pygame.mouse.get_pos()) and bosui_unlocked :
                    character_background = bosui_background
                    selected_buton = bosui_button
                    classe = 'bosui'
                elif start_button.collidepoint(pygame.mouse.get_pos()) and selected_buton :
                    character_selected = True
            screen.blit(character_background, (0, 0))            
            screen.blit(kriegerbouton_sprite, krieger_button)
            screen.blit(huvudbouton_sprite, huvud_button)
            screen.blit(sowabouton_sprite, sowa_button)
            screen.blit(bosuibouton_sprite, bosui_button)
            screen.blit(startbouton_sprite, start_button)
            if selected_buton != None :
                screen.blit(select_sprite, selected_buton)
            pygame.display.update()
            clock.tick(FPS)
        player_obj = Perso(classe, player_starting_pos)
        player = player_obj.rect()
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    if timer_counter > 0:
                        timer_counter -= 1
                    else:
                        game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and len(bomb_on_grid) < bomb_max_number and relative_pos(bomb_size,player) not in [bomb.get_pos() for bomb in bomb_on_grid]:
                        bomb_on_grid.append(Bomb(relative_pos(bomb_size, player)))
                    elif event.key in direction:
                        key_pressed_state[event.key] = True
                elif event.type == pygame.KEYUP:
                    key_pressed_state[event.key] = False
                elif event.type == pygame.QUIT:
                    save_score(score_dict)
                    pygame.quit()
                    sys.exit()

            player_velocity = pygame.Vector2(0, 0)
            current_direction = []
            for key, state in key_pressed_state.items():
                if state and key in direction:
                    current_direction.append(key)
                    if key in [pygame.K_LEFT, pygame.K_RIGHT]:
                        player_velocity.x += direction[key][0] * min(speed_malus, player_speed) * dt
                    elif key in [pygame.K_UP, pygame.K_DOWN]:
                        player_velocity.y += direction[key][1] * min(speed_malus, player_speed) * dt

            nb_frame = (nb_frame + 1) % 12
            player_obj.next_anim(nb_frame)
            if pygame.K_DOWN in current_direction and not pygame.K_UP in current_direction:
                player_obj.set_sprite(1)
            elif pygame.K_UP in current_direction and not pygame.K_DOWN in current_direction:
                player_obj.set_sprite(7)
            elif pygame.K_RIGHT in current_direction and not pygame.K_LEFT in current_direction:
                player_obj.set_sprite(3)
            elif pygame.K_LEFT in current_direction and not pygame.K_RIGHT in current_direction:
                player_obj.set_sprite(5)

            temp_player = player.move(player_velocity.x, 0)
            [bomb.test_if_out(temp_player) for bomb in bomb_on_grid]
            if game_window.contains(temp_player) and temp_player.collidelistall(unbreakables_list + [brick.rect() for brick in bricks_list]) == [] and (any([not(temp_player.colliderect(bomb.rect()) and bomb.got_out()) for bomb in bomb_on_grid]) if bomb_on_grid != [] else True):
                player.x = temp_player.x

            temp_player = player.move(0, player_velocity.y)
            [bomb.test_if_out(temp_player) for bomb in bomb_on_grid]
            if game_window.contains(temp_player) and temp_player.collidelistall(unbreakables_list + [brick.rect() for brick in bricks_list]) == [] and (any([not(temp_player.colliderect(bomb.rect()) and bomb.got_out()) for bomb in bomb_on_grid]) if bomb_on_grid != [] else True):
                player.y = temp_player.y
            
            bricks_grid = convert_bricks_to_grid(bricks_list)
            for ennemy in ennemies_list:
                if ennemy.target_reached():
                    ennemy.set_path(player,bricks_grid)
                ennemy.update()
                
            for bomb in bomb_on_grid:
                if bomb.timer() >= 0:
                    bomb.timer_increment()
                if bomb.timer() >= 2:
                    bomb_sfx = random.choice(l_bomb_sfx)
                    bomb_sfx.play()
                    if player_obj.get_effect() == "poison":
                        bomb.explosion(bricks_list, 2, 1, 1)
                    else:
                        bomb.explosion(bricks_list, radius, piercing, strenght)
                    bomb.explosion_timer_start()
                if bomb.explosion_timer() >= 0:
                    bomb.explosion_timer_increment()
                if bomb.explosion_timer() >= 0.5:
                    for brick in bricks_list:
                        if brick.is_destroyed():
                            powerup = powerup_appear()
                            if powerup != None:
                                powerup_on_grid.append(Powerup(relative_pos(powerup_size, brick.rect()), powerup))
                            bricks_list.remove(brick)
                    bomb_on_grid.remove(bomb)

            for powerup in powerup_on_grid:
                if powerup.timer() >= 0:
                    powerup.timer_increment()
                if powerup.timer() >= 5:
                    powerup_on_grid.remove(powerup)

            if player_obj.get_timer_effect() >= 0:
                player_obj.timer_effect_increment()
                if player_obj.get_effect() == "poison":
                    speed_malus = 150
            if player_obj.get_timer_effect() >= 5:
                player_obj.reset_effect()
            if player_obj.get_timer_effect() == -1:
                speed_malus = player_speed
            
            if player.colliderect(floor_key):
                floor_key.update(0, 0, 0, 0)
                key_picked_up = True
                score_number += 10
            if player.colliderect(trap) and key_picked_up:
                floor_number += 1
                score_number += 1000
                trap, floor_key, bricks_list, ennemies_list = gen_floor(floor_number, player.topleft, player_obj)
                key_picked_up = False
                timer_counter = floor_timer(floor_number)
                for bomb in bomb_on_grid:
                    bomb_on_grid.remove(bomb)
                for powerup in powerup_on_grid :
                    powerup_on_grid.remove(powerup)  
            if player_obj.get_effect() != "shield":
                for bomb in bomb_on_grid:
                    if player.collidelistall(bomb.get_explosion_trail()):
                        game_over = True
                for ennemy in ennemies_list :
                    if player.collidelistall([ennemy.rect()]) :
                        game_over = True
            for powerup in powerup_on_grid:
                if player.colliderect(powerup.rect()):
                    if powerup.is_effect():
                        player_obj.give_effect(powerup.get_powerup_type())
                        score_number = powerup.use_effect(score_number)
                    else:
                        score_number, radius, strenght, piercing, player_speed, bomb_max_number = powerup.use(score_number, radius, strenght, piercing, player_speed, bomb_max_number)
                    powerup_on_grid.remove(powerup)
            
            score = police.render(str(score_number), True, (255, 255, 255))
            score_rect = score.get_rect()
            score_center_point = (screenx // 2, 69 // 2)
            score_pos = (score_center_point[0] - score_rect.width // 2, score_center_point[1] - score_rect.height // 2)

            timer = police.render(timer_str(timer_counter), True, (255, 255, 255))
            timer_rect = timer.get_rect()
            timer_center_point = (92.5, 69 // 2)
            timer_pos = (timer_center_point[0] - timer_rect.width // 2, timer_center_point[1] - timer_rect.height // 2)

            floor = police.render(f"Floor:{floor_number}", True, (255, 255, 255))
            floor_rect = floor.get_rect()
            floor_center_point = (screenx - 145, 69 // 2)
            floor_pos = (floor_center_point[0] + 45 - floor_rect.width // 2, floor_center_point[1] - floor_rect.height // 2)

            game_background.blit(arena_background, game_window_pos)
            for unbreakables_bricks in unbreakables_list:
                game_background.blit(indestructible_brick_sprite, unbreakables_bricks)
            for brick in bricks_list:
                if brick.types() == 1:
                    game_background.blit(brick_1hit_sprite, brick.rect())
                elif brick.types() == 2:
                    if brick.durability() == 1:
                        game_background.blit(brick_2hit_1_sprite, brick.rect())
                    elif brick.durability() == 2:
                        game_background.blit(brick_2hit_2_sprite, brick.rect())
                elif brick.types() == 3:
                    if brick.durability() == 1:
                        game_background.blit(brick_3hit_1_sprite, brick.rect())
                    elif brick.durability() == 2:
                        game_background.blit(brick_3hit_2_sprite, brick.rect())
                    elif brick.durability() == 3:
                        game_background.blit(brick_3hit_3_sprite, brick.rect())
            if not trap.collidelistall(bricks_list):
                game_background.blit(trapdoor_sprite, trap)
            if not key_picked_up:
                game_background.blit(key_sprite, floor_key)
            for powerup in powerup_on_grid:
                game_background.blit(powerup.sprite(), powerup.rect())
            if player_obj.get_effect() == "poison":
                pygame.draw.rect(game_background, "purple", player)
            elif player_obj.get_effect() == "shield":
                pygame.draw.rect(game_background, "blue", player)
            else:
                game_background.blit(player_obj.sprite(), player)
            for bomb in bomb_on_grid:
                game_background.blit(bomb_sprite, bomb.rect())
                for explosion in bomb.get_explosion_trail():
                    diff = (explosion_size[0] - bomb_size[0]) // 2
                    if game_window.contains(explosion):
                        if bomb.rect()[0] == explosion[0] + diff:
                            if bomb.rect()[1] == explosion[1] + diff:
                                game_background.blit(center_explosion_sprite, explosion)
                            else:
                                game_background.blit(vertical_explosion_sprite, explosion)
                        else:
                            game_background.blit(horizontal_explosion_sprite, explosion)
            for ennemy in ennemies_list:
                pygame.draw.rect(game_background, "red", ennemy.rect())
            screen.blit(game_background, (0, 0))
            screen.blit(score, score_pos)
            screen.blit(timer, timer_pos)
            screen.blit(floor, floor_pos)
            pygame.display.update()
            dt = clock.tick(FPS) / 1000

        end_menu += 1
        if end_menu == 0:
            bomb_sfx.stop()
            die_sfx.play()
            game_over_text = police4.render("GAME OVER !", True, "#DEFF00")
            game_over_text_rect = game_over_text.get_rect()
            screen.blit(screen_shade, (0, 0))
            screen.blit(game_over_text,(screenx / 2 - game_over_text_rect.width // 2, screeny / 2 - game_over_text_rect.height // 2))
            pygame.display.update()
            pygame.time.wait(2000)
        elif end_menu == 1:
            player_name = ""
            user_text = ""
            while player_name == "":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            player_name = user_text
                        elif event.key == pygame.K_BACKSPACE:
                            user_text = user_text[:-1]
                        else:
                            if len(user_text) < 15:
                                user_text += event.unicode

                game_background.blit(arena_background, game_window_pos)
                for unbreakables_bricks in unbreakables_list:
                    game_background.blit(indestructible_brick_sprite, unbreakables_bricks)
                for brick in bricks_list:
                    if brick.types() == 1:
                        game_background.blit(brick_1hit_sprite, brick.rect())
                    elif brick.types() == 2:
                        if brick.durability() == 1:
                            game_background.blit(brick_2hit_1_sprite, brick.rect())
                        elif brick.durability() == 2:
                            game_background.blit(brick_2hit_2_sprite, brick.rect())
                    elif brick.types() == 3:
                        if brick.durability() == 1:
                            game_background.blit(brick_3hit_1_sprite, brick.rect())
                        elif brick.durability() == 2:
                            game_background.blit(brick_3hit_2_sprite, brick.rect())
                        elif brick.durability() == 3:
                            game_background.blit(brick_3hit_3_sprite, brick.rect())
                if not trap.collidelistall(bricks_list):
                    game_background.blit(trapdoor_sprite, trap)
                if not key_picked_up:
                    game_background.blit(key_sprite, floor_key)
                for powerup in powerup_on_grid:
                    game_background.blit(powerup.sprite(), powerup.rect())
                if player_obj.get_effect() == "poison":
                    pygame.draw.rect(game_background, "purple", player)
                else:
                    game_background.blit(player_obj.sprite(), player)
                for bomb in bomb_on_grid:
                    game_background.blit(bomb_sprite, bomb.rect())
                    for explosion in bomb.get_explosion_trail():
                        diff = (explosion_size[0] - bomb_size[0]) // 2
                        if game_window.contains(explosion):
                            if bomb.rect()[0] == explosion[0] + diff:
                                if bomb.rect()[1] == explosion[1] + diff:
                                    game_background.blit(center_explosion_sprite, explosion)
                                else:
                                    game_background.blit(vertical_explosion_sprite, explosion)
                            else:
                                game_background.blit(horizontal_explosion_sprite, explosion)
                screen.blit(game_background, (0, 0))
                screen.blit(score, score_pos)
                screen.blit(timer, timer_pos)
                screen.blit(floor, floor_pos)

                screen.blit(screen_shade, (0, 0))

                name_text = police3.render("Enter your name:", True, "#DEFF00")
                name_text_rect = name_text.get_rect()
                screen.blit(name_text,
                            (screenx / 2 - name_text_rect.width // 2, screeny / 4 - name_text_rect.height // 2))

                text_surface_center_point = (screenx / 2, screeny / 2)
                text_surface = police2.render(f"Name: {user_text}", True, "#DEFF00")
                text_surface_rect = text_surface.get_rect()
                text_surface_pos = (text_surface_center_point[0] - text_surface_rect.width // 2,
                                    text_surface_center_point[1] - text_surface_rect.height // 2)
                screen.blit(text_surface, text_surface_pos)

                pygame.display.update()

            score_dict[player_name] = [score_number, floor_number]
            save_score(score_dict)
        elif end_menu == 2:
            end_menu = -1
            in_game = False
            screen.blit(blank_background, (0, 0))
            display_scores(score_dict, player_name)
            pygame.display.update()
            pygame.time.wait(3500)

pygame.quit()
sys.exit()