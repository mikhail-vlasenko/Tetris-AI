class DisplayConsts:
    """
    Stores key pixel positions to retrieve correct portions of the screen.
    Should be set for each user separately.
    """
    def __init__(self, top, bottom, left, right, next_top, next_bottom, next_left, next_right, num_extra_rows=0):
        # corners of the playing grid (only of those 20x10 cells)
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

        # small portion of the screen where the next piece is
        # no need to include the whole piece
        self.next_top = next_top
        self.next_bottom = next_bottom
        self.next_left = next_left
        self.next_right = next_right

        self.num_extra_rows = num_extra_rows

        self.update()

    def update(self):
        row_height = (self.bottom - self.top) // 20
        self.extra_rows = self.top - self.num_extra_rows * row_height
        self.vertical_offset = min(self.extra_rows, self.next_top)
        self.horizontal_offset = min(self.left, self.next_left)

    def get_field_from_screen(self, img):
        return img[self.extra_rows-self.vertical_offset:self.bottom-self.vertical_offset,
                   self.left-self.horizontal_offset:self.right-self.horizontal_offset]

    def get_next(self, img):
        return img[self.next_top-self.vertical_offset:self.next_bottom-self.vertical_offset,
                   self.next_left-self.horizontal_offset:self.next_right-self.horizontal_offset]

    def get_screen_bounds(self):
        """
        Provides the box that has to be captured to get all necessary information
        """
        bottom = max(self.bottom, self.next_bottom)
        right = max(self.right, self.next_right)
        return {
            "left": self.horizontal_offset,
            "width": right - self.horizontal_offset,
            "top": self.vertical_offset,
            "height": bottom - self.vertical_offset
        }

    def __str__(self):
        return f"DisplayConsts(top={self.top}, bottom={self.bottom}, left={self.left}, right={self.right}, " \
                f"next_top={self.next_top}, next_bottom={self.next_bottom}, next_left={self.next_left}, " \
                f"next_right={self.next_right}, num_extra_rows={self.num_extra_rows})"
