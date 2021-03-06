#!/usr/bin/env python

# Constants for Tartarus Game:
FIELD_EMPTY = 0
FIELD_WALL = 1
FIELD_BOX = 2
FIELD_ROBOT = 3
DIR_UP = 4
DIR_RIGHT = 5
DIR_DOWN = 6
DIR_LEFT = 7

MAP_SIZE = 6                    # 6 x 6 grid
NUM_OF_BOXES = 6                # Boxes / boulders
NUM_OF_FIELDS = MAP_SIZE + 2    # 8 x 8 grid (Map + padding)

# Colors for GUI
COLOR_BACKGROUND = (190, 190, 190)
COLOR_BACKGROUND_HIGHLIGHT = (220, 220, 220)
COLOR_WALL = (30, 30, 30)
COLOR_WALL_HIGHLIGHT = (70, 70, 70)
COLOR_BOX = (0, 0, 150)
COLOR_ROBOT = (0, 150, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

FONT_SIZE_1 = 30
FONT_SIZE_2 = 25
FONT_SIZE_3 = 14

MAX_MOVES = 80
MAX_CONSECUTIVE_MOVES = 4
MAX_SCORE = 1100    # 10
MIN_SCORE = 10      # 0

ACTION_TURN_LEFT = 100
ACTION_TURN_RIGHT = 101
ACTION_MOVE_FORWARD = 102
ACTION_RESET = 103