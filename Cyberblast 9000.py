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

    def use(self, score_number, radius, strenght, piercing, player_speed, bomb_max_number):
        score_number -= 10
        if not self.__effect:
            if self.__powerup_type == "coin":
                score_number += 15
            elif self.__powerup_type == "radius_up":
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
animations[1] = Regard 3/4 droite
animations[2] = Regard 3/4 gauche
animations[3] = Marche devant 1
animations[4] = Marche devant 2
animations[5] = Marche droite 1
animations[6] = Marche droite 2
animations[7] = Marche gauche 1
animations[8] = Marche gauche 2
animations[9] = Marche derrière 1
animations[10] = Marche derrière 2
"""


class Perso:
    def __init__(self, classe, pos):
        self.__class = classe
        '''
        if classe == 'krieger':
            self.__animations = [krieger_idle_face_sprite, krieger_idle_right_sprite, krieger_idle_left_sprite,
                                 krieger_walkfront1_sprite, krieger_walkfront2_sprite, krieger_walkright1_sprite,
                                 krieger_walkright2_sprite, krieger_walkleft1_sprite, krieger_walkleft2_sprite,
                                 krieger_walkback1_sprite, krieger_walkback2_sprite]
        elif classe == 'huvud':
            self.__animations = [huvud_idle_face_sprite, huvud_idle_right_sprite, huvud_idle_left_sprite, huvud_walkfront1_sprite,
                                 huvud_walkfront2_sprite, huvud_walkright1_sprite, huvud_walkright2_sprite, huvud_walkleft1_sprite,
                                 huvud_walkleft2_sprite, huvud_walkback1_sprite, huvud_walkback2_sprite]
        elif classe == 'bosui':
            self.__animations = [bosui_idle_face_sprite, bosui_idle_right_sprite, bosui_idle_left_sprite,
                                 bosui_walkfront1_sprite, bosui_walkfront2_sprite, bosui_walkright1_sprite,
                                 bosui_walkright2_sprite, bosui_walkleft1_sprite, bosui_walkleft2_sprite,
                                 bosui_walkback1_sprite, bosui_walkback2_sprite]
        elif classe == 'sowa':
            self.__animations = [sowa_idle_face_sprite, sowa_idle_right_sprite, sowa_idle_left_sprite,
                                 sowa_walkfront1_sprite, sowa_walkfront2_sprite, sowa_walkright1_sprite,
                                 sowa_walkright2_sprite, sowa_walkleft1_sprite, sowa_walkleft2_sprite,
                                 sowa_walkback1_sprite, sowa_walkback2_sprite]
        '''
        self.__animations = [huvud_idle_sprite, huvud_idle_sprite, huvud_idle_sprite, huvud_walkfront1_sprite, huvud_walkfront2_sprite,
                             huvud_walkright1_sprite, huvud_walkright2_sprite, huvud_walkleft1_sprite, huvud_walkleft2_sprite,
                             huvud_walkback1_sprite, huvud_walkback2_sprite]
        self.__rect = pygame.Rect(pos, player_size)
        self.__effect = None
        self.__timer_effect = -1
        self.__timer_capa = -1
        self.__sprite = self.__animations[0]
        self.__orientation = 'Front'
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

    def orientation(self):
        return self.__orientation

    def sprite(self):
        return self.__sprite

    def set_sprite(self, sprite):
        self.__sprite = self.__animations[sprite + self.__current_anim]

    def next_anim(self, nb_frame):
        if nb_frame == 0:
            self.__current_anim = (self.__current_anim + 1) % 2

    def set_orientation(self, orientation):
        self.__orientation = orientation

    def idle(self):
        if self.__orientation == 'Right':
            self.__sprite = self.__animations[1]
        elif self.__orientation == 'Left':
            self.__sprite = self.__animations[2]
        else:
            self.__sprite = self.__animations[0]


# Functions

def relative_pos(relative_rect_size, rect):
    # Calcule la position de la bombe en fonction de la position du joueur et de la grille
    rect_center = pygame.Vector2(rect.center)
    rect_relative_pos = rect_center - pygame.Vector2(game_window.topleft)
    grid_square_size = pygame.Vector2(brick_size[0] + 2, brick_size[1] + 2)
    rect_relative_grid_pos = rect_relative_pos.elementwise() // grid_square_size
    grid_square_top_left = rect_relative_grid_pos.elementwise() * grid_square_size + pygame.Vector2(margin, margin)
    relative_rect_position = grid_square_top_left + pygame.Vector2(game_window.topleft) + pygame.Vector2(
        ((brick_size[0] - relative_rect_size[0] + 2) / 2, (brick_size[1] - relative_rect_size[1] + 2) / 2))
    return relative_rect_position


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
    return trap, floor_key, bricks_list


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


# Initializations

pygame.init()

screen = pygame.display.set_mode((1000, 900))
pygame.display.set_caption('Cyberblast 9000')

screenx = 1000
screeny = 900

screen_shade = pygame.Surface((screenx, screeny)).convert_alpha()
screen_shade.fill((0, 0, 0, 100))

current_dir = os.path.dirname(__file__)

game_background = pygame.image.load(os.path.join(current_dir, "image/game_background.png"))
menu_background = pygame.image.load(os.path.join(current_dir, "image/menu_background.png")).convert()
blank_background = pygame.image.load(os.path.join(current_dir, "image/blank_background.png")).convert()
perso_background = pygame.image.load(os.path.join(current_dir, "image/perso_background.png")).convert()
krieger_background = pygame.image.load(os.path.join(current_dir, "image/krieger_background.png")).convert()
huvud_background = pygame.image.load(os.path.join(current_dir, "image/huvud_background.png")).convert()
arena_background = pygame.image.load(os.path.join(current_dir, "image/arena_background.png")).convert()

key_sprite = pygame.image.load(os.path.join(current_dir, "image/key.png")).convert()
key_sprite.set_colorkey(key_sprite.get_at((0, 0)))
trapdoor_sprite = pygame.image.load(os.path.join(current_dir, "image/trapdoor.png")).convert()

brick_1hit_sprite = pygame.image.load(os.path.join(current_dir, "image/1hit_brick.png")).convert()
brick_2hit_1_sprite = pygame.image.load(os.path.join(current_dir, "image/2hit_1_brick.png")).convert()
brick_2hit_2_sprite = pygame.image.load(os.path.join(current_dir, "image/2hit_2_brick.png")).convert()
brick_3hit_1_sprite = pygame.image.load(os.path.join(current_dir, "image/3hit_1_brick.png")).convert()
brick_3hit_2_sprite = pygame.image.load(os.path.join(current_dir, "image/3hit_2_brick.png")).convert()
brick_3hit_3_sprite = pygame.image.load(os.path.join(current_dir, "image/3hit_3_brick.png")).convert()
indestructible_brick_sprite = pygame.image.load(os.path.join(current_dir, "image/indestructible_brick.png")).convert()

bomb_sprite = pygame.image.load(os.path.join(current_dir, "image/bomb_sprite.png")).convert()
bomb_sprite.set_colorkey(bomb_sprite.get_at((0, 0)))
center_explosion_sprite = pygame.image.load(os.path.join(current_dir, "image/explosion_sprite0.png")).convert()
horizontal_explosion_sprite = pygame.image.load(os.path.join(current_dir, "image/explosion_sprite2.png")).convert()
vertical_explosion_sprite = pygame.image.load(os.path.join(current_dir, "image/explosion_sprite1.png")).convert()

coin_sprite = pygame.image.load(os.path.join(current_dir, "image/coin_sprite.png")).convert()
coin_sprite.set_colorkey(coin_sprite.get_at((0, 0)))

rangeup_sprite = pygame.image.load(os.path.join(current_dir, "image/rangeup_sprite.png")).convert()
strenghtup_sprite = pygame.image.load(os.path.join(current_dir, "image/strenghtup_sprite.png")).convert()
speedup_sprite = pygame.image.load(os.path.join(current_dir, "image/speedup_sprite.png")).convert()
bombup_sprite = pygame.image.load(os.path.join(current_dir, "image/bombup_sprite.png")).convert()
piercingup_sprite = pygame.image.load(os.path.join(current_dir, "image/piercingup_sprite.png")).convert()
shield_sprite = pygame.image.load(os.path.join(current_dir, "image/shield_sprite.png")).convert()

rangedown_sprite = pygame.image.load(os.path.join(current_dir, "image/rangedown_sprite.png")).convert()
strenghtdown_sprite = pygame.image.load(os.path.join(current_dir, "image/strenghtdown_sprite.png")).convert()
speeddown_sprite = pygame.image.load(os.path.join(current_dir, "image/speeddown_sprite.png")).convert()
bombdown_sprite = pygame.image.load(os.path.join(current_dir, "image/bombdown_sprite.png")).convert()
piercingdown_sprite = pygame.image.load(os.path.join(current_dir, "image/piercingdown_sprite.png")).convert()
poison_sprite = pygame.image.load(os.path.join(current_dir, "image/poison_sprite.png")).convert()

playbouton_sprite = pygame.image.load(os.path.join(current_dir, "image/play_bouton.png")).convert()
extrabouton_sprite = pygame.image.load(os.path.join(current_dir, "image/extra_bouton.png")).convert()
quitbouton_sprite = pygame.image.load(os.path.join(current_dir, "image/quit_bouton.png")).convert()
kriegerbouton_sprite = pygame.image.load(os.path.join(current_dir, "image/krieger_bouton.png")).convert()
bosuibouton_sprite = pygame.image.load(os.path.join(current_dir, "image/bosui_bouton.png")).convert()
huvudbouton_sprite = pygame.image.load(os.path.join(current_dir, "image/huvud_bouton.png")).convert()

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

button_size = (500, 100)
play_button = pygame.Rect((screenx / 2 - button_size[0] / 2, 2.5 * screeny / 5 - button_size[1] / 2), button_size)
info_button = pygame.Rect((screenx / 2 - button_size[0] / 2, 3.25 * screeny / 5 - button_size[1] / 2), button_size)
exit_button = pygame.Rect((screenx / 2 - button_size[0] / 2, 4 * screeny / 5 - button_size[1] / 2), button_size)


character_button_size = (200, 150)
krieger_button = pygame.Rect((screenx / -8 + character_button_size[0], screeny / 9 + 4 * character_button_size[1]), character_button_size)
bosui_button = pygame.Rect((9*screenx / 100 + character_button_size[0], screeny / 9 + 4 * character_button_size[1]), character_button_size)
huvud_button = pygame.Rect((31*screenx / 100 + character_button_size[0], screeny / 9 + 4 * character_button_size[1]), character_button_size)
sowa_button = pygame.Rect((21*screenx / 40 + character_button_size[0], screeny / 9 + 4 * character_button_size[1]), character_button_size)

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
                    floor_number = 1
                    timer_counter = floor_timer(floor_number)
                    key_pressed_state = {}
                    powerup_on_grid = []
                    bomb_on_grid = []
                    bomb_max_number = 1
                    explosion_on_grid = []
                    trap, floor_key, bricks_list = gen_floor(floor_number, player_starting_pos, player_obj)
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
        while not character_selected:
            character_background = blank_background
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            click = pygame.mouse.get_pressed()
            if click[0]:
                if krieger_button.collidepoint(pygame.mouse.get_pos()):
                    character_selected = True
                    classe = 'krieger'
                elif huvud_button.collidepoint(pygame.mouse.get_pos()):
                    character_selected = True
                    classe = 'huvud'
                elif sowa_button.collidepoint(pygame.mouse.get_pos()):
                    character_selected = True
                    classe = 'sowa'
                elif bosui_button.collidepoint(pygame.mouse.get_pos()):
                    character_selected = True
                    classe = 'bosui'
            if not click[0]:
                if krieger_button.collidepoint(pygame.mouse.get_pos()):
                    character_background = krieger_background
                elif huvud_button.collidepoint(pygame.mouse.get_pos()):
                    character_background = huvud_background
                elif sowa_button.collidepoint(pygame.mouse.get_pos()):
                    character_background = perso_background
                elif bosui_button.collidepoint(pygame.mouse.get_pos()):
                    character_background = perso_background
            screen.blit(character_background, (0, 0))            
            screen.blit(kriegerbouton_sprite, krieger_button)
            screen.blit(huvudbouton_sprite, huvud_button)
            screen.blit(kriegerbouton_sprite, sowa_button)
            screen.blit(bosuibouton_sprite, bosui_button)
            pygame.display.update()
        player_obj = Perso(classe, player_starting_pos)
        player = player_obj.rect()
        while not game_over:
            player_obj.idle()
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
                player_obj.set_sprite(3)
            elif pygame.K_UP in current_direction and not pygame.K_DOWN in current_direction:
                player_obj.set_orientation('Front')
                player_obj.set_sprite(9)
            elif pygame.K_RIGHT in current_direction and not pygame.K_LEFT in current_direction:
                player_obj.set_orientation('Right')
                player_obj.set_sprite(5)
            elif pygame.K_LEFT in current_direction and not pygame.K_RIGHT in current_direction:
                player_obj.set_orientation('Right')
                player_obj.set_sprite(7)

            temp_player = player.move(player_velocity.x, 0)
            if game_window.contains(temp_player) and temp_player.collidelistall(unbreakables_list + [brick.rect() for brick in bricks_list]) == []:
                player.x = temp_player.x

            temp_player = player.move(0, player_velocity.y)
            if game_window.contains(temp_player) and temp_player.collidelistall(unbreakables_list + [brick.rect() for brick in bricks_list]) == []:
                player.y = temp_player.y

            for bomb in bomb_on_grid:
                if bomb.timer() >= 0:
                    bomb.timer_increment()
                if bomb.timer() >= 1.5:
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
                trap, floor_key, bricks_list = gen_floor(floor_number, player.topleft, player_obj)
                key_picked_up = False
                timer_counter = floor_timer(floor_number)
                del_props(powerup_on_grid,bomb_on_grid)
                for powerup in powerup_on_grid :
                    powerup_on_grid.remover(powerup)
                for bomb in bomb_on_grid :
                    bomb_on_grid.remover(bomb)   
            if player_obj.get_effect() != "shield":
                for bomb in bomb_on_grid:
                    if player.collidelistall(bomb.get_explosion_trail()):
                        game_over = True
            for powerup in powerup_on_grid:
                if player.colliderect(powerup.rect()):
                    if powerup.is_effect():
                        player_obj.give_effect(powerup.get_powerup_type())
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
            screen.blit(game_background, (0, 0))
            screen.blit(score, score_pos)
            screen.blit(timer, timer_pos)
            screen.blit(floor, floor_pos)

            pygame.display.update()
            clock.tick(FPS)

        end_menu += 1
        if end_menu == 0:
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
        elif end_menu == 2:
            end_menu = -1
            in_game = False
            screen.blit(blank_background, (0, 0))
            display_scores(score_dict, player_name)
            pygame.display.update()
            pygame.time.wait(4000)

    dt = clock.tick(FPS) / 1000

pygame.quit()
sys.exit()
