import pygame

pygame.init()

screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption('Cyberblast 9000')
input_box = pygame.Rect(0, 0, 200, 64)
user_text = ''
active = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(user_text)
            elif event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                user_text += event.unicode
                
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, "white", input_box, 2)
    text_surface = pygame.font.Font(None, 64).render(user_text, True, (255, 255, 255))
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
    pygame.display.flip()
