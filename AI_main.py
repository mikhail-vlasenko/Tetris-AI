from find_landings import all_landings
import numpy as np
from direct_keys import *
from copy import deepcopy
import time

FIELD_SIZE = [20, 10]


class AI:
    def __init__(self):
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
        tops = [100]*10
        blank_cnt = 0
        blank_depth = 0
        for i in range(len(field)):
            for j in range(FIELD_SIZE[1]):
                if field[i][j] and tops[j] == 100:
                    tops[j] = i
                elif not field[i][j] and tops[j] != 100:
                    blank_cnt += 1
                    blank_depth += i - tops[j] - 1
        return blank_cnt, 17 - min(tops), tops, blank_depth

    @staticmethod
    def almost_full_line(field):
        score = 0
        for i in range(len(field)):
            if sum(field[i]) == 9:
                score += 1
            if sum(field[i]) == 8:
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
        for i in range(len(field)-1, -1, -1):
            if curr_pit == -1 and gap_idx[i] != -1 and tops[gap_idx[i]] > i:
                curr_pit = gap_idx[i]
                pit_height += 1
            elif gap_idx[i] == curr_pit and curr_pit != -1:
                pit_height += 1
            elif curr_pit != -1:
                break
        return pit_height

    def get_score(self, field):
        """
        tells how good a position is
        :param field:
        :return:
        """
        field = field.tolist()
        score = 100

        clear = self.clear_line(field)
        field = clear[0]
        score += clear[1]
        if clear[1] >= 4:
            score += 20

        roofs = self.find_roofs(field)
        score -= roofs[0] * 5
        score -= roofs[3]
        score -= round(roofs[1] ** 1.4, 2)
        if self.scared:
            score -= round(roofs[1] ** 2, 2)
        score += self.almost_full_line(field)

        if self.line_held and not self.scared:
            pit_height = self.find_pit(field, roofs[2])
            score += 5*pit_height
            if pit_height >= 4:
                print('opportunity for a full pit')
        return score

    def calc_best(self, field, piece_idx):
        results = all_landings(field[3:], piece_idx)
        for i in range(len(results)):
            results[i].append(self.get_score(deepcopy(results[i][0])))
        results.sort(key=lambda x: x[3], reverse=True)
        return results

    def choose_action(self, field, piece_idx):
        """
        finds the best action to take
        :param field:
        :param piece_idx:
        :return: [rotation, x_pos, max_score]
        """
        if self.find_roofs(field[3:].tolist())[1] >= 13:
            self.scared = True
            print('scared')
        else:
            self.scared = False
        print(self.find_pit(field[3:].tolist(), self.find_roofs(field[3:].tolist())[2]))
        if self.find_pit(field[3:].tolist(), self.find_roofs(field[3:].tolist())[2]) >= 4:
            print('FULL PIT FOUND!!')
            if self.line_held:
                piece_idx = self.hold_piece(piece_idx)
        elif piece_idx == 0 and not self.line_held and not self.scared:
            piece_idx = self.hold_piece(piece_idx)

        results = self.calc_best(field, piece_idx)
        if not self.line_held or self.scared:
            results_held = self.calc_best(field, self.held_piece)
            if results_held[0][3] > results[0][3]:
                self.hold_piece(piece_idx)
                return results_held[0][1], results_held[0][2], results_held[0][3]

        return results[0][1], results[0][2], results[0][3]

    def place_piece(self, rotation, x_pos):
        for i in range(rotation):
            click_key(rotate_k)
        move = x_pos - 3  # 3 is the starting position
        for i in range(abs(move)):
            if move > 0:
                click_key(mv_right)
            else:
                click_key(mv_left)
        if time.time() - self.start_time < 240:
            if time.time() - self.start_time < 120:
                click_key(mv_down)
            click_key(mv_down)
            click_key(place_k)
            time.sleep(0.4)
