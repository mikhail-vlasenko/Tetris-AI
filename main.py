import time
from copy import deepcopy
from digit import get_field
from figures import type_of_figure
from AI_main import AI
import numpy as np


def main():
    can_hold_flag = True
    expected_rwd = 0
    ai = AI()
    while True:
        field = get_field()
        piece_idx = type_of_figure(field)
        if piece_idx is None:
            piece_idx = type_of_figure(field[1:])
            if piece_idx is None:
                continue
        if ai.held_piece == -1:
            ai.hold_piece(piece_idx)
            can_hold_flag = False
            time.sleep(0.2)
            continue
        if 'placement' in locals() and placement[3]:
            # hoping that it was not a misclick, not taking a screenshot because TETRIS block the view
            field = np.zeros((3, 10), dtype=np.int)
            field = np.concatenate((field, ai.clear_line(placement[4])[0]))
            time.sleep(0.2)
        else:
            field = get_field()
        print(field)
        if expected_rwd != ai.get_score(field[3:], verbose=True)[0]:
            print('\nit was a misclick\n')
        placement = ai.choose_action(field, piece_idx, can_hold_flag)
        print(f'chosen placement for figure {placement[5]}, ({placement[0]}, {placement[1]}) with score {placement[2]}')
        if placement[3]:
            print('expecting TETRIS')
        expected_rwd = placement[2]
        ai.place_piece(placement[5], placement[0], placement[1])
        ai.place_piece_delay()
        can_hold_flag = True


if __name__ == '__main__':
    time.sleep(2)
    main()
