import Const
from Model.GameObject.bullet import *
from Model.GameObject.base_game_object import *

class Player(Base_Game_Object):
    '''
    Represent a player.
    '''
    def __init__(self, model, player_id: int):
        super().__init__(model, Const.PLAYER_INIT_POSITION[player_id], Const.PLAYER_RADIUS)

        self.player_id = player_id
        self.score = 0

        self.attack_cd = Const.PLAYER_ATTACK_CD
        self.attack_kick = Const.PLAYER_ATTACK_KICK
        self.aux_line_length = 1
        self.cd_time = 0

        self.bullet_trace_time = Const.BULLET_TRACE_TIME
        self.bullet_repulsion = Const.BULLET_REPULSION
    
    def tick(self):
        '''
        Run whenever EventEveryTick() arises.
        '''
        super().tick()
        if self.in_cd():
            self.cd_time -= 1

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
        if self.in_cd():
            return
        self.cd_time = self.attack_cd * Const.FPS
        self.knock_back(self.attack_kick, -self.direction)
        self.model.items.append(Bullet(self.model, self, self.bullet_trace_time, self.bullet_repulsion))
    
    def in_cd(self):
        '''
        Check if the player is waiting for the cooldown.
        '''
        return self.cd_time > 0