import math
import pygame as pg
import Map.map_1 as mp # Change map HERE

# model
# length unit: a unit grid's size (L)
# time unit: frame (T)

FPS = 60 # frame per second
GAME_LENGTH = 100 * FPS # temporarily set to infinity
PLAYER_NUMBER = 4
PLAYER_INIT_POSITION = [pg.Vector2(9.5, 9.5), pg.Vector2(20.5, 9.5), pg.Vector2(9.5, 20.5), pg.Vector2(20.5, 20.5)]

PLAYER_RADIUS = 0.5                       # L
PLAYER_BASE_SPEED = 10 / FPS              # L / T
PLAYER_ROTATION_SPEED = 3 / FPS           # radian / T
PLAYER_REPULSION_RESISTANCE = 0

PLAYER_ATTACK_SPEED = 0.5                 # bullet / T
PLAYER_ATTACK_KICK = 1 / 10               # speed 
PLAYER_ATTACK_ACCURACY = 0.25             # radian
PLAYER_ATTACK_AMMO = 1                    # bullet
PLAYER_AUX_LINE_LENGTH = 1                # L

PLAYER_QUOTA_ATTACK_SPEED = 5
PLAYER_QUOTA_REPULSION = 5
PLAYER_QUOTA_ATTACK_ACCURACY = 5

PLAYER_RESPAWN_TIME = 5 * FPS             # T
PLAYER_MAX_RESPAWN_COUNT = [2, 2, 2, 2]
PLAYER_INIT_DEATH_CNT = 0
PLAYER_ALIVE_SCORE = [0, 100, 200, 300]

BULLET_RADIUS = 0.2                       # L
BULLET_REPULSION = 3 / 10                 # speed
BULLET_SPEED = 15 / FPS                   # L / T
BULLET_LIFESPAN = 6 * FPS                 # T
BULLET_TRACE_TIME = 0.1 * FPS             # T
BULLET_HIT_SCORE = 10

GUN_TYPE_NORMAL_GUN = 0
GUN_TYPE_MACHINE_GUN = 1
GUN_TYPE_SNIPER = 2
GUN_TYPE_SHOTGUN = 3

GUN_USE_TIME = [math.inf * FPS, 10 * FPS, 20 * FPS, 20 * FPS] # T
GUN_ATTACK_SPEED_MULTIPLIER = [1, 4, 1, 1]
GUN_ATTACK_KICK_MULTIPLIER = [1, 1/4, 1.5, 1]
GUN_ATTACK_AMMO_MULTIPLIER = [1, 1, 1, 5]
GUN_AUX_LINE_LENGTH_MULTIPLIER = [1, 1, 1, 1]
GUN_BULLET_LIFESPAN_MULTIPLIER = [1, 1, 2, 1]
GUN_BULLET_TRACE_TIME_MULTIPLIER = [1, 1, 2, 0.6]
GUN_BULLET_REPULSION_MULTIPLIER = [1, 1/3, 2, 1]
GUN_BULLET_ACCURACY_MULTIPLIER = [1, 1, 0.1, 2]

SHOTGUN_SPREAD_ANGLE = math.pi / 36       # radian

BUFF_TYPE_ATTACK_SPEED = 4
BUFF_TYPE_REPULSION = 5
BUFF_TYPE_ATTACK_ACCURACY = 6

BUFF_VALUE_ATTACK_SPEED = 0.2             # bullet / T
BUFF_VALUE_REPULSION = 4 / FPS            # L / T
BUFF_VALUE_ATTACK_ACCURACY = -0.04        # radian

ITEM_GENERATOR_COOLDOWN = 1 * FPS         # T
ITEM_MAX = 10
ITEM_GUN_RADIUS = 0.5                     # L
ITEM_BUFF_RADIUS = 0.5                    # L

OBSTACLE_RADIUS = 0.5                     # L
RE_FIELD_RADIUS = 0.5                     # L
OBSTACLE_POSITION = mp.OBSTACLE_POSITION
RE_FIELD_POSITION = mp.RE_FIELD_POSITION

ENHANCEMENT_BASE_SPEED = 0.01
ENHANCEMENT_ATTACK_SPEED = 0.01
ENHANCEMENT_BULLET_REPULSION = 0.01
ENHANCEMENT_REPULSION_RESISTANCE = 0.01

# view
WINDOW_CAPTION = 'Challenge 2022'
WINDOW_SIZE = (900, 900)
ARENA_SIZE = (900, 900)
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
