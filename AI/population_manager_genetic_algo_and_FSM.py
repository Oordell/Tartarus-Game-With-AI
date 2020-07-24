#!/usr/bin/env python

import csv
from player_genetic_algo_and_FSM import PlayerAIGenetic as Player
import random as rand
from constants import *


class PopulationManager(object):
    def __init__(self,
                 enable_gui=False,
                 highlight_sensors=False,
                 num_of_states=3,
                 num_of_players=100,
                 num_of_games=300,
                 num_of_generations=100,
                 sensor_input_combination_file_name=None,
                 write_results=False,
                 output_file_path=""):
        self.view_gui = enable_gui
        self.highlight_sensors = highlight_sensors
        self.num_of_states = num_of_states
        self.num_of_players = num_of_players
        self.num_of_games = num_of_games
        self.num_of_generations = num_of_generations
        self.sensor_input_combination_file_name = sensor_input_combination_file_name
        self.write_results = write_results
        self.output_file_path = output_file_path
        self.sensor_combinations = []

        if self.sensor_input_combination_file_name:
            self.load_sensor_input_combination_file()

        self.population = []
        self.generation = 1
        self.max_possible_score = self.num_of_games * (MAX_SCORE - MIN_SCORE)

    def load_sensor_input_combination_file(self):
        with open(self.sensor_input_combination_file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                key = ""
                for l in range(len(row)):
                    key += row[l]
                self.sensor_combinations.append(key)

    def fill_population_with_random_players(self):
        self.population = []
        for num in range(self.num_of_players):
            s = self.get_single_random_player(num)
            self.population.append(s)

    def get_single_random_player(self, number):
        states = self.get_states()
        transition = dict()
        player = Player()

        for sensor_input in self.sensor_combinations:
            temp_state = rand.randint(0, self.num_of_states - 1)
            while not self.validate_transition_and_action(states, sensor_input, temp_state):
                temp_state = rand.randint(0, self.num_of_states - 1)
            transition[sensor_input] = temp_state

        player.load_params(self.num_of_states, states, transition, self.generation, number)
        return player

    def get_states(self):
        states = []
        for j in range(0, self.num_of_states):
            action = (j - (int(j / 3) * 3)) + ACTION_TURN_LEFT
            states.append(action)
        return states

    @staticmethod
    def validate_transition_and_action(states, sensor_input, new_state):
        # If it's in a corner, it should rotate to face out of the corner:
        # Wall in front and to the left:
        if sensor_input[1] == FIELD_WALL and sensor_input[7] == FIELD_WALL and not \
                states[new_state] == ACTION_TURN_RIGHT:
            return False
        # Wall in front and to the right:
        elif sensor_input[1] == FIELD_WALL and sensor_input[3] == FIELD_WALL and not \
                states[new_state] == ACTION_TURN_LEFT:
            return False
        # If there is a wall in front, don't switch to state where you drive straight
        elif sensor_input[1] == FIELD_WALL and states[new_state] == ACTION_MOVE_FORWARD:
            return False
        # Wall to the left, don't turn left:
        elif sensor_input[7] == FIELD_WALL and states[new_state] == ACTION_TURN_LEFT:
            return False
        # Wall to the right, don't turn right:
        elif sensor_input[3] == FIELD_WALL and states[new_state] == ACTION_TURN_RIGHT:
            return False
        # If there is symmetry around it, it shouldn't turn, as this will result in eternal rotation
        elif sensor_input == "00000000" or sensor_input == "02020202" or sensor_input == "20202020":
            if not states[new_state] == ACTION_MOVE_FORWARD:
                return False
        return True

    def run_generation(self):
        for player in range(self.num_of_players):
            for game in range(self.num_of_games):
                self.population[player].play_game()
            self.population[player].fitness = self.population[player].total_points_scored / self.max_possible_score

    def evaluate_generation(self):
        next_generation = []
        temp_population = []
        new_child_number = 0
        # 10% best specimens goes to next generation
        best_specimens_cutoff = int(self.num_of_players * 0.10)
        # Taking the best into new generation, and deleting them from current generation
        for i in range(0, best_specimens_cutoff):
            self.population[0].fitness = float(0.0)
            self.population[0].total_points_scored = 0
            next_generation.append(self.population[0])
            self.population.pop(0)

        # Now for the remaining. Pick 3 at random, select the best one (Highest fitness), and add to temp_population
        num_of_randoms = 3
        while len(self.population) >= num_of_randoms:
            valid_selected = 0
            selected = []
            while valid_selected < 3:
                player = rand.randint(0, len(self.population) - 1)
                if player not in selected:
                    selected.append(self.population[player])
                    self.population.pop(player)
                    valid_selected += 1
            # Sort list to find best:
            self.sort_list_of_players(selected)

            # Add best to temp_population:
            temp_population.append(selected[0])

        # Now create children from temp_population:
        while len(temp_population) > 1:
            p1 = temp_population.pop()
            p2 = temp_population.pop()
            # p1.fitness = float(0.0)
            # p2.fitness = float(0.0)
            # p1.total_points_scored = 0
            # p2.total_points_scored = 0
            # Create num_of_randoms * 2 children:
            for i in range(0, num_of_randoms * 2):
                temp_states = self.get_states()
                temp_trans = dict()

                for j in range(0, len(self.sensor_combinations)):
                    # Random number to decide from which parent the state should be copied from
                    p1_or_p2 = rand.getrandbits(1)
                    if p1_or_p2 < 0.5:
                        temp_trans[self.sensor_combinations[j]] = p1.transitions[self.sensor_combinations[j]]
                    else:
                        temp_trans[self.sensor_combinations[j]] = p2.transitions[self.sensor_combinations[j]]

                s = Player(enable_gui=self.view_gui, highlight_sensors=self.highlight_sensors)
                s.load_params(self.num_of_states, temp_states, temp_trans, self.generation, new_child_number)
                new_child_number += 1
                next_generation.append(s)
            #next_generation.append(p1)
            #next_generation.append(p2)

        while len(next_generation) < self.num_of_players:
            player = self.get_single_random_player(new_child_number)
            new_child_number += 1
            next_generation.append(player)

        while len(next_generation) > self.num_of_players:
            next_generation.pop(-1)

        self.population = next_generation

    def mutation(self):
        mutation_chance = 5  # 5/1000 = 0,5 % chance

        for player in range(0, self.num_of_players):
            for sensor_input in self.sensor_combinations:
                res = rand.randint(1, 1000)
                if res <= mutation_chance:
                    new_state = rand.randint(0, self.num_of_states - 1)
                    while not self.validate_transition_and_action(self.population[player].states, sensor_input, new_state):
                        new_state = rand.randint(0, self.num_of_states - 1)
                    self.population[player].transitions[sensor_input] = new_state

    @staticmethod
    def sort_by_fitness(player):
        return player.fitness

    def sort_list_of_players(self, list_of_players):
        list_of_players.sort(key=self.sort_by_fitness, reverse=True)

    def print_generation_recap(self):
        print("Generation: ", self.generation)
        print("Best performer: ", self.population[0].fitness)
        print("Worst performer: ", self.population[-1].fitness)

    def run(self):
        while self.generation <= self.num_of_generations:
            if self.generation == 1:
                self.fill_population_with_random_players()
            self.run_generation()
            self.sort_list_of_players(self.population)
            self.print_generation_recap()
            if self.write_results:
                self.write_results_to_file()
            self.generation += 1
            if self.generation <= self.num_of_generations:
                self.evaluate_generation()
                self.mutation()

    def write_results_to_file(self):
        file_name = self.output_file_path + "generation_" + str(self.generation) + ".csv"
        writer = open(file_name, "w+")
        writer.write("Generation, Population number, Fitness")
        for i in range(0, self.num_of_states):
            writer.write(", state_" + str(i))
        for sen_in in self.sensor_combinations:
            writer.write(", " + str(sen_in))
        writer.write("\n")
        for s in self.population:
            writer.write(str(s.generation) + ", " + str(s.population_number) + ", " + str(s.fitness))
            for state in s.states:
                writer.write(", " + str(state))
            for val in s.transitions.values():
                writer.write(", " + str(val))
            writer.write("\n")
        writer.close()


if __name__ == '__main__':
    PM = PopulationManager(enable_gui=False,
                           highlight_sensors=False,
                           num_of_states=12,
                           num_of_players=100,
                           num_of_generations=500,
                           sensor_input_combination_file_name="sensor_input_combinations.csv",
                           write_results=True,
                           output_file_path="test_results/12states_100players_300_games/")
    PM.run()
