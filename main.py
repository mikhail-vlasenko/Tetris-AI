import time
from copy import deepcopy
from digit import get_field
from figures import type_of_figure
from AI_main import AI


def main():
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
            continue
        field = get_field()
        placement = ai.choose_action(field, piece_idx)
        print(field)
        print(f'chosen placement for figure {piece_idx}, ({placement[0]}, {placement[1]}) with score {placement[2]}')
        ai.place_piece(placement[0], placement[1])


if __name__ == '__main__':
    time.sleep(2)
    main()
