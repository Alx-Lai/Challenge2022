import Const
from EventManager.EventManager import *
from Model.GameObject.base_game_object import *
from Model.Gun.gun import *

class Player(Base_Circle_Object):
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

        self.quota_attack_cd = Const.PLAYER_QUOTA_ATTACK_CD
        self.quota_repulsion = Const.PLAYER_QUOTA_REPULSION
        self.quota_aux_line_length = Const.PLAYER_QUOTA_AUX_LINE_LENGTH

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
        '''
        Switch the player's gun.
        '''
        match gun_type:
            case Const.GUN_TYPE_NORMAL_GUN:
                self.gun = Normal_Gun(self.model, self)
            case Const.GUN_TYPE_MACHINE_GUN:
                self.gun = Machine_Gun(self.model, self)
            case Const.GUN_TYPE_SNIPER:
                self.gun = Sniper(self.model, self)
            case Const.GUN_TYPE_SHOTGUN:
                self.gun = Shotgun(self.model, self)
        self.model.ev_manager.post(EventPlayerSwitchGun(self.player_id, gun_type))

    def quota_enough(self, buff_type):
        '''
        Check if the quota of a buff is enough
        '''
        match buff_type:
            case Const.BUFF_TYPE_ATTACK_CD:
                return self.quota_attack_cd > 0
            case Const.BUFF_TYPE_REPULSION:
                return self.quota_repulsion > 0
            case Const.BUFF_TYPE_AUX_LINE_LENGTH:
                return self.quota_aux_line_length > 0


    def buff(self, buff_type):
        '''
        Add permanent buff to the player.
        '''
        match buff_type:
            case Const.BUFF_TYPE_ATTACK_CD:
                self.attack_cd += Const.BUFF_VALUE_ATTACK_CD
                self.quota_attack_cd -= 1
            case Const.BUFF_TYPE_REPULSION:
                self.bullet_repulsion += Const.BUFF_VALUE_REPULSION
                self.quota_repulsion -= 1
            case Const.BUFF_TYPE_AUX_LINE_LENGTH:
                self.aux_line_length += Const.BUFF_VALUE_AUX_LINE_LENGTH
                self.quota_aux_line_length -= 1
        self.model.ev_manager.post(EventPlayerBuffed(self.player_id, buff_type))
