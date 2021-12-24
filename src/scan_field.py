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


def simplified(pixels: np.array) -> np.array:
    """
    create a 2d array with 1 on position of a piece pixel and 0 on empty pixel
    :param pixels: pixels from screen in BGR
    :return: field of shape (pixels.shape[0], pixels.shape[1]) with 1 if this pixel has a piece
    """
    field0 = np.array(pixels[:, :, 0] < 130, int)  # blue
    field1 = np.array(pixels[:, :, 1] < 100, int)  # green
    field2 = np.array(pixels[:, :, 2] < 90, int)  # red
    # these are too dark on all colors to be a piece
    dark_pixels = field0 * field1 * field2

    field_white0 = np.array(pixels[:, :, 0] > 200, int)
    field_white1 = np.array(pixels[:, :, 1] > 200, int)
    field_white2 = np.array(pixels[:, :, 2] > 200, int)
    # these are too bright on all colors to be a piece
    white_pixels = field_white0 * field_white1 * field_white2

    # combine dark and bright to get all pixels that are NOT a tetris piece
    excluded_pixels = dark_pixels + white_pixels
    # make 1 where piece and 0 where empty
    field = 1 - excluded_pixels
    return field


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
        pixels = simplified(consts.get_field_from_screen(img))

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
