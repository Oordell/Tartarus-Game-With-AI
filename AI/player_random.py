#!/usr/bin/env python

from game import TartarusGame as TarGame
from constants import *
import random as rand


class PlayerRandom(object):
    def __init__(self, enable_gui=False, highlight_sensors=False):
        self.view_gui = enable_gui
        self.highlight_sensors = highlight_sensors
        self.game = TarGame(enable_gui=self.view_gui, highlight_sensors=self.highlight_sensors)

    def play_game(self):
        self.game.create_new_game()
        self.game.running = True

        for i in range(MAX_MOVES):
            move = rand.randint(ACTION_TURN_LEFT, ACTION_MOVE_FORWARD)
            self.game.run_auto(random_movement=False, action=move)
            if self.view_gui:
                self.game.gui.draw_map(self.game.map)


if __name__ == '__main__':
    p = PlayerRandom(True, True)
    p.play_game()
