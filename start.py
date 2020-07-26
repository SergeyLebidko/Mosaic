import pygame
from sprite_generator import create_sprites, create_square_sprite, SPRITES_FOLDER

# Частота обновления окна
FPS = 30

# Размер ячейки фоновой сетки
CELL_SIZE = 50

# Размер окна
W, H = CELL_SIZE * 32, CELL_SIZE * 17

# Заголовок окна
WINDOW_TITLE = 'Mosaic'

# Цвет фона ячеек
CELL_COLOR = (220, 220, 220)

# Цвет сетки
GRID_COLOR = (120, 120, 120)


def draw_grid(surface):
    surface.fill(CELL_COLOR)
    for x in range(CELL_SIZE, W - CELL_SIZE + 1, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, CELL_SIZE), (x, H - CELL_SIZE))
    for y in range(CELL_SIZE, H - CELL_SIZE + 1, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (CELL_SIZE, y), (W - CELL_SIZE, y))


def main():
    create_sprites(CELL_SIZE - 2)
    create_square_sprite(16, (255, 0, 0), 'icon')

    pygame.init()
    sc = pygame.display.set_mode((W, H))
    icon = pygame.image.load(f'{SPRITES_FOLDER}/icon.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption(WINDOW_TITLE)

    clock = pygame.time.Clock()

    square = pygame.Rect(0, 0, CELL_SIZE - 2, CELL_SIZE - 2)
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

        draw_grid(sc)
        pygame.draw.rect(sc, (255, 255, 255), square)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
