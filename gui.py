#!/usr/bin/env python

import pygame as py
import random as rand
from constants import *
from map import TartarusMap

class GameGUI(object):
    def __init__(self, highlight_sensors=True, fps=30):
        self.view_highlight_sensors = highlight_sensors
        self.screen_height = 400
        self.screen_width = self.screen_height + 200
        self.scale = self.screen_height / 400

        py.init()
        py.display.set_caption("Tartarus")

        self.screen = py.display
        self.screen_surface = self.screen.set_mode((self.screen_width, self.screen_height))
        self.clock = py.time.Clock()
        self.fps = fps

        self.fields = []
        self.field_width = self.screen_height / NUM_OF_FIELDS

        self.img_boulder = py.image.load('img/boulder.png')
        self.img_boulder = py.transform.scale(self.img_boulder, (int(self.field_width), int(self.field_width)))
        self.img_robot = py.image.load('img/robot.png')
        self.img_robot = py.transform.scale(self.img_robot, (int(self.field_width), int(self.field_width)))

    def draw_map(self, map):
        self.make_fields()
        self.draw_all_walls(map)
        for y in range(1, NUM_OF_FIELDS - 1):
            for x in range(1, NUM_OF_FIELDS - 1):
                self.draw_empty_field(self.fields[y][x])
                if map.map[y][x] == FIELD_BOX:
                    self.draw_box_on_field(self.fields[y][x])
        self.draw_robot(map)

        self.draw_text('MOVES', 1, FONT_SIZE_1)
        self.draw_text('SCORE', 3, FONT_SIZE_1)
        self.draw_text('Press ENTER to start / reset', 6, FONT_SIZE_3)
    
    def draw_all_walls(self, map):
        for y in range(NUM_OF_FIELDS):
            for x in range(NUM_OF_FIELDS):
                if map.map[y][x] == FIELD_WALL:
                    self.draw_wall(self.fields[y][x])

    def draw_empty_field(self, field):
        py.draw.rect(self.screen_surface, COLOR_BACKGROUND, field)

    def draw_wall(self, field):
        py.draw.rect(self.screen_surface, COLOR_WALL, field)

    def draw_box_on_field(self, field):
        self.screen_surface.blit(self.img_boulder, field)
    
    def draw_robot(self, map):
        y = map.robot_pos[0]
        x = map.robot_pos[1]
        if self.view_highlight_sensors:
            for yy in range(-1, 2):
                for xx in range(-1, 2):
                    if map.map[y + yy][x + xx] == FIELD_WALL:
                        self.draw_highlighted_field_wall(self.fields[y + yy][x + xx])
                    else:
                        self.draw_highlighted_field(self.fields[y + yy][x + xx])
                    if map.map[y + yy][x + xx] == FIELD_BOX:
                        self.draw_box_on_field(self.fields[y + yy][x + xx])
        
        field = self.fields[y][x]
        if map.robot_direction == DIR_UP:
            self.screen_surface.blit(py.transform.rotozoom(self.img_robot, 0, self.scale), field)
        elif map.robot_direction == DIR_DOWN:
            self.screen_surface.blit(py.transform.rotozoom(self.img_robot, 180, self.scale), field)
        elif map.robot_direction == DIR_LEFT:
            self.screen_surface.blit(py.transform.rotozoom(self.img_robot, 90, self.scale), field)
        elif map.robot_direction == DIR_RIGHT:
            self.screen_surface.blit(py.transform.rotozoom(self.img_robot, 270, self.scale), field)

    def draw_highlighted_field(self, field):
        py.draw.rect(self.screen_surface, COLOR_BACKGROUND_HIGHLIGHT, field)

    def draw_highlighted_field_wall(self, field):
        py.draw.rect(self.screen_surface, COLOR_WALL_HIGHLIGHT, field)

    def draw_text(self, tx, placement, size):
        font = py.font.Font('freesansbold.ttf', size)
        text = font.render(tx, True, COLOR_WHITE, COLOR_BLACK)
        text_rect = text.get_rect()
        text_rect.center = ((self.screen_height + self.screen_width) / 2, self.field_width * placement)
        self.screen_surface.blit(text, text_rect)

    def draw_moves(self, moves):
        background_rect = (self.screen_height, self.field_width * 2 - 15 , self.screen_width - self.screen_height, 30)
        py.draw.rect(self.screen_surface, COLOR_BLACK, background_rect)
        self.draw_text(str(moves), 2, FONT_SIZE_2)

    def draw_score(self, score):
        background_rect = (self.screen_height, self.field_width * 4 - 15 , self.screen_width - self.screen_height, 30)
        py.draw.rect(self.screen_surface, COLOR_BLACK, background_rect)
        self.draw_text(str(score), 4, FONT_SIZE_2)

    def make_fields(self):
        for y in range(NUM_OF_FIELDS):
            temp_fields = []
            for x in range(NUM_OF_FIELDS):
                f = (x * self.field_width, y * self.field_width, self.field_width, self.field_width)
                temp_fields.append(f)
            self.fields.append(temp_fields)
        
    def update_display(self):
        py.display.update()
        self.clock.tick(self.fps)

    def run(self):
        while True:
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    quit()
                if event.type == py.KEYDOWN:
                    if event.key == py.K_ESCAPE:
                        py.quit()
                        quit()
                    if event.key == py.K_RIGHT:
                        return ACTION_TURN_RIGHT
                    if event.key == py.K_LEFT:
                        return ACTION_TURN_LEFT
                    if event.key == py.K_UP:
                        return ACTION_MOVE_FORWARD
                    if event.key == py.K_RETURN or event.key == py.K_KP_ENTER:
                        return ACTION_RESET

            self.update_display()

    def run_auto(self, random_actions=True, action=None):
        while True:
            if py.event.peek():
                for event in py.event.get():
                    if event.type == py.QUIT:
                        py.quit()
                        quit()
                    if event.type == py.KEYDOWN:
                        if event.key == py.K_ESCAPE:
                            py.quit()
                            quit()
                        if event.key == py.K_RETURN or event.key == py.K_KP_ENTER:
                            return ACTION_RESET
            else:
                move = -1
                if random_actions:
                    move = rand.randint(ACTION_TURN_LEFT, ACTION_MOVE_FORWARD)
                else:
                    move = action

                if move == ACTION_TURN_LEFT:
                    return ACTION_TURN_LEFT
                elif move == ACTION_TURN_RIGHT:
                    return ACTION_TURN_RIGHT
                elif move == ACTION_MOVE_FORWARD:
                    return ACTION_MOVE_FORWARD
                else:
                    print("ERROR: input action not formated correctly")
                    return
                
            self.update_display()
            

if __name__ == '__main__':
    gui = GameGUI()
    map = TartarusMap()
    gui.draw_map(map)
    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                quit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    py.quit()
                    quit()
        gui.update_display()
