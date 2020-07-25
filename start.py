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
    move_functions = {
        273: [lambda v: v - 15, 'centery'],
        275: [lambda v: v + 15, 'centerx'],
        274: [lambda v: v + 15, 'centery'],
        276: [lambda v: v - 15, 'centerx']
    }
    move_list = []

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                move_list.append(event.key)

            if event.type == pygame.KEYUP:
                move_list.remove(event.key)

        for move in move_list:
            old_top, old_right, old_bottom, old_left = square.top, square.right, square.bottom, square.left
            function, value_name = move_functions[move]
            value = getattr(square, value_name)
            value = function(value)
            setattr(square, value_name, value)
            if square.top < 0 or square.right > W or square.bottom > H or square.left < 0:
                square.top, square.right, square.bottom, square.left = old_top, old_right, old_bottom, old_left

        sc.fill((0, 0, 0))
        pygame.draw.rect(sc, (255, 255, 255), square)

        pygame.display.update()
        clock.tick(FPS)
