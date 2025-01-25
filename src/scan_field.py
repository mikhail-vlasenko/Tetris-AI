from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
from mss import mss
from numba import jit

from config import CONFIG
from src.display_interacive_setup import InteractiveSetup

screen_capture = mss()
piece_colors = CONFIG['piece colors']


def simplified(pixels: np.array) -> np.array:
    """
    create a 2d array with 1 on position of a piece pixel and 0 on empty pixel
    :param pixels: pixels from screen in BGR
    :return: field of shape (pixels.shape[0], pixels.shape[1]) with 1 if this pixel has a piece
    """
    dark_boundary = [130, 100, 90]
    if CONFIG['tetrio garbage']:
        # lower dark excluded boundary for garbage
        dark_boundary = [70, 60, 60]
    field0 = np.array(pixels[:, :, 0] < dark_boundary[0], int)  # blue
    field1 = np.array(pixels[:, :, 1] < dark_boundary[1], int)  # green
    field2 = np.array(pixels[:, :, 2] < dark_boundary[2], int)  # red
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


@jit(nopython=True)
def cmp_pixel(pixels, color):
    return np.abs(pixels[:, 0] - color[2]) + \
           np.abs(pixels[:, 1] - color[1]) + \
           np.abs(pixels[:, 2] - color[0])


def get_figure_by_color(screen: np.array):
    pixels = screen[:, :, :3].reshape(-1, 3).astype(int)
    distances = np.zeros((len(piece_colors), len(pixels)), dtype=int)

    for i in range(len(piece_colors)):
        distances[i] = cmp_pixel(pixels, piece_colors[i])

    min_distances = np.min(distances, axis=1)  # shape (len(piece_colors),)
    if np.min(min_distances) < 30:
        return np.argmin(min_distances)
    return -1


def get_field(interactive_setup: Optional[InteractiveSetup] = None) -> (np.array, int):
    """
    takes a screenshot and computes playing grid
    :return: field grid, next piece id
    """
    img = np.array(screen_capture.grab(CONFIG['display consts'].get_screen_bounds()))
    field_img = CONFIG['display consts'].get_field_from_screen(img)
    pixels = simplified(field_img)
    next_img = CONFIG['display consts'].get_next(img)
    next_piece = get_figure_by_color(next_img)

    if interactive_setup is not None:
        interactive_setup.render_frame(field_img, pixels, next_img, next_piece)

    # all empty initially
    field = np.zeros((20 + CONFIG['extra rows'], 10))
    # find middles of grid cells
    cell_size = pixels.shape[1] // 10
    vertical_centers = np.array(np.linspace(cell_size // 2, pixels.shape[0] + cell_size // 2, 21 + CONFIG['extra rows'])[:-1], int)
    if vertical_centers[-1] > pixels.shape[0]:
        print("Width to height ratio is not close to 1:2, so the cell size is not correct")
        return field, next_piece
    horizontal_centers = np.array(np.linspace(cell_size // 2, pixels.shape[1] + cell_size // 2, 11)[:-1], int)

    offsets_to_check = []
    steps = [-cell_size//3, 0, cell_size//3]
    nearby = np.zeros((len(steps)**2))
    for v_offset in steps:
        for h_offset in steps:
            offsets_to_check.append((v_offset, h_offset))
    # go through all cell centers
    for i, v in enumerate(vertical_centers):
        for j, h in enumerate(horizontal_centers):
            for k, (v_offset, h_offset) in enumerate(offsets_to_check):
                nearby[k] = pixels[v + v_offset][h + h_offset]
            if np.mean(nearby) > 0.75:
                field[i][j] = 1
                if CONFIG['print piece color'] and i < 3:
                    piece_bgr = field_img[v][h][:3].astype(dtype=int)
                    print(f'RGB color of the new piece: '
                          f'({piece_bgr[2]}, {piece_bgr[1]}, {piece_bgr[0]})')
    return field, next_piece
