from copy import deepcopy
from position import Position
from figures import array_of_figures as pieces


def check_collision(field, piece, piece_pos, piece_idx):
    r = 4
    if piece_idx != 0:
        r -= 1
    for i in range(r):
        for j in range(r):
            if piece[i][j]:
                if (i + piece_pos[0] >= len(field)) or (j + piece_pos[1] >= len(field[0])) or (i + piece_pos[0] < 0) or\
                        (j + piece_pos[1] < 0) or field[i + piece_pos[0]][j + piece_pos[1]]:
                    return True
    return False


def land(field, piece, pos_now, piece_idx):
    res = deepcopy(field)
    while not check_collision(res, piece, pos_now, piece_idx):
        pos_now[0] += 1
    if pos_now[0] == 0:
        return None
    pos_now[0] -= 1
    for i in range(4):
        for j in range(4):
            if i + pos_now[0] < len(field) and j + pos_now[1] < len(field[0]):
                res[i + pos_now[0]][j + pos_now[1]] += piece[i][j]
    return res


def all_landings(field, piece_index):
    """
    calculates all possible results
    :param field:
    :param piece_index:
    :return: Position
    """
    results = []
    for rotation in range(len(pieces[piece_index])):
        for x_pos in range(-3, 10):
            res = land(field, pieces[piece_index][rotation], [0, x_pos], piece_index)
            if res is not None:
                results.append(Position(res, rotation, x_pos, piece_index))
    return results
