import pygame
import random
from settings import SPRITES_FOLDER, FIELD_RECT, SPRITE_COLORS_COUNT, COL_COUNT, ROW_COUNT
from functions import get_cell_for_coords, get_coords_for_cell


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
        c2 = [(monomino.row, monomino.col) for polymino in self.polymino_list for monomino in polymino.monomino_list]
        return len(set(c1) & set(c2)) != 0


class Level:
    areas = [(7, 6)]

    def __init__(self):
        self.level_number = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.level_number == len(self.areas):
            raise StopIteration

        # Количество строк и столбцов в целевой области текущего уровня
        area_rows_count, area_cols_count = self.areas[self.level_number]

        # Площадь целевой области
        total_space = area_rows_count * area_cols_count

        # Флаги переходов для формирования полимино
        flags_count = 2 * area_cols_count * area_rows_count - area_cols_count - area_rows_count
        flags = [(index < (3 * total_space / 4)) for index in range(flags_count)]
        random.shuffle(flags)

        # Словарь, в котором будем накапливать данные для формирования полимино
        data = {}

        marker = 0
        current_area = [[0] * area_cols_count for _ in range(area_rows_count)]
        for row in range(area_rows_count):
            for col in range(area_cols_count):
                if current_area[row][col] == 0:
                    marker += 1
                    current_area[row][col] = marker
                    data[marker] = [(row, col)]
                    current_marker = marker
                else:
                    current_marker = current_area[row][col]

                if row < (area_rows_count - 1):
                    flag = flags.pop()
                    if flag:
                        row_beside, col_beside = row + 1, col
                        if not current_area[row_beside][col_beside]:
                            current_area[row_beside][col_beside] = current_marker
                            data[current_marker].append((row_beside, col_beside))

                if col < (area_cols_count - 1):
                    flag = flags.pop()
                    if flag:
                        row_beside, col_beside = row, col + 1
                        if not current_area[row_beside][col_beside]:
                            current_area[row_beside][col_beside] = current_marker
                            data[current_marker].append((row_beside, col_beside))

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

        # В словаре будет храниться описание уровня
        level = {
            'level_number': self.level_number + 1,
            'polymino_list': polymino_list,
            'area': (anchor_row, anchor_col, area_rows_count, area_cols_count)
        }

        self.level_number += 1
        return level
