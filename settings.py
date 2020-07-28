import pygame

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

# Количество цветов
SPRITE_COLORS_COUNT = len(COLOR_PRESETS)

# Папка для хранения спрайтов
SPRITES_FOLDER = 'images'

# Цвет фона по-умолчанию для pillow
TRANSPARENCY_COLOR = (0, 0, 0)

# Количество цветовых переходов
SPRITE_COLOR_LEVEL_COUNT = 5

# Ширина центральной зоны спрайта
SPRITE_CENTER_AREA = 1

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

# Цвета для фона целевой области
AREA_COLORS = (
    (80, 80, 80),
    (120, 120, 120)
)
