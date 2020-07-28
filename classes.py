import pygame
from settings import SPRITES_FOLDER, FIELD_RECT
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


class Level:

    def __iter__(self):
        return self

    def __next__(self):

        # Строку ниже - в дальнейшем удалить
        from start import create_polymino
        level = {
            'polymino_list': [create_polymino('XXXX|X___|XX__|X___', 5)]
        }
        return level
