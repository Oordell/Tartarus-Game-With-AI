#!/usr/bin/env python

import random as rand
from constants import *


class TartarusMap(object):
    def __init__(self):
        self.map = None
        self.valid_map = False
        self.robot_pos = [-1, -1]      #[y, x]
        self.robot_direction = None
        self.sensor_readings = []
        self.new_map()
        
    def new_map(self):
        self.valid_map = False
        self.create_empty_map()
        self.place_boxes()
        self.place_robot()
        self.update_sensor_readings()

    def create_empty_map(self):
        self.map = []
        # Adding walls as padding all around the map
        for y in range(0, MAP_SIZE + 2):
            temp_map = []
            for x in range(0, MAP_SIZE + 2):
                if y == 0 or y == MAP_SIZE + 1 or x == 0 or x == MAP_SIZE + 1:
                    temp_map.append(FIELD_WALL)
                else:
                    temp_map.append(FIELD_EMPTY)
            self.map.append(temp_map)
    
    def place_boxes(self):
        valid_boxes_placed = 0
        while valid_boxes_placed < NUM_OF_BOXES:
            x, y = rand.randint(2, MAP_SIZE-1), rand.randint(2, MAP_SIZE-1)
            if self.map[y][x] == FIELD_EMPTY:
                self.map[y][x] = FIELD_BOX
                valid_boxes_placed += 1
        if not self.is_boxlocation_valid():
            self.create_empty_map()
            self.place_boxes()
    
    def is_boxlocation_valid(self):
        for y in range(2, MAP_SIZE-1):
            for x in range(2, MAP_SIZE-1):
                # Checking for four boxes in a square:
                if self.map[y][x] == FIELD_BOX \
                    and self.map[y + 1][x] == FIELD_BOX \
                    and self.map[y][x + 1] == FIELD_BOX \
                    and self.map[y + 1][x + 1] == FIELD_BOX:
                    return False
        ''' Check for a box-placement like this (Willson-configuration): 
        0   0   0   0   0
        0   2   2   0   0
        0   2   0   2   0
        0   0   2   2   0
        0   0   0   0   0
        or 
        0   0   0   0   0
        0   0   2   2   0
        0   2   0   2   0
        0   2   2   0   0
        0   0   0   0   0
        '''
        for y in range(3, MAP_SIZE - 1):
            for x in range(3, MAP_SIZE - 1):
                if self.map[y][x] == FIELD_EMPTY:
                    if self.map[y][x - 1] == FIELD_BOX \
                        and self.map[y - 1][x - 1] == FIELD_BOX \
                        and self.map[y - 1][x] == FIELD_BOX \
                        and self.map[y][x + 1] == FIELD_BOX \
                        and self.map[y + 1][x + 1] == FIELD_BOX \
                        and self.map[y + 1][x] == FIELD_BOX:
                        # print("Willson-configuration. Resetting map.")
                        return False
                    elif self.map[y - 1][x] == FIELD_BOX \
                        and self.map[y - 1][x + 1] == FIELD_BOX \
                        and self.map[y][x + 1] == FIELD_BOX \
                        and self.map[y + 1][x] == FIELD_BOX \
                        and self.map[y + 1][x - 1] == FIELD_BOX \
                        and self.map[y][x - 1] == FIELD_BOX:
                        # print("Willson-configuration. Resetting map.")
                        return False
        return True

    def place_robot(self):
        pos_valid = False
        while not pos_valid:
            x, y = rand.randint(2, MAP_SIZE-1), rand.randint(2, MAP_SIZE-1)
            if self.map[y][x] == FIELD_EMPTY:
                self.map[y][x] = FIELD_ROBOT
                self.robot_pos[0] = y
                self.robot_pos[1] = x
                pos_valid = True
        self.robot_direction = rand.randint(DIR_UP, DIR_LEFT)

    def update_sensor_readings(self):
        # Sensor reading is dependent on robot orientation. 
        # The sensor output is always clock-wise, starting from
        # top-left sensor, seen from the robots orientation.
        self.sensor_readings = []
        if self.robot_direction == DIR_UP:
            self.sensor_readings.append(self.map[self.robot_pos[0] - 1][self.robot_pos[1] - 1])
            self.sensor_readings.append(self.map[self.robot_pos[0] - 1][self.robot_pos[1] + 0])
            self.sensor_readings.append(self.map[self.robot_pos[0] - 1][self.robot_pos[1] + 1])
            self.sensor_readings.append(self.map[self.robot_pos[0] + 0][self.robot_pos[1] + 1])
            self.sensor_readings.append(self.map[self.robot_pos[0] + 1][self.robot_pos[1] + 1])
            self.sensor_readings.append(self.map[self.robot_pos[0] + 1][self.robot_pos[1] + 0])
            self.sensor_readings.append(self.map[self.robot_pos[0] + 1][self.robot_pos[1] - 1])
            self.sensor_readings.append(self.map[self.robot_pos[0] + 0][self.robot_pos[1] - 1])
        elif self.robot_direction == DIR_RIGHT:
            self.sensor_readings.append(self.map[self.robot_pos[0] - 1][self.robot_pos[1] + 1])
            self.sensor_readings.append(self.map[self.robot_pos[0] + 0][self.robot_pos[1] + 1])
            self.sensor_readings.append(self.map[self.robot_pos[0] + 1][self.robot_pos[1] + 1])
            self.sensor_readings.append(self.map[self.robot_pos[0] + 1][self.robot_pos[1] + 0])
            self.sensor_readings.append(self.map[self.robot_pos[0] + 1][self.robot_pos[1] - 1])
            self.sensor_readings.append(self.map[self.robot_pos[0] + 0][self.robot_pos[1] - 1])
            self.sensor_readings.append(self.map[self.robot_pos[0] - 1][self.robot_pos[1] - 1])
            self.sensor_readings.append(self.map[self.robot_pos[0] - 1][self.robot_pos[1] - 0])
        elif self.robot_direction == DIR_DOWN:
            self.sensor_readings.append(self.map[self.robot_pos[0] + 1][self.robot_pos[1] + 1])
            self.sensor_readings.append(self.map[self.robot_pos[0] + 1][self.robot_pos[1] + 0])
            self.sensor_readings.append(self.map[self.robot_pos[0] + 1][self.robot_pos[1] - 1])
            self.sensor_readings.append(self.map[self.robot_pos[0] + 0][self.robot_pos[1] - 1])
            self.sensor_readings.append(self.map[self.robot_pos[0] - 1][self.robot_pos[1] - 1])
            self.sensor_readings.append(self.map[self.robot_pos[0] - 1][self.robot_pos[1] + 0])
            self.sensor_readings.append(self.map[self.robot_pos[0] - 1][self.robot_pos[1] + 1])
            self.sensor_readings.append(self.map[self.robot_pos[0] + 0][self.robot_pos[1] + 1])
        elif self.robot_direction == DIR_LEFT:
            self.sensor_readings.append(self.map[self.robot_pos[0] + 1][self.robot_pos[1] - 1])
            self.sensor_readings.append(self.map[self.robot_pos[0] - 0][self.robot_pos[1] - 1])
            self.sensor_readings.append(self.map[self.robot_pos[0] - 1][self.robot_pos[1] - 1])
            self.sensor_readings.append(self.map[self.robot_pos[0] - 1][self.robot_pos[1] - 0])
            self.sensor_readings.append(self.map[self.robot_pos[0] - 1][self.robot_pos[1] + 1])
            self.sensor_readings.append(self.map[self.robot_pos[0] - 0][self.robot_pos[1] + 1])
            self.sensor_readings.append(self.map[self.robot_pos[0] + 1][self.robot_pos[1] + 1])
            self.sensor_readings.append(self.map[self.robot_pos[0] + 1][self.robot_pos[1] + 0])

        # convert to string for AI to read:
        temp = ""
        for i in range(len(self.sensor_readings)):
            temp += str(self.sensor_readings[i])
        self.sensor_readings = temp

    def print(self):
        for i in range(MAP_SIZE+2):
            print(self.map[i])


if __name__ == '__main__':
    game = TartarusMap()
    game.print()
    print(game.sensor_readings)
