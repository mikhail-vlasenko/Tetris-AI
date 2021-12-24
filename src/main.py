import time

from config import CONFIG, name_piece
from scan_field import get_field
from src.figures import type_figure_ext
from src.AI_main import AI
import numpy as np


def main():
    can_hold_flag = True
    expected_rwd = 0
    ai = AI(CONFIG['play safe'])
    placement = None
    while True:
        field, next_piece = get_field()
        piece_idx = type_figure_ext(field[:5])
        if piece_idx is None:
            continue
        if ai.held_piece == -1:
            ai.hold_piece(piece_idx)
            can_hold_flag = False
            time.sleep(0.2)
            continue
        if placement is not None and placement.expect_tetris:
            # hoping that it was not a misclick, not taking a screenshot because TETRIS blocks the view
            field = np.zeros((3, 10), dtype=np.int)
            field = np.concatenate((field, ai.clear_line(placement.field)[0]))
            time.sleep(0.2)
        elif not ai.scared:
            field, next_piece = get_field()
        ai.manual_speed_set()
        actual_score = ai.get_score(field[3:])[0]
        if expected_rwd != actual_score:
            print('\nit was a misclick\n')
        print(field)
        print(f'current score {actual_score}')
        if next_piece == -1:
            print("unknown next")
            next_piece = 1
        calc_start_time = time.time()
        placement = ai.choose_action_depth2(field[3:], piece_idx, next_piece, can_hold_flag)
        print('calculation took', time.time() - calc_start_time)
        print(f'chosen placement for {name_piece(placement.piece)}: '
              f'({placement.rotation}, {placement.x_pos}) with score {placement.score}')
        print(f'next figure {name_piece(next_piece)} should give {placement.next_score}')
        if placement.expect_tetris:
            print('expecting TETRIS')
        expected_rwd = ai.get_score(ai.clear_line(placement.field)[0])[0]
        ai.place_piece(placement.piece, placement.rotation, placement.x_pos, ai.find_roofs(placement.field)[1])
        ai.place_piece_delay(no_waiting=True)
        can_hold_flag = True


if __name__ == '__main__':
    time.sleep(2)
    main()