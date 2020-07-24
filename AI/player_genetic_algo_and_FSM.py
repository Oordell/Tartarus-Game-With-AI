#!/usr/bin/env python

from game import TartarusGame as TarGame
from constants import *
import random as rand


class PlayerAIGenetic(object):
    def __init__(self, num_of_states=3, enable_gui=False, highlight_sensors=False):
        self.num_of_states = num_of_states
        self.view_gui = enable_gui
        self.highlight_sensors = highlight_sensors
        self.game = TarGame(enable_gui=self.view_gui, highlight_sensors=self.highlight_sensors)

        self.states = []
        self.transitions = dict()
        self.current_state = 0
        self.fitness = float(0.0)
        self.total_points_scored = 0
        self.generation = -1
        self.population_number = -1

    def load_params(self, num_of_states, states, transitions, generation, number):
        self.num_of_states = num_of_states
        self.states = states
        self.transitions = transitions
        self.current_state = 0
        if self.generation < 0:
            self.generation = generation
            self.population_number = number

    def play_game(self):
        self.game.create_new_game()
        self.game.running = True

        last_action = -1
        consecutive_moves = 1
        state_history = [-1, -1, -1, -1, -1, -1, -1, -1]

        for move_number in range(MAX_MOVES):
            action = self.states[self.current_state]

            self.game.run_auto(random_movement=False, action=action, ai_score_map=True)
            if self.view_gui:
                self.game.gui.draw_map(self.game.map)

            if action == last_action:
                consecutive_moves += 1
            else:
                consecutive_moves = 1

            # Checking for turn-back events.
            state_history.pop(0)
            state_history.append(action)
            if move_number > 5 and \
                    (state_history[0] == state_history[2] and state_history[1] == state_history[3]) or \
                    (state_history[0] == state_history[4] and state_history[1] == state_history[5] and
                     state_history[2] == state_history[6] and state_history[3] == state_history[7]):
                consecutive_moves += MAX_CONSECUTIVE_MOVES

            if consecutive_moves > MAX_CONSECUTIVE_MOVES:
                consecutive_moves = 1
                temp_new_state = rand.randint(0, self.num_of_states - 1)
                while temp_new_state == self.current_state:
                    temp_new_state = rand.randint(0, self.num_of_states - 1)
                # self.transitions[self.game.map.sensor_readings] = temp_new_state
                self.current_state = temp_new_state
            else:
                self.game.map.update_sensor_readings()
                self.current_state = self.transitions[self.game.map.sensor_readings]

        self.total_points_scored += self.game.score


if __name__ == '__main__':
    pass
