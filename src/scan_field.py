import matplotlib.pyplot as plt
import numpy as np
from mss import mss
from config import CONFIG

consts = CONFIG['consts']


def print_image(arr, figure_size=10):
    if CONFIG['debug status'] == 1:
        n = len(arr)
        fig = plt.figure(figsize=(figure_size, figure_size))
        for i in range(n):
            fig.add_subplot(1, n, i + 1)
            plt.imshow(arr[i])


def cmp_pixel(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2])


def get_figure_by_color(screen):
    """
    finds next piece class based on color
    shape recognition is difficult because the piece is not aligned with a grid
    :param screen: part of screen with next piece
    :return: piece class
    """
    for i in range(len(screen)):
        for j in range(len(screen[0])):
            pixel = screen[i, j][:3]
            for piece_idx in range(len(CONFIG['piece colors'])):
                distance = cmp_pixel(CONFIG['piece colors'][piece_idx][::-1], pixel)
                if distance < 10:
                    return piece_idx
    return -1


def get_field() -> (np.array, int):
    """
    takes a screenshot and computes playing grid
    :return: field grid, next piece id
    """
    monitor = {"left": 0, "top": 0, "width": CONFIG['screen width'], "height": CONFIG['screen height']}
    with mss() as sct:
        img = np.array(sct.grab(monitor))
        pixels = consts.get_field_from_screen(img)

        next_piece = get_figure_by_color(consts.get_next(img))
        # all empty initially
        field = np.zeros((20 + CONFIG['extra rows'], 10))
        # find middles of grid cells
        cell_size = pixels.shape[1] // 10
        vertical_centers = np.array(np.linspace(cell_size // 2, pixels.shape[0] + cell_size // 2, 21 + CONFIG['extra rows'])[:-1], int)
        horizontal_centers = np.array(np.linspace(cell_size // 2, pixels.shape[1] + cell_size // 2, 11)[:-1], int)
        # go through all cell centers
        for i, v in enumerate(vertical_centers):
            for j, h in enumerate(horizontal_centers):
                if pixels[v][h] == 1:
                    # check a nearby pixel to ensure its not a snowflake or a star
                    if pixels[v+5][h+5] == 1:
                        field[i][j] = 1
        return field, next_piece
