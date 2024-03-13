import pygame
import sys
import math
import random
from random import randint

# Initialisation de Pygame
pygame.init()

# Création de la fenêtre de jeu
screen = pygame.display.set_mode((1000, 900))
pygame.display.set_caption('Cyberblast 9000')

# Définition des dimensions de l'écran
screenx = 1000
screeny = 900

# Surface pour l'arrière-plan du jeu
background = pygame.image.load("background.png")

# Taille et position de la fenêtre de jeu dans l'écran
game_size = (750, 750)
game_window_pos = pygame.Vector2((screenx - game_size[0]) / 2, (screeny - game_size[1]) / 1.5)
game_window = pygame.Rect(game_window_pos, game_size)

# Position initiale et taille du joueur
player_pos = pygame.Vector2(game_window_pos)
player_size = (40, 40)
player = pygame.Rect(player_pos, player_size)

# Directions de mouvement du joueur
direction = {pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0), pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1)}

# Initialisation des variables pour la bombe
bomb_timer = -1
bomb = None
bomb_size = (25, 25)

# Fonction pour obtenir la position de la bombe en fonction de la position du joueur et de la grille
def bomb_pos():
    player_center = pygame.Vector2(player.center)
    player_relative_pos = player_center - pygame.Vector2(game_window.topleft)
    player_relative_grid_pos = player_relative_pos.elementwise() // pygame.Vector2(unbreakables_size)
    grid_square_center = player_relative_grid_pos.elementwise() * pygame.Vector2(unbreakables_size) + pygame.Vector2(unbreakables_size) / 2
    bomb_relative_pos = grid_square_center + pygame.Vector2(game_window.topleft) - pygame.Vector2(bomb_size) / 2
    return bomb_relative_pos

# Liste des positions des briques unbreakables et initialisation de la taille des briques unbreakables
unbreakables_size = (game_size[0] / 13, game_size[1] / 13)
unbreakables_pos_list = [[(round(game_size[0] / 13 * i + game_window_pos.x , 5), round(game_size[1] / 13 * j + game_window_pos.y, 5)) for i in range(1, 13, 2)] for j in range(1, 13, 2)]
unbreakables_pos_list = sum(unbreakables_pos_list, [])

# Création des rectangles des unbreakabless
unbreakables_list = [pygame.Rect(pos, unbreakables_size) for pos in unbreakables_pos_list]
# Aplatir la liste d'unbreakabless en une seule liste


# Initialisation de l'horloge pour la gestion du temps
clock = pygame.time.Clock()

# Police de caractères pour le texte
police = pygame.font.SysFont('chalkduster.ttf', 40)

# Initialisation des variables de jeu
game_over = False
pygame.time.set_timer(pygame.USEREVENT, 1000)  # Déclencher un événement toutes les secondes
timer_counter = 300  # Compteur de temps initial
score_number = 10  # Score initial
floor_number = 1  # Numéro de l'étage initial

# Dictionnaire pour stocker l'état des touches du clavier
key_pressed_state = {}

# Initialisation de la variable de temps écoulé (delta time)
dt = 0

# Fonction pour convertir le compteur de temps en une chaîne de caractères au format "mm:ss"
def timer_str(timer_counter):
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

# Classe Brick pour représenter les blocs cassables
class Brick:
    def __init__(self, pos, durability):
        self.__rect = pygame.Rect(pos, (game_size[0] / 13, game_size[1] / 13))
        self.__durability = durability
    
    def rect(self):
        return self.__rect

    def boom(self):
        self.__durability -= 1

    def is_destroyed(self):
        return self.__durability <= 0
    
# Fonction pour générer les briques
def gen_bricks(num_bricks, player_pos, floor_key):
    brick_size = (55, 55)
    bricks_list = []

    for i in range(0, 13):
        for j in range(0, 13):
            brick_pos = (round(game_size[0] / 13 * i + game_window_pos.x, 5), round(game_size[1] / 13 * j + game_window_pos.y, 5))
            brick_rect = pygame.Rect(brick_pos, brick_size)
            if not brick_rect.contains(floor_key) and brick_rect.collidelistall(unbreakables_list) == []:
                bricks_list.append(brick_rect)
    
    player_temp_rect = pygame.Rect(player_pos, (brick_size[0]*2, brick_size[1]*2))
    bricks_list = [brick_rect for brick_rect in bricks_list if not player_temp_rect.colliderect(brick_rect)]

    return random.sample(bricks_list, min(num_bricks, len(bricks_list)))

