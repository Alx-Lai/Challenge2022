import Const
import pygame as pg

class Bullet:
    def __init__(self, model, player, length, repulsion):
        self.model = model
        self.attacker = player
        self.position = player.position + player.direction * (Const.PLAYER_RADIUS + Const.BULLET_RADIUS) * Const.ARENA_GRID_SIZE
        self.direction = player.direction
        self.length = length
        self.repulsion = repulsion

        self.speed = Const.BULLET_SPEED
        self.lifespam = Const.BULLET_LIFESPAM

        self.__death = False

    def tick(self):
        self.move()
        if self.lifespam <= 0:
            self.kill()
        for player in self.model.players:
            if self.collide_player(player):
                player.knock_back(self.repulsion, self.direction)
                if player.player_id != self.attacker.player_id:
                    self.attacker.score += Const.BULLET_HIT_SCORE
                self.kill()


    def move(self):
        '''
        Move the bullet along the direction of its speed.
        Will automatically clip the position and reflect so no need to worry out-of-bound moving.
        '''
        self.position += self.speed * Const.ARENA_GRID_SIZE / Const.FPS * self.direction
        self.lifespam -= self.speed / Const.FPS

        if self.position.x < 0 or Const.ARENA_SIZE[0] < self.position.x:
            self.direction = self.direction.reflect(pg.math.Vector2(1, 0))
        if self.position.y < 0 or Const.ARENA_SIZE[1] < self.position.y:
            self.direction = self.direction.reflect(pg.math.Vector2(0, 1))

        self.position.x = max(0, min(Const.ARENA_SIZE[0], self.position.x))
        self.position.y = max(0, min(Const.ARENA_SIZE[1], self.position.y))
    
    def collide_player(self, player):
        return (self.position - player.position).length_squared() <= (Const.PLAYER_RADIUS * Const.ARENA_GRID_SIZE) ** 2

    def kill(self):
        self.__death = True

    def killed(self):
        return self.__death