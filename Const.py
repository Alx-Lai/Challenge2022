import math
import pygame as pg


# view
WINDOW_CAPTION = 'Challenge 2020 Homework'
WINDOW_SIZE = (800, 800)
ARENA_SIZE = (800, 800)
ARENA_GRID_COUNT = 30
ARENA_GRID_SIZE = ARENA_SIZE[0] / ARENA_GRID_COUNT
BACKGROUND_COLOR = pg.Color('black')
PLAYER_COLOR = [pg.Color('green'), pg.Color('magenta'), pg.Color('yellow'), pg.Color('blue')]


# model
FPS = 60 # frame per second
GAME_LENGTH = math.inf * FPS # temporarily set to infinity
PLAYER_INIT_POSITION = [pg.Vector2(10, 10), pg.Vector2(21, 10), pg.Vector2(10, 21), pg.Vector2(21, 21)]
PLAYER_INIT_DIRECTION = [pg.Vector2(1, 0), pg.Vector2(1, 0), pg.Vector2(1, 0), pg.Vector2(1, 0)]

PLAYER_RADIUS = 0.5        # grid unit 
PLAYER_BASE_SPEED = 500    # grid unit per second
PLAYER_ROTATION_SPEED = 3  # rad per second

PLAYER_ATTACK_CD = 2       # second
PLAYER_ATTACK_KICK = 1     # grid unit

BULLET_RADIUS = 0.2        # grid unit
BULLET_LENGTH = 1.5        # grid unit
BULLET_REPULSION = 3       # grid unit
BULLET_SPEED = 10          # grid unit per second
BULLET_LIFESPAM = 90       # grid unit
BULLET_HIT_SCORE = 10


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