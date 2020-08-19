import time
from copy import deepcopy
from digit import get_field
from figures import type_figure_ext
from AI_main import AI
import numpy as np
import cProfile


PLAY_SAFE = False


def main():
    can_hold_flag = True
    expected_rwd = 0
    ai = AI(PLAY_SAFE)
    while True:
        field = get_field()
        piece_idx = type_figure_ext(field[:5])
        if piece_idx is None:
            continue
        if ai.held_piece == -1:
            ai.hold_piece(piece_idx)
            can_hold_flag = False
            time.sleep(0.2)
            continue
        if 'placement' in locals() and placement.expect_tetris:
            # hoping that it was not a misclick, not taking a screenshot because TETRIS blocks the view
            field = np.zeros((3, 10), dtype=np.int)
            field = np.concatenate((field, ai.clear_line(placement.field)[0]))
            time.sleep(0.2)
        elif not ai.scared:
            field = get_field()
        print(field)
        ai.manual_speed_set()
        if expected_rwd != ai.get_score(field[3:], verbose=True)[0]:
            print('\nit was a misclick\n')
        placement = ai.choose_action(field, piece_idx, can_hold_flag)
        print(f'chosen placement for figure {placement.piece}, ({placement.rotation}, {placement.x_pos}) with score {placement.score}')
        if placement.expect_tetris:
            print('expecting TETRIS')
        expected_rwd = placement.score
        ai.place_piece(placement.piece, placement.rotation, placement.x_pos, ai.find_roofs(placement.field)[1])
        ai.place_piece_delay()
        can_hold_flag = True


if __name__ == '__main__':
    time.sleep(2)
    main()
