import math
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
SCALE = 2
WIDTH = 1 / SCALE
LENGTH = int(Const.ARENA_GRID_COUNT * SCALE)

DX = [0, 1, 0, -1, 1, 1, -1, -1] # D, R, U, L, DR, UR, UL, DL
DY = [1, 0, -1, 0, 1, -1, -1, 1]
DW = [1] * 4 + [math.sqrt(2)] * 4

# Navigator
MOVING_ROTATIONAL_TOLERANCE = 0.03 # radian
DIJKSTRA_FREQUENCY = 3 # frames per evaluate

# Attacker
ATTACK_ROTATIONAL_TOLERANCE = 0.03 # radian
ATTACK_TARGET_SCAN_FREQUENCY = 60 # frames per scan
ATTACK_RANGE = 10.0 # grids