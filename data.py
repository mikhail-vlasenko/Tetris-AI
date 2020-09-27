import numpy as np


class Consts:
    """константы для кАсТоМиЗаЦиИ"""

    def __init__(self, top, bottom, left, right, next_top, next_bottom, next_left, next_right):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.next_top = next_top
        self.next_bottom = next_bottom
        self.next_left = next_left
        self.next_right = next_right

    def get_field_from_screen(self, img):
        field = img[self.top:self.bottom, self.left:self.right]
        field0 = np.array(field[:, :, 0] < 130, int)  # blue
        field1 = np.array(field[:, :, 1] < 100, int)  # green
        field2 = np.array(field[:, :, 2] < 90, int)  # red
        field_white0 = np.array(field[:, :, 0] > 200, int)
        field_white1 = np.array(field[:, :, 1] > 200, int)
        field_white2 = np.array(field[:, :, 2] > 200, int)
        field_white = field_white0 * field_white1 * field_white2
        field = field0 * field1 * field2 + field_white
        field = 1 - field
        return field

    def get_next_3(self, img):
        n3xt = img[self.next_top:self.next_bottom, self.next_left:self.next_right]
        next1 = n3xt[30:75]  # TODO разделение на нормальные части
        next2 = n3xt[90:135]
        next3 = n3xt[150:195]
        return next1, next2, next3


misha = Consts(370, 970, 155, 455, 340, 540, 485, 560)
alex = Consts(339, 895, 142, 422, 315, 505, 450, 475)
alex_notebook = Consts(225, 888, 115, 441, 315, 505, 450, 475)
maxx = Consts(370, 970, 155, 455, 340, 540, 485, 560)
