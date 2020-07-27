import pygame
from sprite_generator import create_sprite_folder, create_sprites, create_square_sprite, SPRITES_FOLDER

# Частота обновления окна
FPS = 30

# Размер ячейки фоновой сетки
CELL_SIZE = 50

# Количество ячеек на игровом поле
ROW_COUNT, COL_COUNT = 15, 30

# Размер окна
W, H = CELL_SIZE * (COL_COUNT + 2), CELL_SIZE * (ROW_COUNT + 2)

# Прямоугольник для игрового поля
FIELD_RECT = pygame.Rect(CELL_SIZE, CELL_SIZE, CELL_SIZE * COL_COUNT, CELL_SIZE * ROW_COUNT)

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
        self.row, self.col = row, col
        self.refresh_coords()

    def refresh_coords(self):
        self.rect.x, self.rect.y = get_coords_for_cell(self.row, self.col)


class Polymino:

    def __init__(self):
        self.monomino_list = []

    def add(self, monomino):
        self.monomino_list.append(monomino)

    def move(self, dx, dy):
        for monomino in self.monomino_list:
            monomino.rect.move_ip((dx, dy))

    def rotate(self):
        x0 = sum([monomino.rect.centerx for monomino in self.monomino_list]) / len(self.monomino_list)
        y0 = sum([monomino.rect.centery for monomino in self.monomino_list]) / len(self.monomino_list)
        for monomino in self.monomino_list:
            x1, y1 = x0 - (monomino.rect.centery - y0), y0 + (monomino.rect.centerx - x0)
            monomino.rect.centerx, monomino.rect.centery = x1, y1

    def collidepoint(self, x, y):
        return any([monomino.rect.collidepoint((x, y)) for monomino in self.monomino_list])

    def blit(self, surface):
        for monomino in self.monomino_list:
            surface.blit(monomino.image, monomino.rect)


class Drag:

    def __init__(self, polymino_list):
        self.polymino_list = polymino_list
        self.polymino = None

    def take(self, x, y):
        for polymino in self.polymino_list:
            if polymino.collidepoint(x, y):
                self.polymino = polymino

    def move(self, dx, dy):
        if self.polymino:
            self.polymino.move(dx, dy)

    def rotate(self):
        if self.polymino:
            self.polymino.rotate()

    def drop(self):
        if not self.polymino:
            return
        polymino_rect = self.polymino.monomino_list[0].rect.unionall(
            [monomino.rect for monomino in self.polymino.monomino_list[1:]]
        )
        if FIELD_RECT.contains(polymino_rect):
            for monomino in self.polymino.monomino_list:
                monomino.row, monomino.col = get_cell_for_coords(monomino.rect.centerx, monomino.rect.centery)
                monomino.refresh_coords()
        else:
            for monomino in self.polymino.monomino_list:
                monomino.rect.x, monomino.rect.y = get_coords_for_cell(monomino.row, monomino.col)
        self.polymino = None


def draw_grid(surface):
    surface.fill(CELL_COLOR)
    for x in range(CELL_SIZE, W - CELL_SIZE + 1, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, CELL_SIZE), (x, H - CELL_SIZE))
    for y in range(CELL_SIZE, H - CELL_SIZE + 1, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (CELL_SIZE, y), (W - CELL_SIZE, y))


def get_coords_for_cell(row, col):
    return CELL_SIZE + (CELL_SIZE * col) + 1, CELL_SIZE + (CELL_SIZE * row) + 1


def get_cell_for_coords(x, y):
    return y // CELL_SIZE - 1, x // CELL_SIZE - 1


# Временная функция для тетирования
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


def main():
    # Создаем спрайты для игры и иконку окна
    create_sprite_folder()
    create_sprites(CELL_SIZE - 1)
    create_square_sprite(16, (255, 0, 0), 'icon')

    # Инициализируем окно игры
    pygame.init()
    sc = pygame.display.set_mode((W, H))
    icon = pygame.image.load(f'{SPRITES_FOLDER}/icon.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption(WINDOW_TITLE)

    clock = pygame.time.Clock()
    polymino_list = []

    polymino = create_polymino('XXXX|X___|XX__|X___', 5)
    polymino_list.append(polymino)

    drag = Drag(polymino_list)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Захват мышкой полимино
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                drag.take(*event.pos)

            # Поворот захваченного полимино
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT:
                drag.rotate()

            # Перемещение захваченного полимино
            if event.type == pygame.MOUSEMOTION and drag:
                drag.move(*event.rel)

            # Сброс захвата полимино
            if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
                drag.drop()

        draw_grid(sc)
        polymino.blit(sc)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
