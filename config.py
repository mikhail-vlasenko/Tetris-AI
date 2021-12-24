# pieces are encoded as
# 0 - line, 1 - square, 2 - T(flip), 3 - |__, 4 - __|, 5 - -|_,6 - _|-
from src.display_consts import DisplayConsts

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

# set important pixels for screen recognition
misha = DisplayConsts(370, 970, 155, 455, 340, 540, 485, 560)
alex = DisplayConsts(339, 895, 142, 422, 315, 505, 450, 475)
alex_notebook = DisplayConsts(225, 888, 115, 441, 315, 505, 450, 475)
maxx = DisplayConsts(370, 970, 155, 455, 340, 540, 485, 560)

tetrio_default = DisplayConsts(279, 1203, 1046, 1512, 370, 420, 1640, 1710, 180)

# -------------------------------- ACTION REQUIRED --------------------------------
# add yours and change 'display consts' in CONFIG
# to easily find these pixel positions, take a screenshot and paste it into paint or something
# then hover your mouse to the location and read the coordinates

# my_consts = DisplayConsts()


CONFIG = {
    # ---------- per run ----------
    'debug status': 1,  # greater is more information, 0 is none
    'key press delay': 0.02,  # increase if facing misclicks, decrease to go faster
    'tetrio garbage': True,
    'starting choices for 2nd': 3,
    # if true, looks at another frame to check for correct piece placement
    # reduces speed, improves robustness
    'confirm placement': True,
    'play safe': False,  # ai is even more robust
    'play for survival': False,  # if true, starts in 'cleaning' mode
    'override delay': False,  # if true, hard places all pieces even when scared

    # ---------- per user ----------
    'display consts': tetrio_default,
    'screen width': 2560,
    'screen height': 1440,

    # ---------- per game ----------
    'game': 'tetr.io',
    'playing field size': [20, 10],
    'piece colors': tetrio_colors,
    'extra rows': 2,  # in some Tetrises (tetr.io) pieces spawn above the main field

    # ---------- other ----------
    'gave warning': False,
}


def configure_fast():
    CONFIG['starting choices for 2nd'] = 1
    CONFIG['confirm placement'] = False
    CONFIG['play for survival'] = True
    CONFIG['override delay'] = True


# call to use the pre-set
configure_fast()
