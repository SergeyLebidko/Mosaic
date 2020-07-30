import pygame
import random
from settings import SPRITES_FOLDER, FIELD_RECT, SPRITE_COLORS_COUNT, COL_COUNT, ROW_COUNT
from utils import get_cell_for_coords, get_coords_for_cell, mix_polyminos


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

        if self._polymino_failed_field() or self._polymino_failed_cells():
            for monomino in self.polymino.monomino_list:
                monomino.rect.x, monomino.rect.y = get_coords_for_cell(monomino.row, monomino.col)
        else:
            for monomino in self.polymino.monomino_list:
                monomino.row, monomino.col = get_cell_for_coords(*monomino.rect.center)
                monomino.refresh_coords()

        self.polymino = None

    def _polymino_failed_field(self):
        polymino_rect = self.polymino.monomino_list[0].rect.unionall(
            [monomino.rect for monomino in self.polymino.monomino_list[1:]]
        )
        return not FIELD_RECT.contains(polymino_rect)

    def _polymino_failed_cells(self):
        c1 = [(get_cell_for_coords(*monomino.rect.center)) for monomino in self.polymino.monomino_list]
        c2 = [
            (monomino.row, monomino.col)
            for polymino in self.polymino_list
            for monomino in polymino.monomino_list
            if polymino is not self.polymino
        ]
        return len(set(c1) & set(c2)) != 0


class Level:

    def __init__(self):
        self.areas = []
        count = 3
        for row in range(3, 14, 2):
            for col in range(row - 3, row + 6, 2):
                if col < 3 or col > 14:
                    continue
                self.areas.extend([(row, col)] * count)
                count += 1

        self.areas.sort(key=lambda c: c[0] * c[1])

        self.levels_count = len(self.areas)
        self.level_number = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.level_number == len(self.areas):
            self.level_number = 1

        # Количество строк и столбцов в целевой области текущего уровня
        area_rows_count, area_cols_count = self.areas[self.level_number]

        # Площадь целевой области
        total_space = area_rows_count * area_cols_count

        # Словарь, в котором будем накапливать данные полимино
        data = {}

        # Составляем список свободных ячеек
        free_cells = [(row, col) for row in range(area_rows_count) for col in range(area_cols_count)]

        # Общее количество полимино, которое будет на уровне (зависит от площади)
        count_polyminos = total_space // 4

        # Расставляем точки формирования полимино
        for marker in range(count_polyminos + 1):
            cell = free_cells.pop(random.randint(0, len(free_cells)-1))
            data[marker] = [cell]

        # Допустимые смещения по осям
        deltas = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        # Запукаем "рост" полимино
        while free_cells:
            for marker, cells in data.items():
                available_cells = [
                    (cell[0] + delta_row, cell[1] + delta_col)
                    for cell in cells
                    for delta_row, delta_col in deltas
                    if (cell[0] + delta_row, cell[1] + delta_col) in free_cells
                ]
                if available_cells:
                    select_cell = random.choice(available_cells)
                    free_cells.remove(select_cell)
                    data[marker].append(select_cell)

        # Формируем полимино на основе сформированных данных
        polymino_list = []
        anchor_row = (ROW_COUNT // 2) - (area_rows_count // 2)
        anchor_col = (COL_COUNT // 2) - (area_cols_count // 2)
        color_number = 1
        for _, cells in data.items():
            polymino = Polymino()
            for row, col in cells:
                polymino.add(Monomino(anchor_row + row, anchor_col + col, color_number))
            polymino_list.append(polymino)
            color_number += 1
            if color_number > SPRITE_COLORS_COUNT:
                color_number = 1

        # Располагаем полимино на поле в случайном порядке
        mix_polyminos(polymino_list)

        # В словаре будет храниться описание уровня
        level = {
            'level_number': self.level_number + 1,
            'polymino_list': polymino_list,
            'area': (anchor_row, anchor_col, area_rows_count, area_cols_count)
        }

        self.level_number += 1
        return level
