import time

from config import CONFIG, name_piece
from scan_field import get_field
from src.figures import type_figure_ext
from src.AI_main import AI
import numpy as np


def main():
    can_hold_flag = True
    expected_rwd = 0
    ai = AI()
    position = None

    # call jit-compiling functions to compile them
    ai.calc_best(np.zeros((20, 10), dtype=np.int), 0)
    field, _ = get_field()
    print("Compilation complete")

    # infinite playing cycle
    while True:
        # get playing grid and the next piece
        field, next_piece = get_field()
        # parse current tetris piece
        piece_idx = type_figure_ext(field[:5])
        if piece_idx is None:
            if not CONFIG['gave warning']:
                print('\nTetris piece is not found.\n'
                      'Are you sure you have set your DisplayConsts in config.py?\n')
                CONFIG['gave warning'] = True
            continue

        # hold if nothing is held
        if ai.held_piece == -1:
            ai.hold_piece(piece_idx)
            can_hold_flag = False
            continue

        # shenanigans for better parsing of the original game
        if CONFIG['game'] == 'original':
            if position is not None and position.expect_tetris:
                # hoping that it was not a misclick, not taking a screenshot because TETRIS blocks the view
                field = np.zeros((3, 10), dtype=np.int)
                field = np.concatenate((field, ai.clear_line(position.field)[0]))
                time.sleep(0.2)
            elif not ai.scared:
                field, next_piece = get_field()

        # check held keys for runtime AI tuning
        ai.runtime_tuning()

        # check if the result is expected
        actual_score = ai.get_score(field[3:])[0]
        if CONFIG['debug status'] >= 1:
            if expected_rwd != actual_score:
                print('\nit was a misclick\n')
            if CONFIG['debug status'] >= 2:
                print(field)
            print(f'current score {actual_score}')

        # next piece is not recognized
        if next_piece == -1:
            if CONFIG['debug status'] >= 1:
                print("unknown next")
            next_piece = 1  # assume square as it is the most neutral one

        calc_start_time = time.time()
        # compute best outcome
        position = ai.choose_action_depth2(field[3:], piece_idx, next_piece, can_hold_flag)

        if CONFIG['debug status'] >= 1:
            # print useful info
            print('calculation took', time.time() - calc_start_time)
            print(f'chosen placement for {name_piece(position.piece)}: '
                  f'({position.rotation}, {position.x_pos}) with score {position.score}')
            print(f'next figure {name_piece(next_piece)} should give {position.next_score}')
            if position.expect_tetris:
                print('expecting TETRIS')

        expected_rwd = ai.get_score(ai.clear_line(position.field)[0])[0]
        # emulate key presses to place the piece
        ai.place_piece(position.piece, position.rotation, position.x_pos, ai.find_roofs(position.field)[1])
        # wait for everything to settle down
        ai.place_piece_delay()

        can_hold_flag = True
        if CONFIG['debug status'] >= 1:
            print()


if __name__ == '__main__':
    time.sleep(1)
    main()
