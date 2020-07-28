import pygame
from sprite_generator import create_sprite_folder, create_sprites, create_square_sprite
from settings import CELL_SIZE, W, H, WINDOW_TITLE, FPS, SPRITES_FOLDER
from classes import Monomino, Polymino, Drag, Level
from functions import draw_grid


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

    # Создаем объект для ограничения FPS
    clock = pygame.time.Clock()

    for level in Level():
        polymino_list = level['polymino_list']
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
            for polymino in polymino_list:
                polymino.blit(sc)

            pygame.display.update()
            clock.tick(FPS)


if __name__ == '__main__':
    main()
