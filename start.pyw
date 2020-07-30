import pygame
import time
from settings import CELL_SIZE, W, H, WINDOW_TITLE, FPS, SPRITES_FOLDER
from classes import Drag, Level
from utils import draw_grid, create_sprite_folder, create_sprites, create_square_sprite, draw_polyminos, draw_area, \
    is_level_finish, draw_msg


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

    # Создаем шрифт
    font = pygame.font.Font(None, 36)

    levels = Level()
    for level in levels:
        polymino_list = level['polymino_list']
        area = level['area']
        level_number = level['level_number']

        msg = f'Уровень {level_number} из {levels.levels_count}'
        drag = Drag(polymino_list)

        level_finish = False
        while not level_finish:
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
                    level_finish = is_level_finish(*area, polymino_list)

            draw_grid(sc)
            draw_msg(sc, msg, font)
            draw_area(sc, *area)
            draw_polyminos(sc, polymino_list, drag)

            pygame.display.update()
            clock.tick(FPS)

        time.sleep(1)


if __name__ == '__main__':
    main()
