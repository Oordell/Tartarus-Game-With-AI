#!/usr/bin/env python

from gui import GameGUI as GUI
from map import TartarusMap as tm
from constants import *


class TartarusGame(object):
    def __init__(self, enable_gui=True, highlight_sensors=True, fps=30):
        self.view_gui = enable_gui
        self.view_highlight_sensors = highlight_sensors
        self.fps = fps

        self.gui = GUI(highlight_sensors=self.view_highlight_sensors, fps=self.fps) if self.view_gui else None
        self.map = tm()

        self.new_game = True
        self.running = False
        self.moves = 0
        self.score = 0

    def create_new_game(self):
        self.map.new_map()
        self.moves = 0
        self.score = 0
        if self.view_gui:
            self.gui.draw_map(self.map)
            self.gui.draw_moves(moves=self.moves)
            self.gui.draw_score(score=self.score)

    def action_turn_left(self):
        self.map.robot_direction -= 1
        if self.map.robot_direction < DIR_UP:
            self.map.robot_direction += 4
        if self.view_gui:
            self.gui.draw_robot(self.map)

    def action_turn_right(self):
        self.map.robot_direction += 1
        if self.map.robot_direction > DIR_LEFT:
            self.map.robot_direction -= 4
        if self.view_gui:
            self.gui.draw_robot(self.map)

    def action_move_forward(self):
        next_field_1, next_field_2 = self.get_next_two_fields()

        if not self.is_action_move_valid(next_field_1, next_field_2):
            return
        if self.map.robot_direction == DIR_UP:
            self.map.map[self.map.robot_pos[0]][self.map.robot_pos[1]] = FIELD_EMPTY
            self.map.map[self.map.robot_pos[0] - 1][self.map.robot_pos[1]] = FIELD_ROBOT
            if next_field_1 == FIELD_BOX:
                self.map.map[self.map.robot_pos[0] - 2][self.map.robot_pos[1]] = FIELD_BOX
            self.map.robot_pos = [self.map.robot_pos[0] - 1, self.map.robot_pos[1]]

        elif self.map.robot_direction == DIR_RIGHT:
            self.map.map[self.map.robot_pos[0]][self.map.robot_pos[1]] = FIELD_EMPTY
            self.map.map[self.map.robot_pos[0]][self.map.robot_pos[1] + 1] = FIELD_ROBOT
            if next_field_1 == FIELD_BOX:
                self.map.map[self.map.robot_pos[0]][self.map.robot_pos[1] + 2] = FIELD_BOX
            self.map.robot_pos = [self.map.robot_pos[0], self.map.robot_pos[1] + 1]

        elif self.map.robot_direction == DIR_DOWN:
            self.map.map[self.map.robot_pos[0]][self.map.robot_pos[1]] = FIELD_EMPTY
            self.map.map[self.map.robot_pos[0] + 1][self.map.robot_pos[1]] = FIELD_ROBOT
            if next_field_1 == FIELD_BOX:
                self.map.map[self.map.robot_pos[0] + 2][self.map.robot_pos[1]] = FIELD_BOX
            self.map.robot_pos = [self.map.robot_pos[0] + 1, self.map.robot_pos[1]]

        elif self.map.robot_direction == DIR_LEFT:
            self.map.map[self.map.robot_pos[0]][self.map.robot_pos[1]] = FIELD_EMPTY
            self.map.map[self.map.robot_pos[0]][self.map.robot_pos[1] - 1] = FIELD_ROBOT
            if next_field_1 == FIELD_BOX:
                self.map.map[self.map.robot_pos[0]][self.map.robot_pos[1] - 2] = FIELD_BOX
            self.map.robot_pos = [self.map.robot_pos[0], self.map.robot_pos[1] - 1]

    def is_action_move_valid(self, next_1=None, next_2=None):
        if not next_1:
            next_field_1, next_field_2 = self.get_next_two_fields()
        else:
            next_field_1 = next_1
            next_field_2 = next_2

        if  (next_field_1 == FIELD_WALL) or \
            (next_field_1 == FIELD_BOX and (next_field_2 == FIELD_BOX or next_field_2 == FIELD_WALL)):
            return False
        return True
    
    def get_next_two_fields(self):
        next_field_1 = None
        next_field_2 = None

        if self.map.robot_direction == DIR_UP:
            next_field_1 = self.map.map[self.map.robot_pos[0] - 1][self.map.robot_pos[1]]
            if not next_field_1 == FIELD_WALL:
                next_field_2 = self.map.map[self.map.robot_pos[0] - 2][self.map.robot_pos[1]] 
        elif self.map.robot_direction == DIR_RIGHT:
            next_field_1 = self.map.map[self.map.robot_pos[0]][self.map.robot_pos[1] + 1]
            if not next_field_1 == FIELD_WALL:
                next_field_2 = self.map.map[self.map.robot_pos[0]][self.map.robot_pos[1] + 2] 
        elif self.map.robot_direction == DIR_DOWN:
            next_field_1 = self.map.map[self.map.robot_pos[0] + 1][self.map.robot_pos[1]]
            if not next_field_1 == FIELD_WALL:
                next_field_2 = self.map.map[self.map.robot_pos[0] + 2][self.map.robot_pos[1]] 
        elif self.map.robot_direction == DIR_LEFT:
            next_field_1 = self.map.map[self.map.robot_pos[0]][self.map.robot_pos[1] - 1]
            if not next_field_1 == FIELD_WALL:
                next_field_2 = self.map.map[self.map.robot_pos[0]][self.map.robot_pos[1] - 2] 
        
        return next_field_1, next_field_2

    def update_score(self, ai_score_map=False):
        score_map = [[2,    1,  1,  1,  1,  2],
                     [1,    0,  0,  0,  0,  1],
                     [1,    0,  0,  0,  0,  1],
                     [1,    0,  0,  0,  0,  1],
                     [1,    0,  0,  0,  0,  1],
                     [2,    1,  1,  1,  1,  2]]
        if ai_score_map:
            score_map = [[200, 150, 100, 100, 150, 200],
                         [150, 10, 5, 5, 10, 150],
                         [100, 5, 0, 0, 5, 100],
                         [100, 5, 0, 0, 5, 100],
                         [150, 10, 5, 5, 10, 150],
                         [200, 150, 100, 100, 150, 200]]

        temp_score = 0

        for y in range(0, MAP_SIZE):
            for x in range(0, MAP_SIZE):
                if self.map.map[y + 1][x + 1] == FIELD_BOX:
                    temp_score += score_map[y][x]

        if self.score != temp_score:
            self.score = temp_score

    def run(self, autorun=False, random_movement=True, action=None):
        while True:
            if self.new_game:
                self.create_new_game()
                self.new_game = False
                self.running = True
            
            if autorun:
                self.run_auto(random_movement=random_movement, action=action)
            else:
                self.run_manual()

            if self.moves >= MAX_MOVES:
                self.running = False
    
    def run_manual(self):
        if self.view_gui:
            move = self.gui.run()
            self.perform_action(action=move)
    
    def run_auto(self, random_movement=True, action=None, ai_score_map=False):
        move = action
        if self.view_gui:
            move = self.gui.run_auto(random_actions=random_movement, action=action)
        self.perform_action(action=move, ai_score_map=ai_score_map)
        if self.view_gui:
            self.gui.update_display()

    def perform_action(self, action, ai_score_map=False):
        if action == ACTION_RESET:
            self.new_game = True
            return
        
        if self.running:
            if action == ACTION_MOVE_FORWARD:
                self.action_move_forward()
            elif action == ACTION_TURN_LEFT:
                self.action_turn_left()
            elif action == ACTION_TURN_RIGHT:
                self.action_turn_right()

            self.moves += 1
            self.update_score(ai_score_map=ai_score_map)

            if self.view_gui:
                self.gui.draw_map(self.map)
                self.gui.draw_moves(self.moves)
                self.gui.draw_score(self.score)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Tartarus game")
    parser.add_argument('-f', '--freq', dest='freq', default=30, type=int, help="Frequency")
    parser.add_argument('-g', '--gui', dest='gui', default=True, action='store_false', help="Disable GUI")
    parser.add_argument('-hs', '--high_sen', dest='highlight_sensors', default=True, action='store_false', help="Hide sensors")
    parser.add_argument('-a', '--autorum', dest='auto', default=False, action='store_true', help="Autorun")
    args = parser.parse_args()

    game = TartarusGame(enable_gui=args.gui, highlight_sensors=args.highlight_sensors, fps=args.freq)
    game.run(autorun=args.auto)
