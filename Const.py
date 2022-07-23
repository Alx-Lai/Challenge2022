import math
import pygame as pg

# model
# length unit: a unit grid's size (L)
# time unit: frame (T)

FPS = 60 # frame per second
GAME_LENGTH = 120 * FPS                   # T
PLAYER_NUMBER = 4
PLAYER_INIT_POSITION = [pg.Vector2(9.5, 9.5), pg.Vector2(20.5, 9.5), pg.Vector2(9.5, 20.5), pg.Vector2(20.5, 20.5)]

PLAYER_RADIUS = 0.5                       # L
PLAYER_BASE_SPEED = 2 / FPS               # L / T
PLAYER_ROTATION_SPEED = 2 / FPS           # radian / T
PLAYER_REPULSION_RESISTANCE = 0

PLAYER_ATTACK_SPEED = 0.5                 # bullet / T
PLAYER_ATTACK_KICK = 2 / 10               # speed 
PLAYER_ATTACK_ACCURACY = 0.25             # radian
PLAYER_ATTACK_AMMO = 1                    # bullet
PLAYER_AUX_LINE_LENGTH = 1                # L

PLAYER_QUOTA_ATTACK_SPEED = 5
PLAYER_QUOTA_REPULSION = 5
PLAYER_QUOTA_ATTACK_ACCURACY = 5

PLAYER_RESPAWN_TIME = 5 * FPS  # T
PLAYER_MAX_RESPAWN_COUNT = [2, 2, 2, 2]
PLAYER_ALIVE_SCORE = [0, 100, 200, 300]

BULLET_RADIUS = 0.2                       # L
BULLET_REPULSION = 2 / 10                 # speed
BULLET_SPEED = 15 / FPS                   # L / T
BULLET_LIFESPAN = 3 * FPS                 # T
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
BUFF_VALUE_REPULSION = 0.4 / 10           # speed
BUFF_VALUE_ATTACK_ACCURACY = -0.04        # radian

ITEM_GENERATOR_COOLDOWN = 1 * FPS         # T
ITEM_MAX = 10
ITEM_GUN_RADIUS = 0.5                     # L
ITEM_BUFF_RADIUS = 0.5                    # L

OBSTACLE_RADIUS = 0.5                     # L
RE_FIELD_RADIUS = 0.5                     # L

ENHANCEMENT_BASE_SPEED = 0.01
ENHANCEMENT_ATTACK_SPEED = 0.01
ENHANCEMENT_BULLET_REPULSION = 0.01
ENHANCEMENT_REPULSION_RESISTANCE = 0.01

# view
WINDOW_CAPTION = 'Challenge 2022'
WINDOW_SIZE = (1000, 900)
ARENA_SIZE = (900, 900)
ARENA_GRID_COUNT = 30
ARENA_GRID_SIZE = ARENA_SIZE[0] / ARENA_GRID_COUNT
BACKGROUND_COLOR = pg.Color('black')
BACKGROUND_COLOR_SPEED = 20
BACKGROUND_COLOR_CHANGE = [pg.Color(0, 0, 100), pg.Color(0, 100, 0), pg.Color(100, 0, 0), pg.Color(100, 100, 0)]
SCORE_COLOR = [pg.Color(47, 141, 255), pg.Color(0, 255, 0), pg.Color(255, 0, 0), pg.Color(255, 255, 0)]
PLAYER_COLOR = [pg.Color(0, 0, 255), pg.Color(0, 255, 0), pg.Color(255, 0, 0), pg.Color(255, 255, 0)]
PLAYER_COLOR_RESPAWN = [pg.Color(0, 127, 0), pg.Color(127, 0, 127), pg.Color(127, 127, 0), pg.Color(0, 0, 127)]
PLAYER_IMAGE_ZOOM = 2.0

#IMAGE PATH
PLAYER_IMAGE_PATH = [["./View/source/blue_basic.png","./View/source/blue_machine_gun.png","./View/source/blue_sniper.png","./View/source/blue_shotgun.png"],
                    ["./View/source/green_basic.png","./View/source/green_machine_gun.png","./View/source/green_sniper.png","./View/source/green_shotgun.png"],
                    ["./View/source/red_basic.png","./View/source/red_machine_gun.png","./View/source/red_sniper.png","./View/source/red_shotgun.png"],
                    ["./View/source/yellow_basic.png","./View/source/yellow_machine_gun.png","./View/source/yellow_sniper.png","./View/source/yellow_shotgun.png"]]
BUFF_ATTACK_CD_PATH = "./View/source/Attack_CD.png"
BUFF_REPULSION_PATH = "./View/source/Repulsion.png"
BUFF_AUX_lINE_PATH = "./View/source/Aux_line_Length.png"
SHOT_GUN_PATH = "./View/source/Shotgun.png"
SNIPER_PATH = "./View/source/Sniper.png"
MACHINE_GUN_PATH = "./View/source/Machine_Gun.png"
NORMAL_FIELD_PATH = "./View/source/normal_field_1.png"
RE_FIELD_PATH = "./View/source/RE_field_1.png"
CROWN_PATH = "./View/source/crown.png"
SCORE_BACKGROUND_PATH = "./View/source/score_background.png"
BACKGROUND_TOP_PATH = "./View/source/Background_top_1.png"
BACKGROUND_PATH = "./View/source/Background.png"
MENU_PATH = "./View/source/Menu.png"

#SOUND PATH
MENU_MUSIC_PATH = "./View/source/Everen Maxwell - Hyperphantasia [NCS Release].mp3"
BACKGROUND_MUSIC_PATH = "./View/source/background_beta.mp3"
NORMAL_GUN_SOUND_PATH = "./View/source/normal_gun.mp3"
SNIPER_SOUND_PATH = "./View/source/sniper.mp3"
SHOT_GUN_SOUND_PATH = "./View/source/shotgun.mp3"
MACHINE_GUN_SOUND_PATH = "./View/source/machine_gun.mp3"
PLAYER_DIED_SOUND_PATH = "./View/source/player_died.wav"
PLAYER_KILLED_SOUND_PATH = "./View/source/player_killed.mp3"
PLAYER_HIT_SOUND_PATH = "./View/source/wall_bump.mp3"
PLAYER_HIT_WALL_SOUND_PATH = "./View/source/wall_bump.mp3"
PLAYER_PICKUP_ITEM_SOUND_PATH = "./View/source/pick_up_item.mp3"
PLAYER_SWITCH_GUN_SOUND_PATH = "./View/source/switch_weapon.mp3"

# State machine constants
STATE_POP = 0  # for convenience, not really a state which we can be in
STATE_MENU = 1
STATE_PLAY = 2
STATE_STOP = 3 
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

# API
API_TIMEOUT = 1/6/FPS