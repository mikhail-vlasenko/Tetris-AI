import matplotlib.pyplot as plt
import numpy as np
from mss import mss
import data

consts = data.tertio_default  # CUSTOM
extra_rows = 2  # in some Tetrises (tetr.io) pieces spawn above the main field
debug_status = 0

# 0 - line, 1 - square, 2 - T(flip), 3 - |__, 4 - __|, 5 - -|_,6 - _|-
piece_colors = dict()
# original colors
piece_colors[0] = (230, 228, 180)
piece_colors[1] = (182, 228, 247)
piece_colors[2] = (177, 99, 140)
piece_colors[3] = (228, 177, 148)
piece_colors[4] = (128, 180, 235)
piece_colors[5] = (180, 161, 235)
piece_colors[6] = (171, 240, 177)
# tetr.io colors (should be reversed from RGB)
piece_colors[0] = (36, 214, 150)
piece_colors[1] = (210, 171, 42)
piece_colors[2] = (212, 67, 195)
piece_colors[3] = (70, 56, 200)
piece_colors[4] = (217, 96, 48)
piece_colors[5] = (222, 44, 63)
piece_colors[6] = (131, 210, 42)


def print_image(arr, figure_size=10):
    if debug_status == 1:
        n = len(arr)
        fig = plt.figure(figsize=(figure_size, figure_size))
        for i in range(n):
            fig.add_subplot(1, n, i + 1)
            plt.imshow(arr[i])
    else:
        pass


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
            for piece_idx in range(len(piece_colors)):
                distance = cmp_pixel(piece_colors[piece_idx][::-1], pixel)
                if distance < 10:
                    return piece_idx
    return -1


def get_field_deprecated():
    monitor = {"left": 0, "top": 0, "width": 2560, "height": 1440}
    with mss() as sct:
        img = np.array(sct.grab(monitor))
        field = consts.get_field_from_screen(img)

        next_piece = get_figure_by_color(consts.get_next(img))

        size_cell = field.shape[0] // 20
        arr = np.zeros((20, 10))
        for i in range(size_cell):
            r1 = np.array(np.linspace(0, field.shape[0], 21)[:-1], int) + i
            r2 = np.array(np.linspace(0, field.shape[1], 11)[:-1], int) + i
            arr += field[r1][:, r2]

        kek = np.array(arr / size_cell + 0.5, int)
        print_image((img, field, kek))
        return kek, next_piece


def get_field():
    """
    takes a screenshot and computes playing grid
    :return: field grid, next piece id
    """
    monitor = {"left": 0, "top": 0, "width": 2560, "height": 1440}
    with mss() as sct:
        img = np.array(sct.grab(monitor))
        pixels = consts.get_field_from_screen(img)

        next_piece = get_figure_by_color(consts.get_next(img))
        # all empty initially
        field = np.zeros((20 + extra_rows, 10))
        # find middles of grid cells
        cell_size = pixels.shape[1] // 10
        vertical_centers = np.array(np.linspace(cell_size // 2, pixels.shape[0] + cell_size // 2, 21 + extra_rows)[:-1], int)
        horizontal_centers = np.array(np.linspace(cell_size // 2, pixels.shape[1] + cell_size // 2, 11)[:-1], int)
        # go through all cell centers
        for i, v in enumerate(vertical_centers):
            for j, h in enumerate(horizontal_centers):
                if pixels[v][h] == 1:
                    # check a nearby pixel to ensure its not a snowflake or a star
                    if pixels[v+5][h+5] == 1:
                        field[i][j] = 1
        return field, next_piece
