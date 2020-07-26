import os
from PIL import Image, ImageDraw

# Пресеты цветов создаваемых спрайтов
COLOR_PRESETS = [
    (255, 255, 255),
    (120, 120, 120),
    (255, 0, 0),
    (0, 255, 0),
    (150, 150, 255),
    (255, 255, 0),
    (128, 255, 255),
    (255, 0, 255),
    (255, 128, 0)
]

# Папка для хранения спрайтов
SPRITES_FOLDER = 'images'

# Цвет фона по-умолчанию для pillow
TRANSPARENCY_COLOR = (0, 0, 0)

# Количество цветовых переходов
LEVEL_COUNT = 5

# Ширина центральной зоны
CENTER_AREA = 1


def create_sprite_folder():
    try:
        os.mkdir(SPRITES_FOLDER)
    except FileExistsError:
        pass


def create_square_sprite(r0=30, color=(255, 255, 255), filename='square'):
    # Вспомогательные объекты для создания изображения
    img = Image.new('RGB', (r0, r0))
    draw = ImageDraw.Draw(img)

    r_color, g_color, b_color = color
    for k in range(LEVEL_COUNT, 0, -1):
        r = r0 - (r0 / (LEVEL_COUNT + CENTER_AREA)) * (LEVEL_COUNT - k)
        x1, y1 = (r0 - r) / 2, (r0 - r) / 2
        x2, y2 = x1 + r, y1 + r
        background_color = (
            r_color - int((r_color / 3) * ((k - 1) / LEVEL_COUNT)),
            g_color - int((g_color / 3) * ((k - 1) / LEVEL_COUNT)),
            b_color - int((b_color / 3) * ((k - 1) / LEVEL_COUNT))
        )
        draw.rectangle((x1, y1, x2, y2), fill=background_color)

    img.save(f'{SPRITES_FOLDER}/{filename}.png', 'png', transparency=TRANSPARENCY_COLOR)


def create_sprites():
    for number, color in enumerate(COLOR_PRESETS, 1):
        create_square_sprite(color=color, filename=f'{number}')