# Fonction pour générer la structure de l'étage
def gen_floor(floor_number,player_pos):
    # Génération de la clé
    key_grid_pos = (randint(0, 6) * 2, randint(0, 6) * 2)
    key_size = (25,25)
    
    key_x = game_window_pos.x + (key_grid_pos[0] * game_size[0] / 13) + (game_size[0] / 13 - key_size[0]) / 2
    key_y = game_window_pos.y + (key_grid_pos[1] * game_size[1] / 13) + (game_size[1] / 13 - key_size[1]) / 2
    
    floor_key = pygame.Rect((key_x, key_y),key_size)
    
    #Génération des blocs
    bricks_list = gen_bricks(100, player_pos, floor_key)

    return floor_key, bricks_list

# Génération du premier étage
floor_key, bricks_list = gen_floor(floor_number,player_pos)

# Boucle principale du jeu
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.USEREVENT:
            if timer_counter > 0:
                timer_counter -= 1
            else:
                game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and bomb is None:
                bomb = pygame.Rect(bomb_pos(), bomb_size)
                bomb_timer = 0
                bomb_placed_time = pygame.time.get_ticks()
            elif event.key in direction:
                key_pressed_state[event.key] = True
        elif event.type == pygame.KEYUP:
            key_pressed_state[event.key] = False

    # Calcul de la vélocité du joueur en fonction des touches enfoncées
    player_speed = 200
    player_velocity = pygame.Vector2(0, 0)
    for key, state in key_pressed_state.items():
        if state and key in direction:
            if key in [pygame.K_LEFT, pygame.K_RIGHT]:
                player_velocity.x += direction[key][0] * player_speed * dt
            elif key in [pygame.K_UP, pygame.K_DOWN]:
                player_velocity.y += direction[key][1] * player_speed * dt

    # Déplacement horizontal du joueur
    temp_player = player.move(player_velocity.x, 0)
    if game_window.contains(temp_player) and temp_player.collidelistall(unbreakables_list) == []:
        player.x = temp_player.x

    # Déplacement vertical du joueur
    temp_player = player.move(0, player_velocity.y)
    if game_window.contains(temp_player) and temp_player.collidelistall(unbreakables_list) == []:
        player.y = temp_player.y

    # Gestion du minuteur de la bombe
    if bomb_timer >= 0:
        bomb_timer += dt

    if bomb_timer >= 3:
        bomb = None
        bomb_timer = -1
    
    # Génération de l'étage si le joueur a pris la clé
    if player.colliderect(floor_key):
        floor_number += 1
        floor_key, bricks_list = gen_floor(floor_number,player.topleft)
        
    # Définir le point central souhaité dans la barre supérieure pour le score et le minuteur
    
    
    
        
    # Rendu du texte de score, du minuteur et du numéro de l'étage
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
    
    # Affichage des éléments du jeu sur l'écran
    screen.blit(background, (0, 0))
    screen.blit(score, score_pos)
    screen.blit(timer, timer_pos)
    screen.blit(floor, floor_pos)
    pygame.draw.rect(background, "blue", game_window)
    for rect in unbreakables_list:
        pygame.draw.rect(background, "purple", rect)
    for brick in bricks_list:
        pygame.draw.rect(background, "white", brick)
    pygame.draw.rect(background, "yellow", floor_key)
    pygame.draw.rect(background, "green", player)

    if bomb:
        pygame.draw.rect(background, "black", bomb)

    pygame.display.update()

    # Calcul du temps écoulé entre deux boucles
    dt = clock.tick(60) / 1000

# Sortie du jeu
pygame.quit()
sys.exit()