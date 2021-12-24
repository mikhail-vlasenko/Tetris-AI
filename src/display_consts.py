class DisplayConsts:
    """
    Stores key pixel positions to retrieve correct portions of the screen.
    Should be set for each user separately.
    """
    def __init__(self, top, bottom, left, right, next_top, next_bottom, next_left, next_right, extra_rows=-1):
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

        # tetr io spawns the new piece 2 grid cells above the main field
        # set this to vertical position of the highest 'spawning cell'
        if extra_rows == -1:
            self.extra_rows = self.top
        else:
            self.extra_rows = extra_rows

    def get_field_from_screen(self, img):
        return img[self.extra_rows:self.bottom, self.left:self.right]

    def get_next(self, img):
        return img[self.next_top:self.next_bottom, self.next_left:self.next_right]
