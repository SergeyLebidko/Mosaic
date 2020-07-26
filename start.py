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


class Monomino(pygame.sprite.Sprite):

    def __init__(self, row, col, color_number):
        super().__init__()
        self.image = pygame.image.load(f'{SPRITES_FOLDER}/{color_number}.png')
        self.rect = self.image.get_rect()
        self.rect.x = CELL_SIZE + (CELL_SIZE * col) + 1
        self.rect.y = CELL_SIZE + (CELL_SIZE * row) + 1


class Polymino:

    def __init__(self):
        self.monomino_list = []

    def add(self, monomino):
        self.monomino_list.append(monomino)

    def move_ip(self, dx, dy):
        for monomino in self.monomino_list:
            monomino.rect.move_ip((dx, dy))

    def collidepoint(self, x, y):
        return any([monomino.rect.collidepoint((x, y)) for monomino in self.monomino_list])

    def blit(self, surface):
        for monomino in self.monomino_list:
            surface.blit(monomino.image, monomino.rect)


def create_polymino(data, color_number):
    polymino = Polymino()

    data = data.split('|')
    row = 0
    for line in data:
        col = 0
        for element in line:
            if element != '_':
                monomino = Monomino(row, col, color_number)
                polymino.add(monomino)
            col += 1
        row += 1

    return polymino


def draw_grid(surface):
    surface.fill(CELL_COLOR)
    for x in range(CELL_SIZE, W - CELL_SIZE + 1, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, CELL_SIZE), (x, H - CELL_SIZE))
    for y in range(CELL_SIZE, H - CELL_SIZE + 1, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (CELL_SIZE, y), (W - CELL_SIZE, y))


def main():
    create_sprites(CELL_SIZE - 1)
    create_square_sprite(16, (255, 0, 0), 'icon')

    pygame.init()
    sc = pygame.display.set_mode((W, H))
    icon = pygame.image.load(f'{SPRITES_FOLDER}/icon.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption(WINDOW_TITLE)

    clock = pygame.time.Clock()

    polymino = create_polymino('_X__|XX__|_XX_|__X_', 5)
    drag_flag = False

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                if polymino.collidepoint(*event.pos):
                    drag_flag = True

            if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
                drag_flag = False

            if event.type == pygame.MOUSEMOTION and drag_flag:
                polymino.move_ip(*event.rel)

        draw_grid(sc)
        polymino.blit(sc)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
