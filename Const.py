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