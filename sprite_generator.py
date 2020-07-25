import os
import math
from PIL import Image, ImageDraw

demo_data = [
    (255, 255, 255, 'white'),
    (120, 120, 120, 'dark'),

    (255, 0, 0, 'red'),
    (0, 255, 0, 'green'),
    (0, 0, 255, 'blue'),

    (255, 255, 0, 'mix1'),
    (0, 255, 255, 'mix2'),
    (255, 0, 255, 'mix3'),

    (255, 80, 0, 'scale1'),
    (255, 0, 80, 'scale2'),

    (0, 255, 80, 'scale3'),
    (80, 255, 0, 'scale4'),

    (0, 80, 255, 'scale5'),
    (80, 0, 255, 'scale6'),
]

# Папка для хранения спрайтов
SPRITES_FOLDER = 'images'

# Цвет фона по-умолчанию для pillow
TRANSPARENCY_COLOR = (0, 0, 0)

# Количество цветовых переходов
LEVEL_COUNT = 5

# Ширина центральной зоны
CENTER_AREA = 1


def square_generator(r0=100, color=(255, 255, 255), filename='square'):
    # Вспомогательные объекты для создания изображения
    img = Image.new('RGB', (r0, r0))
    draw = ImageDraw.Draw(img)

    r_color, g_color, b_color = color
    for k in range(LEVEL_COUNT, 0, -1):
        r = r0 - (r0 / (LEVEL_COUNT + CENTER_AREA)) * (LEVEL_COUNT - k)
        x1 = (r0 - r) / 2
        y1 = (r0 - r) / 2
        x2 = x1 + r
        y2 = y1 + r
        background_color = (
            r_color - int((r_color / 3) * ((k - 1) / LEVEL_COUNT)),
            g_color - int((g_color / 3) * ((k - 1) / LEVEL_COUNT)),
            b_color - int((b_color / 3) * ((k - 1) / LEVEL_COUNT))
        )
        draw.rectangle((x1, y1, x2, y2), fill=background_color)

    img.save(f'{SPRITES_FOLDER}/{filename}.png', 'png', transparency=TRANSPARENCY_COLOR)


def hexagon_generator(r0=100, color=(255, 255, 255), filename='hexagon'):
    # Ширина/высота поля
    w, h = 1000, 1000

    # Координаты центра поля
    x0, y0 = w // 2, h // 2

    # Вспомогательные объекты для создания изображения
    img = Image.new('RGB', (w, h), TRANSPARENCY_COLOR)
    draw = ImageDraw.Draw(img)

    min_x, min_y, max_x, max_y = w + 1, h + 1, -1, -1
    r_color, g_color, b_color = color
    for k in range(LEVEL_COUNT, 0, -1):

        # Определяем параметры шестиугольника - цвет и размер (движемся от большего к меньшему)
        r = r0 - (r0 / (LEVEL_COUNT + CENTER_AREA)) * (LEVEL_COUNT - k)
        background_color = (
            r_color - int((r_color / 3) * ((k - 1) / LEVEL_COUNT)),
            g_color - int((g_color / 3) * ((k - 1) / LEVEL_COUNT)),
            b_color - int((b_color / 3) * ((k - 1) / LEVEL_COUNT))
        )

        # Определяем координаты вершин шестиугольника и рисуем его
        coords = []
        for index in range(0, 6):
            x = r * math.cos(index * (math.pi / 3))
            y = r * math.sin(index * (math.pi / 3))
            coords.append(x0 + x)
            coords.append(y0 - y)
        draw.polygon(coords, fill=background_color)

        # Определяем координаты прямоугольника, в который вписан самый большой шестиугольник
        if k == LEVEL_COUNT:
            x_coords = coords[0:len(coords):2]
            y_coords = coords[1:len(coords):2]
            min_x = min(min_x, *x_coords)
            min_y = min(min_y, *y_coords)
            max_x = max(max_x, *x_coords)
            max_y = max(max_y, *y_coords)

    # Отрезаем лишние поля и сохраняем изображение
    img = img.crop((min_x, min_y, max_x, max_y))
    img.save(f'{SPRITES_FOLDER}/{filename}.png', 'png', transparency=TRANSPARENCY_COLOR)


def create_sprites():
    try:
        os.mkdir(SPRITES_FOLDER)
    except FileExistsError:
        pass
    for *color, filename in demo_data:
        hexagon_generator(color=color, filename=f'hex_{filename}')
        square_generator(color=color, filename=f'square_{filename}')
