import numpy as np
from src.display_consts import DisplayConsts


# pieces are encoded as
# 0 - line, 1 - square, 2 - T(flip), 3 - |__, 4 - __|, 5 - -|_,6 - _|-
PIECE_NAMES = ['line', 'square', 'T(flip)', '|__', '__|', '-|_', '_|-']


def name_piece(piece: int) -> str:
    return PIECE_NAMES[piece]


# in RGB
original_colors = np.zeros((7, 3), int)
original_colors[0] = (180, 228, 230)
original_colors[1] = (247, 228, 182)
original_colors[2] = (140, 99, 177)
original_colors[3] = (148, 177, 228)
original_colors[4] = (235, 180, 128)
original_colors[5] = (235, 161, 180)
original_colors[6] = (177, 240, 171)

# tetr.io colors in RGB
tetrio_colors = np.zeros((7, 3), int)
tetrio_colors[0] = (50, 179, 131)
tetrio_colors[1] = (179, 153, 49)
tetrio_colors[2] = (165, 63, 155)
tetrio_colors[3] = (80, 63, 166)
tetrio_colors[4] = (179, 99, 50)
tetrio_colors[5] = (181, 53, 60)
tetrio_colors[6] = (133, 181, 52)

# set important pixels for screen recognition
tetrio_default = DisplayConsts(top=465, bottom=1780, left=1590, right=2250,
                               next_top=600, next_bottom=635, next_left=2405, next_right=2535, num_extra_rows=2)


# -------------------------------- ACTION REQUIRED --------------------------------
# Add yours and change 'display consts' in CONFIG
# Set 'debug status' to 3 to inspect what the bot sees and adjust the values (opens 2 new windows)
# Alternatively, take a screenshot of the game and paste it into something like paint,
# then hover your mouse to the location and read the coordinates

# my_consts = DisplayConsts()


CONFIG = {
    # ---------- per run ----------
    'debug status': 1,  # greater is more information, 0 is none. 3 is for interactive setup mode
    # if true, bot prints the color of the piece when it is recognized.
    # it helps with setting up 'piece colors', but can be misleading because the tone of the current piece
    # may be different from the color of the piece in the next frame
    'print piece color': False,
    'key press delay': 0.02,  # increase if facing misclicks, decrease to go faster
    'tetrio garbage': True,
    'starting choices for 2nd': 8,
    # if true, looks at another frame to check for correct piece placement
    # reduces speed, increases robustness
    'confirm placement': True,
    'play safe': False,  # ai is even more robust
    'play for survival': False,  # if true, starts in 'cleaning' mode
    'override delay': False,  # if true, hard places all pieces even when scared

    # ---------- per user ----------
    'display consts': tetrio_default,
    'helper window size': '768x1536',

    # ---------- per game ----------
    'game': 'tetr.io',
    'playing field size': [20, 10],
    'piece colors': tetrio_colors,
    'extra rows': 2,  # in some Tetrises (tetr.io) pieces spawn above the main field

    # ---------- other ----------
    'gave warning': False,
}


def configure_fast():
    CONFIG['starting choices for 2nd'] = 8
    CONFIG['confirm placement'] = False
    CONFIG['play for survival'] = True
    CONFIG['override delay'] = True


# call to use the pre-set
configure_fast()

assert not (CONFIG['print piece color'] and CONFIG['confirm placement']), \
    'Disable "confirm placement" to avoid confusion with the color printout'
