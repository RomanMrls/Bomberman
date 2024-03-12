import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((1000, 900))
pygame.display.set_caption('Bomberman')

screenx = 1000
screeny = 900

scorebar = background = pygame.Surface((screenx, 75))
scorebar.fill((255,0,255))

background = pygame.Surface((screenx, screeny))
background.fill((0,0,0))

game_size = (750,750)
game_window_pos = pygame.Vector2((screenx-game_size[0])/2,(screeny-game_size[1])/1.5)
game_window= pygame.Rect(game_window_pos,game_size)

player_pos = pygame.Vector2(game_window_pos)
player_size = (40,40)
player = pygame.Rect(player_pos,player_size)
direction = {pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0), pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1)}

bomb_timer = -1
bomb = None
bomb_size = (20,20)
def bomb_pos():
    player_center = pygame.Vector2(player.center)
    player_relative_pos = player_center - pygame.Vector2(game_window.topleft)
    player_relative_grid_pos = player_relative_pos.elementwise() // pygame.Vector2(obstacle_size)
    grid_square_center = player_relative_grid_pos.elementwise() * pygame.Vector2(obstacle_size) + pygame.Vector2(obstacle_size) / 2
    bomb_relative_pos = grid_square_center + pygame.Vector2(game_window.topleft) - pygame.Vector2(bomb_size) / 2
    return bomb_relative_pos

obstacle_pos_list = [[(game_size[0]/13*i+game_window_pos.x,game_size[1]/13*j+game_window_pos.y) for i in range(1,13,2)] for j in range(1,13,2)]
obstacle_size = (game_size[0]/13,game_size[1]/13)
obstacle_list = [[pygame.Rect(pos,obstacle_size) for pos in ligne] for ligne in obstacle_pos_list]
obstacle_list = sum(obstacle_list, [])

clock = pygame.time.Clock()

police = pygame.font.SysFont('chalkduster.ttf', 50)

game_over = False

pygame.time.set_timer(pygame.USEREVENT, 1000)
timer_counter = 300
score_number = 10
floor_number = 1

key_state = {}

dt = 0

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
                key_state[event.key] = True 
        elif event.type == pygame.KEYUP:
            key_state[event.key] = False
    
    player_speed = 200
    player_velocity = pygame.Vector2(0, 0)
    for key, state in key_state.items():
        if state and key in direction:
            player_velocity += pygame.Vector2(direction[key]) * player_speed * dt

    temp_player = player.move(player_velocity.x, player_velocity.y)
    if game_window.contains(temp_player) and temp_player.collidelistall(obstacle_list) == list():
        player = temp_player
    
    if bomb_timer >= 0:
        bomb_timer += dt
    
    if bomb_timer >= 3:
        bomb = None
        bomb_timer = -1
        
    score = police.render((str(score_number)), True, (255, 255, 255))
    score_center = pygame.Vector2(score.get_rect().center)
       
    timer = police.render((str(timer_counter)), True, (255, 255, 255))
    timer_center = pygame.Vector2(timer.get_rect().center)
    
    floor = police.render((f"Floor : {floor_number}"), True, (255, 255, 255))
    floor_center = pygame.Vector2(floor.get_rect().center)

    screen.blit(background, (0, 0))
    screen.blit(scorebar, (0, 0))
    screen.blit(score, (screenx/2-score_center.x, 75/2-score_center.y))
    screen.blit(timer, (25, 75/2-timer_center.y))
    screen.blit(floor, (screenx-25-floor_center.x*2 , 75/2-floor_center.y))
    pygame.draw.rect(background, "blue", game_window)
    for rect in obstacle_list:
        pygame.draw.rect(background, "red", rect)
    pygame.draw.rect(background, "green", player)
    
    if bomb:
        pygame.draw.rect(background, "yellow", bomb)
    
    pygame.display.update()
    
    dt = clock.tick(60) / 1000
    
pygame.quit()
sys.exit()