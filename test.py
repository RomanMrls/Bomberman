import pygame

pygame.init()

screen = pygame.display.set_mode((1000, 900))
pygame.display.set_caption('Cyberblast 9000')
input_box = pygame.Rect(100, 50, 140, 32)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
user_text = ''
active = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    print(user_text)
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
                
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, color, input_box, 2)
    text_surface = pygame.font.Font(None, 32).render(user_text, True, (0, 0, 0))
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
    pygame.display.flip()
