import pygame as pg

# model
FPS = 60 # frame per second
GAME_LENGTH = 30 * FPS
PLAYER_INIT_POSITION = [pg.Vector2(200, 400), pg.Vector2(600, 400), pg.Vector2(200, 0), pg.Vector2(200, 0)]

PLAYER_RADIUS = 75
SPEED_ATTACK = 100
SPEED_DEFENSE = 70
DIRECTION_TO_VEC2 = {
    'up': pg.Vector2(0, -1),
    'left': pg.Vector2(-1, 0),
    'down': pg.Vector2(0, 1),
    'right': pg.Vector2(1, 0),
}


# State machine constants
STATE_POP = 0 # for convenience, not really a state which we can be in
STATE_MENU = 1
STATE_PLAY = 2
STATE_STOP = 3 # not implemented yet
STATE_ENDGAME = 4


# view
WINDOW_CAPTION = 'Challenge 2020 Homework'
WINDOW_SIZE = (800, 800)
ARENA_SIZE = (800, 800)
BACKGROUND_COLOR = pg.Color('black')
PLAYER_COLOR = [pg.Color('green'), pg.Color('magenta'), pg.Color('yellow'), pg.Color('blue')]


# controller

PLAYER_MOVE_FRONT = 1
PLAYER_MOVE_BACK = -1
PLAYER_ROTATE_LEFT = 1
PLAYER_ROTATE_RIGHT = -1

PLAYER_MOVE_KEYS = {
    pg.K_w: (0, PLAYER_MOVE_FRONT),
    pg.K_s: (0, PLAYER_MOVE_BACK),
    pg.K_t: (1, PLAYER_MOVE_FRONT),
    pg.K_g: (1, PLAYER_MOVE_BACK),
    pg.K_i: (2, PLAYER_MOVE_FRONT),
    pg.K_k: (2, PLAYER_MOVE_BACK),
    pg.K_UP: (3, PLAYER_MOVE_FRONT),
    pg.K_DOWN: (3, PLAYER_MOVE_BACK)
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