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
        return img[self.extra_rows:self.bottom, self.left:self.right]

    def get_next(self, img):
        return img[self.next_top:self.next_bottom, self.next_left:self.next_right]
