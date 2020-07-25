import pygame
from sprite_generator import create_sprites, square_generator, SPRITES_FOLDER

FPS = 30
W, H = 1200, 800
WINDOW_TITLE = 'Mosaic'

if __name__ == '__main__':
    create_sprites()
    square_generator(16, (255, 0, 0), 'icon')

    pygame.init()
    sc = pygame.display.set_mode((W, H))
    icon = pygame.image.load(f'{SPRITES_FOLDER}/icon.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption(WINDOW_TITLE)

    clock = pygame.time.Clock()

    square = pygame.Rect(0, 0, 50, 50)
    drag_flag = False

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                x_press, y_press = event.pos
                if square.left <= x_press <= square.right and square.top <= y_press <= square.bottom:
                    drag_flag = True

            if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
                drag_flag = False

            if event.type == pygame.MOUSEMOTION and drag_flag:
                dx, dy = event.rel
                square.centerx += dx
                square.centery += dy

        sc.fill((0, 0, 0))
        pygame.draw.rect(sc, (255, 255, 255), square)

        pygame.display.update()
        clock.tick(FPS)
