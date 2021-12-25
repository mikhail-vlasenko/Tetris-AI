from typing import List

from find_landings import all_landings
import numpy as np
from direct_keys import *
import time
from figures import piece_weight, find_figure
from scan_field import get_field
from config import CONFIG, name_piece
import keyboard

from src.position import Position


class AI:
    def __init__(self, play_safe):
        self.play_safe = play_safe
        self.start_time = time.time()
        self.speed = 1
        self.clearing = CONFIG['play for survival']
        self.held_piece = -1
        self.focus_blank = False
        self.scared = False
        self.choices_for_2nd = CONFIG['starting choices for 2nd']

    def hold_piece(self, piece_idx):
        click_key(hold)
        if CONFIG['debug status'] >= 1:
            print(f'{name_piece(piece_idx)} held, {name_piece(self.held_piece)} released')
        piece_idx, self.held_piece = self.held_piece, piece_idx
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
            if np.sum(field[i]) == CONFIG['playing field size'][1]:
                full_cnt += 1
                field = np.delete(field, i, axis=0)
                field = np.insert(field, 0, np.zeros(CONFIG['playing field size'][1]), axis=0)
            else:
                i += 1
        return field, full_cnt

    @staticmethod
    def find_roofs(field: np.array) -> (int, int, np.array, int):
        """
        finds blank squares under landed pieces
        :param field:
        :return: blank_cnt, height, [height of lines], blank_cumulative_depth
        """
        tops = np.zeros((10, 2))
        blank_cnt = 0
        blank_depth = 0
        for i in range(len(field)):
            for j in range(CONFIG['playing field size'][1]):
                if field[i][j]:
                    if tops[j][0] == 0:
                        tops[j][0] = 17 - i
                    tops[j][1] += 1
                elif not field[i][j] and tops[j][0] != 0:
                    blank_cnt += 1
                    blank_depth += tops[j][1] - 1
        return blank_cnt, int(np.max(tops[:, 0])), tops[:, 0], blank_depth

    @staticmethod
    def almost_full_line(field):
        score = 0
        for i in range(len(field)):
            ssum = np.sum(field[i])
            if ssum == 9:
                score += 2
            if ssum == 8:
                score += 1
            if ssum == 7:
                score += 0.5
        return score

    @staticmethod
    def find_pit(field, tops):
        gap_idx = []
        for i in range(len(field)):
            if np.sum(field[i]) == 9:
                gap_idx.append(np.where(field[i] == 0))
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
        tops = np.insert(tops, 0, 20)
        tops[-1] = 20  # not using last column, so lets say its high
        for i in range(1, len(tops) - 1):
            if tops[i - 1] - 2 > tops[i] and tops[i] < tops[i + 1] - 2:
                cnt_hole += 1
            if tops[i - 1] - 4 > tops[i] and tops[i] < tops[i + 1] - 4:
                cnt_hole += min(tops[i - 1] - 4 - tops[i], tops[i + 1] - 4 - tops[i])
        return cnt_hole

    def update_state(self, field):
        roofs = self.find_roofs(field)
        if roofs[1] >= 13 or self.speed == 3:
            self.scared = True
            if CONFIG['debug status'] >= 1:
                print('scared')
        else:
            self.scared = False
        if roofs[0] > 0:
            self.focus_blank = True
            if CONFIG['debug status'] >= 1:
                print('focusing blank')
        else:
            self.focus_blank = False
        return roofs

    def get_score(self, field, verbose=False):
        """
        tells how good a position is
        :param field:
        :param verbose: if True prints debug info
        :return:
        """
        expect_tetris = False
        score = 0
        clear = self.clear_line(field)
        cleared = clear[0]
        roofs = self.find_roofs(cleared)
        score += self.almost_full_line(cleared)
        if clear[1] >= 4:
            score += 1000
            expect_tetris = True
        if self.scared or self.clearing:
            score += 10 * clear[1]
            score -= roofs[0] * 3  # blank spaces
            score -= roofs[3]
            score -= 4 * roofs[1]
            return score, expect_tetris

        score -= roofs[0] * 10  # blank spaces
        score -= roofs[3] * 2
        if roofs[1] > 7:
            score -= roofs[1] ** 1.4
        score -= self.find_hole(roofs[2]) * 10
        if self.focus_blank:
            score -= roofs[3] * 3
            score += 5 * clear[1]
            return score, expect_tetris

        score -= 3 * clear[1]
        if roofs[2][9] != 0:
            score -= 10  # the most right column should be empty
            score -= roofs[2][9]
        pit_height = self.find_pit(cleared, roofs[2])
        # score += 5 * pit_height
        if verbose:
            print(cleared)
            print('lines cleared', clear[1])
            print(roofs)
            print('holes', self.find_hole(roofs[2]))
            print('pit', pit_height)
            print('score', score)
        return score, expect_tetris

    def calc_best(self, field: np.array, piece_idx: int) -> List[Position]:
        """
        chooses the best landing for a piece
        :param field:
        :param piece_idx:
        :return: sorted positions
        """
        results = all_landings(field, piece_idx)
        for i in range(len(results)):
            results[i].score, results[i].expect_tetris = self.get_score(results[i].field)
        results.sort(key=lambda x: x.score, reverse=True)
        return results

    def choose_action(self, field: np.array, piece_idx, can_hold) -> Position:
        """
        finds the best action to take in the situation
        :param field:
        :param piece_idx:
        :param can_hold: in the beginning it can't hold because it already held on this turn
        :return: Position
        """
        # set inner flags for reward function
        self.update_state(field)

        # compute best placement for current piece
        result = self.calc_best(field, piece_idx)[0]
        if can_hold:
            # for held
            result_held = self.calc_best(field, self.held_piece)[0]
            if (result_held.score + piece_weight(self.held_piece)) > \
                    (result.score + piece_weight(piece_idx)):
                self.hold_piece(piece_idx)
                return result_held

        return result

    def choose_action_depth2(self, field: np.array, piece_idx: int, next_piece: int, can_hold: bool) -> Position:
        if self.choices_for_2nd == 1:
            # can simplify
            return self.choose_action(field, piece_idx, can_hold)

        self.update_state(field)

        # top x best placements
        results = self.calc_best(field, piece_idx)[:self.choices_for_2nd]
        # for each of them find best next placement
        for i in range(len(results)):
            # clear full lines
            results[i].field = self.clear_line(results[i].field)[0]
            # compute best scores
            sub_score = self.calc_best(results[i].field, next_piece)[0].score
            sub_score_hold = self.calc_best(results[i].field, self.held_piece)[0].score
            # take best
            results[i].next_score = max(sub_score, sub_score_hold)
        # same for held piece
        if can_hold:
            results += self.calc_best(field, self.held_piece)[:self.choices_for_2nd]
            for i in range(self.choices_for_2nd, len(results)):
                results[i].field = self.clear_line(results[i].field)[0]
                sub_score = self.calc_best(results[i].field, next_piece)[0].score
                sub_score_hold = self.calc_best(results[i].field, piece_idx)[0].score
                results[i].next_score = max(sub_score, sub_score_hold)

        # sort by total score, prioritizing tetris on current turn
        # (not another move, and then tetris)
        results.sort(key=lambda x: x.next_score + x.score + 1000 * x.expect_tetris, reverse=True)
        if results[0].piece == self.held_piece and self.held_piece != piece_idx:
            self.hold_piece(piece_idx)
        return results[0]

    def place_piece(self, piece: int, rotation: int, x_pos: int, height: int, rot_now=0, x_pos_now=3, depth=0):
        if depth == 3:
            if CONFIG['debug status'] >= 1:
                print('depth 3 reached in place_piece')
            return
        rotate = (rotation - rot_now) % 4
        if rotate < 3:
            for i in range(rotate):
                click_key(rotate_k)
        else:
            click_key(rot_counterclock)
        move = x_pos - x_pos_now  # 3 is the starting position
        for i in range(abs(move)):
            if move > 0:
                click_key(mv_right)
            else:
                click_key(mv_left)

        # verify piece is placed where it should be
        if CONFIG['confirm placement']:
            time.sleep(0.09)
            field = get_field()[0]
            actual_pos = find_figure(field, piece, x_pos, max(0, 16 - height))
            if not actual_pos:
                if CONFIG['debug status'] >= 1:
                    print('piece not found')
            elif [rotation, x_pos] not in actual_pos:
                if CONFIG['debug status'] >= 1:
                    print(f'misclick spotted, position {actual_pos[0]}, should be {rotation, x_pos}')
                self.place_piece(piece, rotation, x_pos, height,
                                 rot_now=actual_pos[0][0], x_pos_now=actual_pos[0][1], depth=depth+1)
            else:
                if CONFIG['debug status'] >= 1:
                    print('all good')

    def place_piece_delay(self):
        if CONFIG['game'] == 'tetr.io':
            if (CONFIG['override delay'] or not self.scared) and self.speed == 1:
                click_key(place_k)
                time.sleep(0.05)  # just a little waiting for the piece to land fully
            elif not self.scared and self.speed == 2:
                press_key(mv_down)
                time.sleep(0.3)
                release_key(mv_down)

        elif CONFIG['game'] == 'original':
            if time.time() - self.start_time < 160 and not self.scared and not self.play_safe:
                if time.time() - self.start_time < 120:
                    click_key(mv_down)
                click_key(mv_down)
                click_key(place_k)
                time.sleep(0.45)
            elif time.time() - self.start_time < 300:
                press_key(mv_down)
                time.sleep(max(0., 0.5 - (time.time() - self.start_time) / 1000))
                release_key(mv_down)
        else:
            click_key(place_k)

    def runtime_tuning(self):
        """
        set speed modes:
        1 - for the slowest level, placing pieces fast
        2 - medium speed, no hard placing, turn on at level 6
        3 - for the late game, always scared
        control number of paths for the next piece:
        z, x, c - 1, 3, 5
        n - try to clean the field
        m - disable cleaning mode (try to get tetrises)

        This is only checked when a new piece appears, so you need to hold the key
        :return:
        """
        if keyboard.is_pressed('1'):
            self.start_time = time.time()
            self.speed = 1
        elif keyboard.is_pressed('2'):
            self.start_time = time.time() - 160
            self.speed = 2
        elif keyboard.is_pressed('3'):
            self.start_time = time.time() - 300
            self.speed = 3

        if keyboard.is_pressed('z'):
            self.choices_for_2nd = 1
        elif keyboard.is_pressed('x'):
            self.choices_for_2nd = 3
        elif keyboard.is_pressed('c'):
            self.choices_for_2nd = 5

        if keyboard.is_pressed('n'):
            self.clearing = True
        elif keyboard.is_pressed('m'):
            self.clearing = False
