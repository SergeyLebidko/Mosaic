import os
import pygame
from PIL import Image, ImageDraw
from settings import CELL_SIZE, CELL_COLOR, GRID_COLOR, W, H, SPRITES_FOLDER, SPRITE_COLOR_LEVEL_COUNT, \
    SPRITE_CENTER_AREA, TRANSPARENCY_COLOR, COLOR_PRESETS


def get_coords_for_cell(row, col):
    return CELL_SIZE + (CELL_SIZE * col) + 1, CELL_SIZE + (CELL_SIZE * row) + 1


def get_cell_for_coords(x, y):
    return y // CELL_SIZE - 1, x // CELL_SIZE - 1


def draw_grid(surface):
    surface.fill(CELL_COLOR)
    for x in range(CELL_SIZE, W - CELL_SIZE + 1, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, CELL_SIZE), (x, H - CELL_SIZE))
    for y in range(CELL_SIZE, H - CELL_SIZE + 1, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (CELL_SIZE, y), (W - CELL_SIZE, y))


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
