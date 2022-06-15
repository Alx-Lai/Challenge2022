import Const
from Model.GameObject.bullet import *
from Model.GameObject.base_game_object import *

class Player(Base_Game_Object):
    def __init__(self, model, player_id: int):
        super().__init__(model, Const.PLAYER_INIT_POSITION[player_id], Const.PLAYER_RADIUS)

        self.player_id = player_id
        self.score = 0

        self.attack_cd = Const.PLAYER_ATTACK_CD
        self.attack_kick = Const.PLAYER_ATTACK_KICK
        self.aux_line_length = 1
        self.cd_time = 0

        self.bullet_length = Const.BULLET_LENGTH
        self.bullet_repulsion = Const.BULLET_REPULSION
    
    def tick(self):
        super().tick()
        if self.in_cd():
            self.cd_time -= 1 / Const.FPS

    def move_direction(self, direction: int):
        '''
        Adjust the player's speed.
        '''
        # Modify position of player
        new_speed = Const.PLAYER_BASE_SPEED / Const.FPS * self.direction * direction
        self.speed = (self.speed * 4 + new_speed) / 5

    def rotate(self, direction: int):
        '''
        Rotate the player leftward or rightward.
        '''
        self.direction = self.direction.rotate_rad(Const.PLAYER_ROTATION_SPEED / Const.FPS * direction)

    def knock_back(self, distance, direction):
        '''
        Repulse the player along the opposite direction of its speed.
        Will automatically clip the position so no need to worry out-of-bound moving.
        '''
        # Modify position of player
        self.speed += distance * direction * 10


    def attack(self):
        '''
        Fire a bullet towards the player's facing direction.
        '''
        if self.in_cd():
            return
        self.cd_time = self.attack_cd
        self.knock_back(self.attack_kick, -self.direction)
        self.model.bullets.append(Bullet(self.model, self, self.bullet_length, self.bullet_repulsion))
    
    def in_cd(self):
        return self.cd_time > 0