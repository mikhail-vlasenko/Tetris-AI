import matplotlib.pyplot as plt
import numpy as np
from PIL import ImageGrab
from mss import mss

dbug = 0

d = dict()
d[0] = (230, 228, 180)
d[1] = (182, 228, 247)
d[2] = (177, 99, 140)
d[3] = (228, 177, 148)
d[4] = (128, 180, 235)
d[5] = (180, 161, 235)
d[6] = (171, 240, 177)
d[7] = (96, 45, 36)


def pD(arr, fsize=10):
    if dbug == 1:
        n = len(arr)
        # print(n)
        fig = plt.figure(figsize=(fsize, fsize))
        for i in range(n):
            fig.add_subplot(1, n, i + 1)
            plt.imshow(arr[i])
    else:
        pass


def cmp_pixel(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2])


def get_figur(next_figure):
    # pD((next_figure,), 5)
    next_figure = next_figure[20:25, 15:20]
    # pD((next_figure,))
    for i in range(5):
        for j in range(5):
            p = next_figure[i, j][:3]
            for k in range(7):
                res = cmp_pixel(d[k], p)
                # print(i, j, k, res)
                if res < 15:
                    return k
    return -1


def get_next_3(img):
    n3xt = img[315:505, 450:475]
    next1 = n3xt[30:75]
    next2 = n3xt[90:135]
    next3 = n3xt[145:190]
    # pD((img, n3xt, next1, next2, next3))
    return get_figur(next1), get_figur(next2), get_figur(next3)


def get_field():
    index_color = 1
    # img = np.array(ImageGrab.grab())[:1000, :550][:, :, index_color]  # CUSTOM
    monitor = {"left": 0, "top": 0, "width": 550, "height": 1000}
    with mss() as sct:
        img = np.array(sct.grab(monitor))[:, :, index_color]
        field = img[370:970, 155:455]  # CUSTOM
        field_old = field
        field = np.array(field != [12, 26, 73][index_color], int)
        # pD((img, field_old, field))
        a, b, c = get_next_3(img)
        print(a, b, c)

        sizeCell = field.shape[0] // 20
        arr = np.zeros((20, 10))
        iters = sizeCell
        for i in range(0, iters):
            arr += field[i::sizeCell, i::sizeCell][:20, :10]

        kek = np.array(arr / iters + 0.5, int)
        pD((kek, field, field_old))
        return kek


def clear_grey_squares(field):
    flag = False
    for i in range(len(field) - 1, -1, -1):
        if np.sum(field[i]) == 10 or flag:
            field[i] = np.zeros(10)
            flag = True
    return field
