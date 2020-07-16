# Tartarus Game With AI
The game of Tartarus implimented using PyGame.
This is ment as a platform for implimenting AI-algorithms to solve the game of Tartarus.

![Game_example](/img/game_ex.jpg)
Format: ![Alt Text](url)

## Game description

The Tartarus game is a 6x6 tile-based game, where 6 boxes are randomly placed within the inner most 4x4 tiles. A robot is randomly placed with a random orientation in a free spot in the same inner 4x4 space, and needs to push the boxes up against the walls. Boxes can only be moved if the tile on the opposite side of the box, seen from the robot, is free. The robot can only see its 8 adjacent tiles, which can be either a wall, a box or empty. The robot can only move forward, or turn left or right. A box placed against a wall rewards 1 point, and a box in a corner rewards 2 points (max 10 points pr. game). The robot is given a maximum of 80 moves to make as high a score as possible. Note that attempting to move a box that can’t be moved or driving into a wall also counts as a move. 

Ude the left, right and up arrow keys to move the robot, if using manual control.

## Run the program

`$ python3 game.py`
* _-f_ : Set the frequenzy of display when using the GUI.
* _-g_ : Disable the GUI (Used for faster runs when using AI).
* _-hs_ : Hide the highlighted sensors around the robot.
* _-a_ : Enable autorun.

## File description

* _game.py_ : The main file that will run the game, incl. game logic.
* _map.py_ : Contains the map that the game logic is build on.
* _gui.py_ : Everything revolving the GUI of the game.
* _constants.py_ : Global constants.

## The use of AI

* If using AI, use the function `update_sensor_readings(self)` in _map.py_ to update what the robot sees from it sensors. Then the `self.sensor_readings` variable can be used to see read the sensors. 
* An action can be controled by another file, by using the `run_auto(self, random_movement=True, action=None)` function from the file _game.py_, where _random\_movement_ is set to _False_, and the movement is inputed as _action_.
* Once the max number of moves has been reached (80), the map must be reset (Use the constant _ACTION\_RESET_ from _constants.py_.
