import pygame as pg
import copy
import Const
from Model.GameObject.base_game_object import *

class Bullet(Base_Game_Object):
    '''
    Represent a bullet shot by a gun.
    '''
    def __init__(self, model, player, direction, trace_time, repulsion, gun_type):
        position = player.position + direction * (Const.PLAYER_RADIUS * 2)
        super().__init__(model, position, Const.BULLET_RADIUS)

        self.tail = Bullet_Tail(model, self, player, direction, trace_time)
        self.model.bullets.append(self.tail)
        self.vertices = [self.position, self.tail.position]

        self.attacker = player
        self.gun_type = gun_type
        self.speed = direction * Const.BULLET_SPEED
        self.repulsion = repulsion

        self.lifespam = Const.BULLET_LIFESPAM * Const.FPS

    def tick(self):
        '''
        Run whenever EventEveryTick() arises.
        '''
        self.position += self.speed / Const.FPS
        self.bounce()

        self.lifespam -= 1
        if self.lifespam <= 0:
            self.kill()

        for player in self.model.players:
            if self.trace_collide_object(player):
                player.knock_back(self.repulsion, self.speed.normalize())
                if player.player_id != self.attacker.player_id:
                    self.attacker.score += Const.BULLET_HIT_SCORE
                self.kill()

    def bounce(self):
        '''
        Bounce against the arena border.
        '''
        bounced = False
        if self.x < self.radius or Const.ARENA_GRID_COUNT - self.radius < self.x:
            self.speed.x = -self.speed.x
            bounced = True
        if self.y < self.radius or Const.ARENA_GRID_COUNT - self.radius < self.y:
            self.speed.y = -self.speed.y
            bounced = True
        
        if bounced:
            self.clip_position()
            self.vertices.insert(1, copy.deepcopy(self.position))

    def trace_collide_object(self, obj):
        '''
        Check if the bullet and its trace collide with another object.
        '''
        # check vertices
        for pos in self.vertices:
            if (pos - obj.position).length_squared() <= (self.radius + obj.radius) ** 2:
                return True

        # check segments
        for p1, p2 in zip(self.vertices, self.vertices[1:]):
            x12, y12 =  p1.x - p2.x,  p1.y - p2.y
            x01, y01 = obj.x - p1.x, obj.y - p1.y
            x02, y02 = obj.x - p2.x, obj.y - p2.y

            # the line segment degenerates into a point
            if x12 == 0 and y12 == 0: continue

            # the bullet does not reach the line
            a, b, c = y12, -x12, x12*p1.y - y12*p1.x
            if (a*obj.x + b*obj.y + c)**2 > (obj.radius**2) * (a**2 + b**2): continue
            
            # the bullet does not reach the line segment
            if x12*x02 + y12*y02 < 0 or -x12*x01 + -y12*y01 < 0: continue
            return True

        return False
    
    def kill(self):
        '''
        Kill the bullet and its trace tail.
        '''
        super().kill()
        self.tail.kill()


class Bullet_Tail(Base_Game_Object):
    '''
    Represent the tail of a bullet's trace.
    '''
    def __init__(self, model, head, player, direction, trace_time):
        position = player.position + direction * (Const.PLAYER_RADIUS * 2)
        super().__init__(model, position, Const.BULLET_RADIUS)

        self.speed = direction * Const.BULLET_SPEED
        self.head = head
        self.trace_time = trace_time * Const.FPS

    def tick(self):
        '''
        Run whenever EventEveryTick() arises.
        '''
        if self.trace_time > 0:
            self.trace_time -= 1
            return
        
        self.position += self.speed / Const.FPS
        self.bounce()

    def bounce(self):
        '''
        Bounce against the arena border.
        '''
        bounced = False
        if self.x < self.radius or Const.ARENA_GRID_COUNT - self.radius < self.x:
            self.speed.x = -self.speed.x
            bounced = True
        if self.y < self.radius or Const.ARENA_GRID_COUNT - self.radius < self.y:
            self.speed.y = -self.speed.y
            bounced = True
        
        if bounced:
            self.clip_position()
            self.head.vertices.pop(-2)