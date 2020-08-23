import matplotlib.pyplot as plt
import numpy as np
from mss import mss
import data

consts = data.alex  # CUSTOM
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
        fig = plt.figure(figsize=(fsize, fsize))
        for i in range(n):
            fig.add_subplot(1, n, i + 1)
            plt.imshow(arr[i])
    else:
        pass


def cmp_pixel(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2])


def get_figure(next_figure):
    next_figure = next_figure[15:25, 15:22]
    for i in range(len(next_figure)):
        for j in range(len(next_figure[0])):
            p = next_figure[i, j][:3]
            for k in range(7):
                res = cmp_pixel(d[k], p)
                if res < 15:
                    return k
    return -1


def get_field():
    monitor = {"left": 0, "top": 0, "width": 550, "height": 1000}
    with mss() as sct:
        img = np.array(sct.grab(monitor))
        field = consts.get_field_from_screen(img)

        next1, next2, next3 = map(get_figure, consts.get_next_3(img))

        sizeCell = field.shape[0] // 20
        arr = np.zeros((20, 10))
        for i in range(sizeCell):
            r1 = np.array(np.linspace(0, field.shape[0], 21)[:-1], int) + i
            r2 = np.array(np.linspace(0, field.shape[1], 11)[:-1], int) + i
            arr += field[r1][:, r2]

        kek = np.array(arr / sizeCell + 0.5, int)
        pD((img, field, kek))
        return kek, next1
