import pygame,sys

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
direction = {pygame.K_LEFT: (-4, 0), pygame.K_RIGHT: (4, 0), pygame.K_UP: (0, -4), pygame.K_DOWN: (0, 4)}


bomb_size = (20,20)
def bomb_pos():
    x = player.topleft[0] - player.topleft[0]%obstacle_size[0] + obstacle_size[0]-bomb_size[0]
    y = player.topleft[1] - player.topleft[1]%obstacle_size[1] + obstacle_size[1]-bomb_size[1]
    return pygame.Vector2((x,y))

obstacle_pos_list = [[(56.25*i+game_window_pos.x,56.25*j+game_window_pos.y) for i in range(1,13,2)] for j in range(1,13,2)]
obstacle_size = (56.25,56.25)
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

while not game_over:
    clock.tick(165)
    for event in pygame.event.get():
        print(player)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.USEREVENT:
            if timer_counter > 0:
                timer_counter -= 1
            else:
                game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bomb = pygame.Rect(bomb_size,bomb_pos())
                pygame.draw.rect(background,"black",rect)
            elif event.key in direction:
                key_state[event.key] = True 
        elif event.type == pygame.KEYUP:
            key_state[event.key] = False
            
    for key, state in key_state.items():
        if state and key in direction:
            v = direction[key]
            temp_player = player.copy()
            temp_player.move_ip(v)
            if game_window.contains(temp_player) and temp_player.collidelistall(obstacle_list) == list():
                player.move_ip(v)
        
    score = police.render((f"SCORE = {score_number}"), True, (255, 255, 255))
    score_center = pygame.Vector2(score.get_rect().center)
       
    timer = police.render((str(timer_counter)), True, (255, 255, 255))
    timer_center = pygame.Vector2(timer.get_rect().center)
    
    floor = police.render((f"FLOOR : {floor_number}"), True, (255, 255, 255))
    floor_center = pygame.Vector2(floor.get_rect().center)

    screen.blit(background,(0, 0))
    screen.blit(scorebar,(0, 0))
    screen.blit(score, (screenx/2-score_center.x, 75/2-score_center.y))
    screen.blit(timer, (25, 75/2-timer_center.y))
    screen.blit(floor, (screenx-25-floor_center.x*2 , 75/2-floor_center.y))
    pygame.draw.rect(background,"blue",game_window)
    for rect in obstacle_list:
        pygame.draw.rect(background,"red",rect)
    pygame.draw.rect(background,"green",player)
    pygame.display.update()
    
    dt = clock.tick(60) // 1000
    
pygame.quit()
sys.exit()