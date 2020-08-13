import time
from copy import deepcopy
from digit import get_field
from figures import type_of_figure
from AI_main import choose_action, place_piece
from direct_keys import click_key, hold


def main():
    held_piece = -1
    while True:
        field = get_field()
        piece_idx = type_of_figure(field)
        if piece_idx is None:
            piece_idx = type_of_figure(field[1:])
            if piece_idx is None:
                continue
        if held_piece == -1:
            click_key(hold)
            held_piece = piece_idx
            print(f'piece {piece_idx} held')
            continue
        field = get_field()
        placement = choose_action(field, piece_idx)
        placement_held = choose_action(field, held_piece)
        if placement_held[2] > placement[2]:
            click_key(hold)
            print(f'piece {piece_idx} held')
            piece_idx, held_piece = held_piece, piece_idx
            placement = deepcopy(placement_held)
        print(field)
        print(f'chosen placement for figure {piece_idx}, ({placement[0]}, {placement[1]}) with score {placement[2]}')
        place_piece(placement[0], placement[1])


if __name__ == '__main__':
    time.sleep(2)
    main()
