import os
import pygame
import random
from PIL import Image, ImageDraw
from settings import CELL_SIZE, CELL_COLOR, GRID_COLOR, W, H, SPRITES_FOLDER, SPRITE_COLOR_LEVEL_COUNT, \
    SPRITE_CENTER_AREA, TRANSPARENCY_COLOR, COLOR_PRESETS, AREA_COLORS, ROW_COUNT, COL_COUNT


def get_coords_for_cell(row, col):
    return CELL_SIZE + (CELL_SIZE * col) + 1, CELL_SIZE + (CELL_SIZE * row) + 1


def get_cell_for_coords(x, y):
    return y // CELL_SIZE - 1, x // CELL_SIZE - 1


def mix_polyminos(polymino_list):
    for polymino in polymino_list:

        # Выполняем случайное количество вращений - от 0 до 3
        for _ in range(0, random.randint(0, 4)):
            polymino.rotate()

        # Фиксируем положение после вращения
        for monomino in polymino.monomino_list:
            monomino.row, monomino.col = get_cell_for_coords(*monomino.rect.center)

        # Ищем якорную точку, ширину и высоту полимино
        anchor_row = min([monomino.row for monomino in polymino.monomino_list])
        anchor_col = min([monomino.col for monomino in polymino.monomino_list])

        polymino_width = max([(monomino.col - anchor_col + 1) for monomino in polymino.monomino_list])
        polymino_height = max([(monomino.row - anchor_row + 1) for monomino in polymino.monomino_list])

        # Устанавливаем положение полимино в левый верхний угол поля
        for monomino in polymino.monomino_list:
            monomino.row, monomino.col = monomino.row - anchor_row, monomino.col - anchor_col

        # Составляем список занятых ячеек
        busy_cells = [(m.row, m.col) for p in polymino_list for m in p.monomino_list if p is not polymino]

        crossing = True
        while crossing:
            delta_row = random.randint(0, ROW_COUNT - polymino_height)
            delta_col = random.randint(0, COL_COUNT - polymino_width)
            tmp_cells = [(monomino.row + delta_row, monomino.col + delta_col) for monomino in polymino.monomino_list]
            crossing = set(tmp_cells) & set(busy_cells)

        # Применяем изменения
        for cell, monomino in zip(tmp_cells, polymino.monomino_list):
            monomino.row, monomino.col = cell[0], cell[1]
            monomino.refresh_coords()


def is_level_finish(anchor_row, anchor_col, area_rows_count, area_cols_count, polymino_list):
    for polymino in polymino_list:
        for monomino in polymino.monomino_list:
            check_row = anchor_row <= monomino.row < (anchor_row + area_rows_count)
            check_col = anchor_col <= monomino.col < (anchor_col + area_cols_count)
            if not (check_row and check_col):
                return False
    return True


def draw_grid(surface):
    surface.fill(CELL_COLOR)
    for x in range(CELL_SIZE, W - CELL_SIZE + 1, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, CELL_SIZE), (x, H - CELL_SIZE))
    for y in range(CELL_SIZE, H - CELL_SIZE + 1, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (CELL_SIZE, y), (W - CELL_SIZE, y))


def draw_polyminos(surface, polymino_list, drag):
    for polymino in polymino_list:
        if polymino is not drag.polymino:
            polymino.blit(surface)
    if drag.polymino:
        drag.polymino.blit(surface)


def draw_area(surface, anchor_row, anchor_col, area_rows_count, area_cols_count):
    x0, y0 = get_coords_for_cell(anchor_row, anchor_col)
    w, h = CELL_SIZE * area_cols_count - 1, CELL_SIZE * area_rows_count - 1

    area_surface = pygame.Surface((w, h))
    area_surface.set_alpha(80)

    for x in range(0, w + 1, 10):
        for y in range(0, h + 1, 10):
            color = AREA_COLORS[((x // 10) + (y // 10)) % 2]
            pygame.draw.rect(area_surface, color, (x, y, 10, 10))

    surface.blit(area_surface, (x0, y0))


def create_sprite_folder():
    try:
        os.mkdir(SPRITES_FOLDER)
    except FileExistsError:
        pass


def create_square_sprite(r0=100, color=(255, 255, 255), filename='square'):
    # Вспомогательные объекты для создания изображения
    img = Image.new('RGB', (r0, r0))
    draw = ImageDraw.Draw(img)

    r_color, g_color, b_color = color
    for k in range(SPRITE_COLOR_LEVEL_COUNT, 0, -1):
        r = r0 - (r0 / (SPRITE_COLOR_LEVEL_COUNT + SPRITE_CENTER_AREA)) * (SPRITE_COLOR_LEVEL_COUNT - k)
        x1, y1 = (r0 - r) / 2, (r0 - r) / 2
        x2, y2 = x1 + r, y1 + r
        background_color = (
            r_color - int((r_color / 3) * ((k - 1) / SPRITE_COLOR_LEVEL_COUNT)),
            g_color - int((g_color / 3) * ((k - 1) / SPRITE_COLOR_LEVEL_COUNT)),
            b_color - int((b_color / 3) * ((k - 1) / SPRITE_COLOR_LEVEL_COUNT))
        )
        draw.rectangle((x1, y1, x2, y2), fill=background_color)

    img.save(f'{SPRITES_FOLDER}/{filename}.png', 'png', transparency=TRANSPARENCY_COLOR)


def create_sprites(r0=100):
    for number, color in enumerate(COLOR_PRESETS, 1):
        create_square_sprite(r0=r0, color=color, filename=f'{number}')
