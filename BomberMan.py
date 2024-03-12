import pygame,sys

pygame.init()
screen = pygame.display.set_mode((1000, 900))
pygame.display.set_caption('Bomberman')

screenx = 1000
screeny = 900

background = pygame.Surface((screenx, screeny))
background.fill((0,0,0))

game_size = (750,750)
game_window_pos = pygame.Vector2((screenx-game_size[0])/2,(screeny-game_size[1])/1.5)
game_window= pygame.Rect(game_window_pos,game_size)

player_pos = pygame.Vector2(game_window_pos)
player_size = (40,40)
player = pygame.Rect(player_pos,player_size)
direction = {pygame.K_LEFT: (-5, 0), pygame.K_RIGHT: (5, 0), pygame.K_UP: (0, -5), pygame.K_DOWN: (0, 5)}

obstacle_pos_list = [[(56.25*i+game_window_pos.x,56.25*j+game_window_pos.y) for i in range(1,13,2)] for j in range(1,13,2)]
obstacle_size = (56.25,56.25)
obstacle_list = [[pygame.Rect(pos,obstacle_size) for pos in ligne] for ligne in obstacle_pos_list]
obstacle_list = sum(obstacle_list, [])

clock = pygame.time.Clock()

game_over = False

while not game_over:
    clock.tick(60)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.draw.rect(background,"green",player)
    if event.type == pygame.KEYDOWN:
        if event.key in direction:
            v = direction[event.key]
            temp_player = player.copy()
            temp_player.move_ip(v)
            if game_window.contains(temp_player) and temp_player.collidelistall(obstacle_list) == list():
                player.move_ip(v)
        
    screen.blit(background,(0, 0))
    pygame.draw.rect(background,"blue",game_window)
    for rect in obstacle_list:
        pygame.draw.rect(background,"red",rect)
    pygame.display.update()
    
    dt = clock.tick(60) // 2000
    
pygame.quit()
sys.exit()