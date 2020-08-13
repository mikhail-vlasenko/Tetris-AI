from find_landings import all_landings
import numpy as np
from direct_keys import *
from copy import deepcopy
import time
from figures import piece_weight

FIELD_SIZE = [20, 10]


class AI:
    def __init__(self, try_tetris):
        self.try_tetris = try_tetris
        self.start_time = time.time()
        self.held_piece = -1
        self.line_held = False
        self.scared = False

    def hold_piece(self, piece_idx):
        click_key(hold)
        print(f'piece {piece_idx} held')
        piece_idx, self.held_piece = self.held_piece, piece_idx
        if self.held_piece == 0:
            self.line_held = True
        else:
            self.line_held = False
        return piece_idx

    @staticmethod
    def clear_line(field):
        """
        counts and clears full lines
        :param field:
        :return: field
        """
        full_cnt = 0
        i = 0
        while i < len(field):
            if all(field[i]) == 1:
                full_cnt += 1
                del field[i]
                field.insert(0, [0]*FIELD_SIZE[1])
            else:
                i += 1
        return field, full_cnt

    @staticmethod
    def find_roofs(field):
        """
        finds blank squares under landed pieces
        :param field:
        :return:
        """
        tops = np.zeros((10, 2))
        blank_cnt = 0
        blank_depth = 0
        for i in range(len(field)):
            for j in range(FIELD_SIZE[1]):
                if field[i][j]:
                    if tops[j][0] == 0:
                        tops[j][0] = 17 - i
                    tops[j][1] += 1
                elif not field[i][j] and tops[j][0] != 0:
                    blank_cnt += 1
                    blank_depth += tops[j][1] - 1
        return blank_cnt, np.max(tops[:, 0]), tops[:, 0], blank_depth

    @staticmethod
    def almost_full_line(field):
        score = 0
        for i in range(len(field)):
            if sum(field[i]) == 9:
                score += 2
            if sum(field[i]) == 8:
                score += 1
            if sum(field[i]) == 7:
                score += 0.5
        return score

    @staticmethod
    def find_pit(field, tops):
        gap_idx = []
        for i in range(len(field)):
            if sum(field[i]) == 9:
                gap_idx.append(field[i].index(0))
            else:
                gap_idx.append(-1)
        curr_pit = -1
        pit_height = 0
        max_pit_h = 0
        for i in range(len(field)-1, -1, -1):
            if gap_idx[i] != -1 and curr_pit != gap_idx and tops[gap_idx[i]] < i:
                if max_pit_h < pit_height:
                    max_pit_h = pit_height
                curr_pit = gap_idx[i]
                pit_height += 1
            elif gap_idx[i] == curr_pit and curr_pit != -1:
                pit_height += 1
        if max_pit_h < pit_height:
            max_pit_h = pit_height
        return max_pit_h

    @staticmethod
    def find_hole(tops):
        cnt_hole = 0
        np.insert(tops, 0, 100)
        tops[-1] = 100  # not using last column, so lets say its high
        for i in range(1, len(tops)):
            if tops[i - 1] - 2 > tops[i] and tops[i] < tops[i + 1] - 2:
                cnt_hole += 1
            if tops[i - 1] - 4 > tops[i] and tops[i] < tops[i + 1] - 4:
                cnt_hole += 1
        return cnt_hole

    def get_score(self, field, verbose=False):
        """
        tells how good a position is
        :param field:
        :return:
        """
        expect_tetris = False
        field = field.tolist()
        score = 0
        clear = self.clear_line(field)
        field = clear[0]
        roofs = self.find_roofs(field)
        if self.scared:
            score += 10 * clear[1]
            score -= roofs[0] * 3  # blank spaces
            score -= roofs[3]
            score -= 3 * roofs[1]
            score += self.almost_full_line(field)
            if clear[1] >= 4:
                score += 100
                expect_tetris = True
            return score, expect_tetris

        score -= roofs[0] * 10  # blank spaces
        score -= roofs[3] * 3
        score += self.almost_full_line(field)
        if roofs[2][9] != 0:
            score -= 10  # the most right column should be empty
            score -= roofs[2][9]
        if clear[1] >= 4:
            score += 1000
            expect_tetris = True
        score -= self.find_hole(roofs[2]) * 10
        pit_height = self.find_pit(field, roofs[2])
        score += 5 * pit_height
        if verbose:
            print(clear[1])
            print(roofs)
            print('holes', self.find_hole(roofs[2]))
            print('pit', pit_height)
            print('score', score)
        return score, expect_tetris

    def calc_best(self, field, piece_idx):
        results = all_landings(field[3:], piece_idx)
        for i in range(len(results)):
            results[i].append(self.get_score(deepcopy(results[i][0])))
        results.sort(key=lambda x: x[3][0], reverse=True)
        return results

    def choose_action(self, field, piece_idx, can_hold):
        """
        finds the best action to take
        :param field:
        :param piece_idx:
        :return: [rotation, x_pos, max_score]
        """
        if self.find_roofs(field[3:].tolist())[1] >= 14:
            self.scared = True
            print('scared')
        else:
            self.scared = False
        print(self.find_pit(field[3:].tolist(), self.find_roofs(field[3:].tolist())[2]))

        results = self.calc_best(field, piece_idx)
        results_held = self.calc_best(field, self.held_piece)
        if (results_held[0][3][0] + piece_weight(self.held_piece)) > (results[0][3][0] + piece_weight(piece_idx)) \
                and can_hold:
            piece_idx = self.hold_piece(piece_idx)
            return results_held[0][1], results_held[0][2], results_held[0][3][0], results_held[0][3][1], piece_idx

        return results[0][1], results[0][2], results[0][3][0], results[0][3][1], piece_idx

    def place_piece(self, rotation, x_pos):
        if rotation < 3:
            for i in range(rotation):
                click_key(rotate_k)
        else:
            click_key(rot_counterclock)
        move = x_pos - 3  # 3 is the starting position
        for i in range(abs(move)):
            if move > 0:
                click_key(mv_right)
            else:
                click_key(mv_left)
        if time.time() - self.start_time < 200 and not self.scared:
            if time.time() - self.start_time < 120:
                click_key(mv_down)
            click_key(mv_down)
            click_key(place_k)
            time.sleep(0.4)
        else:
            click_key(mv_down)
