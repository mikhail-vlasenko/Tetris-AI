# pieces are encoded as
# 0 - line, 1 - square, 2 - T(flip), 3 - |__, 4 - __|, 5 - -|_,6 - _|-
from src.data import Consts

PIECE_NAMES = ['line', 'square', 'T(flip)', '|__', '__|', '-|_', '_|-']


def name_piece(piece: int) -> str:
    return PIECE_NAMES[piece]


# in BGR
original_colors = [(0, 0, 0) for _ in range(7)]
original_colors[0] = (230, 228, 180)
original_colors[1] = (182, 228, 247)
original_colors[2] = (177, 99, 140)
original_colors[3] = (228, 177, 148)
original_colors[4] = (128, 180, 235)
original_colors[5] = (180, 161, 235)
original_colors[6] = (171, 240, 177)

# tetr.io colors in RGB
tetrio_colors = [(0, 0, 0) for _ in range(7)]
tetrio_colors[0] = (36, 214, 150)
tetrio_colors[1] = (210, 171, 42)
tetrio_colors[2] = (212, 67, 195)
tetrio_colors[3] = (70, 56, 200)
tetrio_colors[4] = (217, 96, 48)
tetrio_colors[5] = (222, 44, 63)
tetrio_colors[6] = (131, 210, 42)

# important pixels for screen recognition
misha = Consts(370, 970, 155, 455, 340, 540, 485, 560)
alex = Consts(339, 895, 142, 422, 315, 505, 450, 475)
alex_notebook = Consts(225, 888, 115, 441, 315, 505, 450, 475)
maxx = Consts(370, 970, 155, 455, 340, 540, 485, 560)
tetrio_default = Consts(279, 1203, 1046, 1512, 370, 420, 1640, 1710, 180)

CONFIG = {
    'playing field size': [20, 10],
    'piece colors': tetrio_colors,
    'consts': tetrio_default,
    'extra rows': 2,  # in some Tetrises (tetr.io) pieces spawn above the main field
    'debug status': 0,
    'key press delay': 0.03,  # increase if facing misclicks, decrease to go faster
    'screen width': 2560,
    'screen height': 1440,
    'play safe': False,  # ai is even more robust
}
