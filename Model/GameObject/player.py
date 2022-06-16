import Const
from Model.GameObject.base_game_object import *
from Model.Gun.gun import *

class Player(Base_Game_Object):
    '''
    Represent a player.
    '''
    def __init__(self, model, player_id: int):
        super().__init__(model, Const.PLAYER_INIT_POSITION[player_id], Const.PLAYER_RADIUS)

        self.player_id = player_id
        self.score = 0
        self.gun = Normal_Gun(model, self)

        self.attack_cd = Const.PLAYER_ATTACK_CD
        self.attack_kick = Const.PLAYER_ATTACK_KICK
        self.aux_line_length = Const.PLAYER_AUX_LINE_LENGTH

        self.bullet_trace_time = Const.BULLET_TRACE_TIME
        self.bullet_repulsion = Const.BULLET_REPULSION

    def tick(self):
        '''
        Run whenever EventEveryTick() arises.
        '''
        super().tick()
        self.gun.tick()

    def move_direction(self, direction: int):
        '''
        Increase the player's speed along it's facing direction.
        Can move either forward or backward.
        '''
        new_speed = Const.PLAYER_BASE_SPEED * self.direction * direction
        self.speed = (self.speed * 9 + new_speed) / 10

    def stop_moving(self):
        '''
        Decrease the player's speed.
        '''
        self.speed = (self.speed * 9) / 10

    def rotate(self, direction: int):
        '''
        Rotate the player leftward or rightward.
        '''
        self.direction = self.direction.rotate_rad(Const.PLAYER_ROTATION_SPEED / Const.FPS * direction)

    def knock_back(self, distance, direction):
        '''
        Repulse the player along the given direction.
        '''
        self.speed += distance * direction

    def attack(self):
        '''
        Fire a bullet towards the player's facing direction.
        '''
        self.gun.shoot()
    
    def switch_gun(self, gun_type):
        match gun_type:
            case Const.GUN_TYPE_NORMAL_GUN:
                self.gun = Normal_Gun(self.model, self)
            case Const.GUN_TYPE_MACHINE_GUN:
                self.gun = Machine_Gun(self.model, self)
            case Const.GUN_TYPE_SNIPER:
                self.gun = Sniper(self.model, self)
            case Const.GUN_TYPE_SHOTGUN:
                self.gun = Shotgun(self.model, self)