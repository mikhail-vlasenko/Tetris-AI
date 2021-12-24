import numpy as np


class Consts:
    """константы для кАсТоМиЗаЦиИ"""

    def __init__(self, top, bottom, left, right, next_top, next_bottom, next_left, next_right, extra_rows=-1):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.next_top = next_top
        self.next_bottom = next_bottom
        self.next_left = next_left
        self.next_right = next_right
        if extra_rows == -1:
            self.extra_rows = self.top
        else:
            self.extra_rows = extra_rows

    def get_field_from_screen(self, img):
        field = img[self.extra_rows:self.bottom, self.left:self.right]
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

    def get_next(self, img):
        return img[self.next_top:self.next_bottom, self.next_left:self.next_right]
