import math
import pygame as pg


# model
# length unit: a unit grid's size (L)
# time unit: frame (T)

FPS = 60 # frame per second
GAME_LENGTH = math.inf * FPS # temporarily set to infinity
PLAYER_NUMBER = 4
PLAYER_INIT_POSITION = [pg.Vector2(10, 10), pg.Vector2(21, 10), pg.Vector2(10, 21), pg.Vector2(21, 21)]

PLAYER_RADIUS = 0.5                       # L
PLAYER_BASE_SPEED = 10 / FPS              # L / T
PLAYER_ROTATION_SPEED = 3 / FPS           # radian / T

PLAYER_ATTACK_CD = 2 * FPS                # T
PLAYER_ATTACK_KICK = 10 / FPS             # L / T
PLAYER_AUX_LINE_LENGTH = 1                # L

PLAYER_QUOTA_ATTACK_CD = 5
PLAYER_QUOTA_REPULSION = 5
PLAYER_QUOTA_AUX_LINE_LENGTH = math.inf

PLAYER_RESPAWN_TIME = 5 * FPS             # T
PLAYER_MAX_RESPAWN_COUNT = [2, 2, 2, 2]

BULLET_RADIUS = 0.2                       # L
BULLET_REPULSION = 30 / FPS               # L / T
BULLET_SPEED = 15 / FPS                   # L / T
BULLET_LIFESPAM = 6 * FPS                 # T
BULLET_TRACE_TIME = 0.1 * FPS             # T
BULLET_HIT_SCORE = 10

GUN_TYPE_NORMAL_GUN = 0
GUN_TYPE_MACHINE_GUN = 1
GUN_TYPE_SNIPER = 2
GUN_TYPE_SHOTGUN = 3

GUN_USE_TIME = [math.inf * FPS, 10 * FPS, 20 * FPS, 20 * FPS] # T
GUN_ATTACK_CD_MULTIPLIER = [1, 1/4, 1, 1]
GUN_ATTACK_KICK_MULTIPLIER = [1, 1/4, 1.5, 1]
GUN_AUX_LINE_LENGTH_MULTIPLIER = [1, 1, 1, 1]
GUN_BULLET_TRACE_TIME_MULTIPLIER = [1, 1, 2, 1]
GUN_BULLET_REPULSION_MULTIPLIER = [1, 1/3, 2, 1]

SHOTGUN_SPREAD_ANGLE = math.pi / 36       # radian

BUFF_TYPE_ATTACK_CD = 1
BUFF_TYPE_REPULSION = 2
BUFF_TYPE_AUX_LINE_LENGTH = 3

BUFF_VALUE_ATTACK_CD = -0.3 * FPS         # T
BUFF_VALUE_REPULSION = 4 / FPS            # L / T
BUFF_VALUE_BULLET_TRACE_TIME = 0.01 * FPS # T
BUFF_VALUE_AUX_LINE_LENGTH = 1            # L

ITEM_GENERATOR_COOLDOWN = 1 * FPS         # T
ITEM_MAX = 10
ITEM_GUN_RADIUS = 0.5                     # L
ITEM_BUFF_RADIUS = 0.5                    # L

OBSTACLE_RADIUS = 0.5                     # L
RE_FIELD_RADIUS = 0.5                     # L
OBSTACLE_POSITION = [pg.Vector2(i + 0.5, j + 0.5) for i in range(13, 17) for j in range(13, 17)]
RE_FIELD_POSITION = [pg.Vector2(i + 0.5, j + 0.5) for i in range(13, 17) for j in range(17, 19)]

# view
WINDOW_CAPTION = 'Challenge 2022'
WINDOW_SIZE = (800, 800)
ARENA_SIZE = (800, 800)
ARENA_GRID_COUNT = 30
ARENA_GRID_SIZE = ARENA_SIZE[0] / ARENA_GRID_COUNT
BACKGROUND_COLOR = pg.Color('black')
PLAYER_COLOR = [pg.Color(0, 255, 0), pg.Color(255, 0, 255), pg.Color(255, 255, 0), pg.Color(0, 0, 255)]
PLAYER_COLOR_RESPAWN = [pg.Color(0, 127, 0), pg.Color(127, 0, 127), pg.Color(127, 127, 0), pg.Color(0, 0, 127)]


# State machine constants
STATE_POP = 0 # for convenience, not really a state which we can be in
STATE_MENU = 1
STATE_PLAY = 2
STATE_STOP = 3 # not implemented yet
STATE_ENDGAME = 4


# view

WINDOW_CAPTION = 'Challenge 2022'
WINDOW_SIZE = (800, 800)
ARENA_SIZE = (800, 800)
ARENA_GRID_COUNT = 30
ARENA_GRID_SIZE = ARENA_SIZE[0] / ARENA_GRID_COUNT
BACKGROUND_COLOR = pg.Color('black')
PLAYER_COLOR = [pg.Color('green'), pg.Color('magenta'), pg.Color('yellow'), pg.Color('blue')]

PLAYER_PIC = {
    'G_BASIC':'green_basic.png',
    'G_SNIPER':'green_sniper.png',
    'G_MACHINE_GUN':'green_machine_gun.png',
    'G_SHOTGUN':'green_shotgun.png',
    'R_BASIC':'red_basic.png',
    'R_SNIPER':'red_sniper.png',
    'R_MACHINE_GUN':'red_machine_gun.png',
    'R_SHOTGUN':'red_shotgun.png',
    'Y_BASIC':'yellow_basic.png',
    'Y_SNIPER':'yellow_sniper.png',
    'Y_MACHINE_GUN':'yellow_machine_gun.png',
    'Y_SHOTGUN':'yellow_shotgun.png',
    'B_BASIC':'blue_basic.png',
    'B_SNIPER':'blue_sniper.png',
    'B_MACHINE_GUN':'blue_machine_gun.png',
    'B_SHOTGUN':'blue_shotgun.png'
}

BACKGROUND_PIC = 'Background.png'

WEAPON_PIC = {
    'SNIPER':'Sniper.png',
    'SHOTGUN':'Shotgun.png',
    'MACHINE_GUN':'Machine_Gun.png'
}

BUFF_PIC = {
    'ATTACK_CD':'Attack_CD.png',
    'AUX_LINE':'Aux_Line_Length.png',
    'REPULSION':'Repulsion.png'
}

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