import time
from digit import get_field
from figures import type_of_figure
from AI_main import choose_action, place_piece


def main():
    while True:
        field = get_field()
        piece_idx = type_of_figure(field)
        if piece_idx is None:
            time.sleep(0.05)
            continue
        placement = choose_action(field, piece_idx)
        place_piece(placement[0], placement[1])
        time.sleep(0.1)


if __name__ == '__main__':
    time.sleep(3)
    main()
