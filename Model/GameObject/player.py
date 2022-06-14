from Model.GameObject.bullet import *
import Const

class Player:
    def __init__(self, model, player_id: int):
        self.model = model
        self.player_id = player_id
        self.position = Const.PLAYER_INIT_POSITION[player_id] # is a pg.Vector2
        self.direction = Const.PLAYER_INIT_DIRECTION[player_id] # is a pg.Vector2
        self.speed = Const.PLAYER_SPEED
        self.score = 0

        self.attack_cd = Const.PLAYER_ATTACK_CD
        self.attack_kick = Const.PLAYER_ATTACK_KICK
        self.aux_line_length = 1
        self.cd_time = 0

        self.bullet_length = Const.BULLET_LENGTH
        self.bullet_repulsion = Const.BULLET_REPULSION
    
    def tick(self):
        if self.in_cd():
            self.cd_time -= 1 / Const.FPS

    def move_direction(self, direction: int):
        '''
        Move the player along the direction by its speed.
        Will automatically clip the position so no need to worry out-of-bound moving.
        '''
        # Modify position of player
        self.position += self.speed * Const.ARENA_GRID_SIZE / Const.FPS * self.direction * direction

        # clipping
        self.position.x = max(0, min(Const.ARENA_SIZE[0], self.position.x))
        self.position.y = max(0, min(Const.ARENA_SIZE[1], self.position.y))

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
        self.position += Const.ARENA_GRID_SIZE * distance * direction

        # clipping
        self.position.x = max(0, min(Const.ARENA_SIZE[0], self.position.x))
        self.position.y = max(0, min(Const.ARENA_SIZE[1], self.position.y))


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