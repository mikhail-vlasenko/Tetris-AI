import matplotlib.pyplot as plt
import numpy as np
from PIL import ImageGrab

dbug = 0


def pD(arr):
    if dbug == 1:
        n = len(arr)
        # print(n)
        fig = plt.figure(figsize=(10, 10))
        for i in range(n):
            fig.add_subplot(1, n, i + 1)
            plt.imshow(arr[i])
    else:
        pass


def get_field():
    index_color = 1
    img = np.array(ImageGrab.grab())[:1000, :550][:, :, index_color]  # CUSTOM
    field = img[342:895, 130:408]  # CUSTOM
    field_old = field
    field = np.array(field != [12, 26, 73][index_color], int)
    pD((img, field_old, field))

    sizeCell = field.shape[0] // 20
    arr = np.zeros((20, 10))
    iters = sizeCell + 1
    for i in range(0, iters):
        arr += field[i::sizeCell, i::sizeCell][:20, :10]

    kek = np.array(arr / iters + 0.5, int)
    pD((kek, field, field_old))
    if dbug:
        print(kek)
