import math
import pygame as pg
from enum import Enum
import Const

# Actions
AI_DIR_FORWARD      = 0
AI_DIR_BACKWARD     = 1
AI_DIR_LEFT         = 2
AI_DIR_RIGHT        = 3
AI_DIR_ATTACK       = 4
AI_DIR_STOP         = 5
ACTION_NONE = {'forward':False, 'backward':False, 'left':False, 'right':False, 'attack':False}

# Basic
MAX_DISTANCE = Const.ARENA_GRID_COUNT * math.sqrt(2)
MAX_ACTION_TIME = 20 * Const.FPS # frames

# Graph
SCALE = 2.0
WIDTH = 1 / SCALE
LENGTH = int(Const.ARENA_GRID_COUNT * SCALE)

# D, R, U, L, DR, UR, UL, DL
DXY = [ pg.Vector2(0, 1), pg.Vector2(1, 0), pg.Vector2(0, -1), pg.Vector2(-1, 0), \
        pg.Vector2(1, 1), pg.Vector2(1, -1), pg.Vector2(-1, -1), pg.Vector2(-1, 1)]
DW = [1] * 4 + [math.sqrt(2)] * 4

# Brain
SEGMENT_CLEAR_SIMULATE_LENGTH = 0.2 # grid
DIJKSTRA_FREQUENCY = 10 # frames per evaluate
PLAYER_HABIT_DOT_AMOUNT = 10
PLAYER_HABIT_MULTIPLIER = 0.9

# Navigator
MAX_ALT_DISTANCE = 10
BOOST_CHECK_MULTIPLIER = 4
BOOST_CHECK_ANGLE_TOLERANCE = 0.05 # radian
MOVING_ROTATIONAL_TOLERANCE = 0.02 # radian

# Collector
ITEM_SCAN_FREQUENCY = 30 # frames per scan

# Attacker
ATTACK_ROTATIONAL_TOLERANCE = 0.02 # radian
ATTACK_TARGET_SCAN_FREQUENCY = 30 # frames per scan
MINIMUM_ATTACK_RANGE = 5 # grids
SHOTGUN_ATTACK_RANGE_MULTIPLIER = 2
ADDITIONAL_ATTACK_RANGE = 5
SHOOT_SIMULATE_LENGTH = 0.2
ATTACK_POSITION_PREDICT_TIME = 60 # frames

# Modes
class Mode(Enum):
    IDLE = 0
    COLLECT = 1
    ATTACK = 2