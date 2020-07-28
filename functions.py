import pygame
from settings import CELL_SIZE, CELL_COLOR, GRID_COLOR, W, H


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
