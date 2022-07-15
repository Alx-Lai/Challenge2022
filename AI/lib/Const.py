import math
import pygame as pg
import Const


# Actions
AI_DIR_FORWARD      = 0
AI_DIR_BACKWARD     = 1
AI_DIR_LEFT         = 2
AI_DIR_RIGHT        = 3
AI_DIR_ATTACK       = 4
AI_DIR_STOP         = 5
ACTION_NONE = {'forward':False, 'backward':False, 'left':False, 'right':False, 'attack':False}

# Graph
SCALE = 2.0
WIDTH = 1 / SCALE
LENGTH = int(Const.ARENA_GRID_COUNT * SCALE)

# D, R, U, L, DR, UR, UL, DL
DXY = [ pg.Vector2(0, 1), pg.Vector2(1, 0), pg.Vector2(0, -1), pg.Vector2(-1, 0), \
        pg.Vector2(1, 1), pg.Vector2(1, -1), pg.Vector2(-1, -1), pg.Vector2(-1, 1)]
DW = [1] * 4 + [math.sqrt(2)] * 4

# Navigator
MOVING_ROTATIONAL_TOLERANCE = 0.03 # radian
DIJKSTRA_FREQUENCY = 30 # frames per evaluate

# Attacker
ATTACK_ROTATIONAL_TOLERANCE = 0.03 # radian
ATTACK_TARGET_SCAN_FREQUENCY = 30 # frames per scan
ATTACK_RANGE = Const.PLAYER_RADIUS / ATTACK_ROTATIONAL_TOLERANCE - 1 # grids
SHOOT_SIMULATE_LENGTH = 0.2
