import math
import pygame as pg


# model
FPS = 60 # frame per second
GAME_LENGTH = math.inf * FPS # temporarily set to infinity
PLAYER_NUMBER = 4
PLAYER_INIT_POSITION = [pg.Vector2(10, 10), pg.Vector2(21, 10), pg.Vector2(10, 21), pg.Vector2(21, 21)]

PLAYER_RADIUS = 0.5        # grid unit 
PLAYER_BASE_SPEED = 10     # grid unit per second
PLAYER_ROTATION_SPEED = 3  # rad per second

PLAYER_ATTACK_CD = 2       # second
PLAYER_ATTACK_KICK = 10    # grid unit per second
PLAYER_AUX_LINE_LENGTH = 1 # grid unit

BULLET_RADIUS = 0.2        # grid unit
BULLET_REPULSION = 30      # grid unit per second
BULLET_SPEED = 15          # grid unit per second
BULLET_LIFESPAM = 6        # second
BULLET_TRACE_TIME = 0.1    # second
BULLET_HIT_SCORE = 10

GUN_TYPE_NORMAL_GUN = 0
GUN_TYPE_MACHINE_GUN = 1
GUN_TYPE_SNIPER = 2
GUN_TYPE_SHOTGUN = 3

GUN_USE_TIME = [math.inf, 10, 20, 20]
GUN_ATTACK_CD_MULTIPLIER = [1, 1/4, 1, 1]
GUN_ATTACK_KICK_MULTIPLIER = [1, 1/4, 1.5, 1]
GUN_AUX_LINE_LENGTH_MULTIPLIER = [1, 1, 1, 1]
GUN_BULLET_TRACE_TIME_MULTIPLIER = [1, 1, 2, 1]
GUN_BULLET_REPULSION_MULTIPLIER = [1, 1/3, 2, 1]

SHOTGUN_ATTACK_ANGLE = math.pi / 36

BUFF_TYPE_ATTACK_CD = 1
BUFF_TYPE_REPULSION = 2
BUFF_TYPE_AUX_LINE_LENGTH = 3

BUFF_VALUE_ATTACK_CD = -0.3
BUFF_VALUE_REPULSION = 0.4
BUFF_VALUE_BULLET_TRACE_TIME = 0.01
BUFF_VALUE_AUX_LINE_LENGTH = 1

PLAYER_QUOTA_ATTACK_CD = 5
PLAYER_QUOTA_REPULSION = 5
PLAYER_QUOTA_AUX_LINE_LENGTH = math.inf

ITEM_GENERATOR_COOLDOWN = 1  # second
ITEM_MAX = 10
ITEM_GUN_RADIUS = 0.5        # grid unit
ITEM_BUFF_RADIUS = 0.5       # grid unit

# view
WINDOW_CAPTION = 'Challenge 2022'
WINDOW_SIZE = (800, 800)
ARENA_SIZE = (800, 800)
ARENA_GRID_COUNT = 30
ARENA_GRID_SIZE = ARENA_SIZE[0] / ARENA_GRID_COUNT
BACKGROUND_COLOR = pg.Color('black')
PLAYER_COLOR = [pg.Color('green'), pg.Color('magenta'), pg.Color('yellow'), pg.Color('blue')]


# State machine constants
STATE_POP = 0 # for convenience, not really a state which we can be in
STATE_MENU = 1
STATE_PLAY = 2
STATE_STOP = 3 # not implemented yet
STATE_ENDGAME = 4


# controller
PLAYER_MOVE_FORWARD = 1
PLAYER_MOVE_BACKWARD = -1

PLAYER_ROTATE_LEFT = -1
PLAYER_ROTATE_RIGHT = 1

PLAYER_MOVE_KEYS = {
    pg.K_w: (0, PLAYER_MOVE_FORWARD),
    pg.K_s: (0, PLAYER_MOVE_BACKWARD),
    pg.K_t: (1, PLAYER_MOVE_FORWARD),
    pg.K_g: (1, PLAYER_MOVE_BACKWARD),
    pg.K_i: (2, PLAYER_MOVE_FORWARD),
    pg.K_k: (2, PLAYER_MOVE_BACKWARD),
    pg.K_UP: (3, PLAYER_MOVE_FORWARD),
    pg.K_DOWN: (3, PLAYER_MOVE_BACKWARD)
}


PLAYER_ROTATE_KEYS = {
    pg.K_a: (0, PLAYER_ROTATE_LEFT),
    pg.K_d: (0, PLAYER_ROTATE_RIGHT),
    pg.K_f: (1, PLAYER_ROTATE_LEFT),
    pg.K_h: (1, PLAYER_ROTATE_RIGHT),
    pg.K_j: (2, PLAYER_ROTATE_LEFT),
    pg.K_l: (2, PLAYER_ROTATE_RIGHT),
    pg.K_LEFT: (3, PLAYER_ROTATE_LEFT),
    pg.K_RIGHT: (3, PLAYER_ROTATE_RIGHT)
}

PLAYER_ATTACK_KEYS = {
    pg.K_q: (0, 'attack'),
    pg.K_r: (1, 'attack'),
    pg.K_u: (2, 'attack'),
    pg.K_RSHIFT: (3, 'attack')
}

GAME_STOP_KEY = pg.K_SPACE
GAME_CONTINUE_KEY = pg.K_RETURN
GAME_RESTART_KEY = pg.K_F5
GAME_FULLSCREEN_KEY = pg.K_F11