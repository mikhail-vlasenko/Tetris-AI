from find_landings import all_landings
import numpy as np
from direct_keys import *

FIELD_SIZE = [20, 10]


def clear_line(field):
    """
    counts and clears full lines
    :param field:
    :return: field
    """
    full_cnt = 0
    i = 0
    while i < len(field):
        if all(field[i]) == 1:
            full_cnt += 1
            del field[i]
            field.insert(0, [0]*FIELD_SIZE[1])
        else:
            i += 1
    return field, full_cnt


def find_roofs(field):
    """
    finds blank squares under landed pieces
    :param field:
    :return:
    """
    tops = [0]*10
    blank_cnt = 0
    for i in range(len(field)):
        for j in range(FIELD_SIZE[1]):
            if field[i][j] and not tops[j]:
                tops[j] = i
            elif not field[i][j] and tops[j]:
                blank_cnt += 1
    return blank_cnt, min(tops)


def get_score(field):
    """
    tells how good a position is
    :param field:
    :return:
    """
    field = field.tolist()[3:]
    score = 100

    clear = clear_line(field)
    field = clear[0]
    score += clear[1] ** 2

    roofs = find_roofs(field)
    score -= roofs[0] * 5
    score -= 20 - roofs[1]
    return score


def choose_action(field, piece_idx):
    """
    finds the best action to take
    :param field:
    :param piece_idx:
    :return: [rotation, x_pos]
    """
    results = all_landings(field, piece_idx)
    scores = []
    for r in results:
        scores.append(get_score(r[0]))
    scores = np.array(scores)
    return results[np.argmax(scores)][1], results[np.argmax(scores)][2]


def place_piece(rotation, x_pos):
    for i in range(rotation):
        click_key(rotate_k)
    move = x_pos - 3  # 3 is the starting position
    for i in range(abs(move)):
        if move > 0:
            click_key(mv_right)
        else:
            click_key(mv_left)
    click_key(place_k)
