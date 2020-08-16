import numpy as np

array_of_figures = np.array([
    [
        [[1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        [[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]],
        [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]],
        [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]]
    ],
    [
        [[0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        [[0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        [[0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        [[0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    ],
    [
        [[0, 1, 0, 0], [1, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        [[0, 1, 0, 0], [0, 1, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]],
        [[0, 0, 0, 0], [1, 1, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]],
        [[0, 1, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]]
    ],
    [
        [[1, 0, 0, 0], [1, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        [[0, 1, 1, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]],
        [[0, 0, 0, 0], [1, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0]],
        [[0, 1, 0, 0], [0, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0]]
    ],
    [
        [[0, 0, 1, 0], [1, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0]],
        [[0, 0, 0, 0], [1, 1, 1, 0], [1, 0, 0, 0], [0, 0, 0, 0]],
        [[1, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]]
    ],
    [
        [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        [[0, 0, 1, 0], [0, 1, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]],
        [[0, 0, 0, 0], [1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0]],
        [[0, 1, 0, 0], [1, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]]
    ],
    [
        [[0, 1, 1, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        [[0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0]],
        [[0, 0, 0, 0], [0, 1, 1, 0], [1, 1, 0, 0], [0, 0, 0, 0]],
        [[1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]]
    ]
])


# 0 - line, 1 - square, 2 - T(flip), 3 - |__, 4 - __|, 5 - -|_,6 - _|-
def type_of_figure(arr):
    figure = [[arr[0][3], arr[0][4], arr[0][5], arr[0][6]],
              [arr[1][3], arr[1][4], arr[1][5], arr[1][6]]]
    if figure == [[1, 1, 1, 1], [0, 0, 0, 0]]:
        return 0
    elif figure == [[0, 1, 1, 0], [0, 1, 1, 0]]:
        return 1
    elif figure == [[0, 1, 0, 0], [1, 1, 1, 0]]:
        return 2
    elif figure == [[1, 0, 0, 0], [1, 1, 1, 0]]:
        return 3
    elif figure == [[0, 0, 1, 0], [1, 1, 1, 0]]:
        return 4
    elif figure == [[1, 1, 0, 0], [0, 1, 1, 0]]:
        return 5
    elif figure == [[0, 1, 1, 0], [1, 1, 0, 0]]:
        return 6


def type_figure_ext(field):
    piece_idx = type_of_figure(field)
    if piece_idx is None:
        piece_idx = type_of_figure(field[1:])
        if piece_idx is None:
            piece_idx = type_of_figure(field[2:])
    return piece_idx


def piece_weight(figure):
    weights = [0, 8, 7, 7, 7, 10, 10]  # additional score
    return weights[figure]


def find_figure(field, figure, exp_x_pos, up_to):
    possible = []
    print(f'looking up to {up_to}')
    for rot in range(len(array_of_figures[figure])):
        for y_pos in range(up_to):
            for x_pos in range(exp_x_pos-3, exp_x_pos+4):
                flag = True
                for i in range(4):
                    for j in range(4):
                        if array_of_figures[figure][rot][i][j]:
                            if y_pos + i >= len(field) or x_pos + j >= len(field[0]) or y_pos + i < 0 or\
                                    x_pos + j < 0 or not field[y_pos + i][x_pos + j]:
                                flag = False
                if flag:
                    possible.append([rot, x_pos])
    return possible
