import time
from copy import deepcopy
from digit import get_field
from figures import type_of_figure
from AI_main import choose_action, place_piece


def main():
    while True:
        field = get_field()
        piece_idx = type_of_figure(field)
        piece_idx2 = type_of_figure(field[1:])
        if piece_idx is None:
            piece_idx = deepcopy(piece_idx2)
            if piece_idx is None:
                continue
        field = get_field()
        placement = choose_action(field, piece_idx)
        print(field)
        print(f'chosen placement for figure {piece_idx}, {placement}')
        place_piece(placement[0], placement[1])
        time.sleep(0.4)


if __name__ == '__main__':
    time.sleep(3)
    main()
