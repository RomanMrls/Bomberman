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

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

player_size = (50,50)
player = pygame.Rect(player_pos,player_size)
direction = {pygame.K_LEFT: (-5, 0), pygame.K_RIGHT: (5, 0), pygame.K_UP: (0, -5), pygame.K_DOWN: (0, 5)}

clock = pygame.time.Clock()

game_over = False

while not game_over:
    clock.tick(165)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    if game_window.contains(player):
         if event.type == pygame.KEYDOWN:
            if event.key in direction:
                v = direction[event.key]
                player.move_ip(v)
        
    screen.blit(background,(0, 0))
    pygame.draw.rect(background,"blue",game_window)
    pygame.draw.rect(background,"red",player)
    pygame.display.update()
    
    dt = clock.tick(60) // 1000
    
pygame.quit()
sys.exit()
