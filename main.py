import time
from copy import deepcopy
from digit import get_field
from figures import type_of_figure
from AI_main import AI


TRY_TETRIS = False


def main():
    can_hold_flag = True
    expected_rwd = 0
    ai = AI(try_tetris=TRY_TETRIS)
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
            time.sleep(0.5)
        field = get_field()
        if expected_rwd != ai.get_score(field[3:], verbose=True)[0]:
            print('\nit was a misclick\n')
        placement = ai.choose_action(field, piece_idx, can_hold_flag)
        print(field)
        print(f'chosen placement for figure {placement[4]}, ({placement[0]}, {placement[1]}) with score {placement[2]}')
        expected_rwd = placement[2]
        ai.place_piece(placement[0], placement[1])
        can_hold_flag = True


if __name__ == '__main__':
    time.sleep(2)
    main()
