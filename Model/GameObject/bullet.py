import pygame as pg
import copy
import Const
from EventManager.EventManager import *
from Model.GameObject.base_game_object import *

class Bullet(Base_Circle_Object):
    '''
    Represent a bullet shot by a gun.
    '''
    def __init__(self, model, player, direction, trace_time, repulsion, gun_type):
        super().__init__(model, copy.deepcopy(player.position), Const.BULLET_RADIUS)

        self.tail = Bullet_Tail(model, self, player, direction, trace_time)
        self.model.bullets.append(self.tail)
        self.vertices = []

        self.attacker = player
        self.attacker_proof = True
        self.gun_type = gun_type
        self.speed = direction * Const.BULLET_SPEED
        self.repulsion = repulsion

        self.lifespam = Const.BULLET_LIFESPAM

    def tick(self):
        '''
        Run whenever EventEveryTick() arises.
        '''
        self.position += self.speed
        self.bounce()

        self.lifespam -= 1
        if self.lifespam <= 0:
            self.kill()
        
        if self.attacker_proof and not self.trace_collide_object(self.attacker):
            self.attacker_proof = False

        for player in self.model.players:
            if not player.invisible() and self.trace_collide_object(player) \
                    and not (self.attacker_proof and player.player_id == self.attacker.player_id):
                player.knock_back(self.repulsion, self.speed.normalize())
                if player.player_id != self.attacker.player_id:
                    self.attacker.score += Const.BULLET_HIT_SCORE
                self.model.ev_manager.post(EventPlayerGetHit(player.player_id, self.attacker.player_id))
                self.kill()
        
        collide_edge = False # whether the bullet collides the edges of the obstacles (instead of the corners)
        collided_obstacle = None
        for obstacle in self.model.obstacles:
            if self.collide_object(obstacle):
                dx = (self.position - obstacle.position).x
                dy = (self.position - obstacle.position).y
                if abs(dx) < obstacle.radius or abs(dy) < obstacle.radius:
                    collide_edge = True
                    collided_obstacle = obstacle
                elif not collide_edge:
                    collided_obstacle = obstacle
        if collided_obstacle:
            normal_vector = collided_obstacle.clip_object_position(self)
            self.speed = self.speed.reflect(normal_vector)
            self.vertices.insert(0, copy.deepcopy(self.position))

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
            self.vertices.insert(0, copy.deepcopy(self.position))

    def trace_collide_object(self, obj):
        '''
        Check if the bullet and its trace collide with another object.
        '''
        vertices = [self.position] + self.vertices + [self.tail.position]
        # check vertices
        for pos in vertices:
            if (pos - obj.position).length_squared() <= (self.radius + obj.radius) ** 2:
                return True

        # check segments
        for p1, p2 in zip(vertices, vertices[1:]):
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


class Bullet_Tail(Base_Circle_Object):
    '''
    Represent the tail of a bullet's trace.
    '''
    def __init__(self, model, head, player, direction, trace_time):
        super().__init__(model, copy.deepcopy(player.position), Const.BULLET_RADIUS)

        self.speed = direction * Const.BULLET_SPEED
        self.head = head
        self.trace_time = trace_time

    def tick(self):
        '''
        Run whenever EventEveryTick() arises.
        '''
        if self.trace_time > 0:
            self.trace_time -= 1
            return
        
        self.position += self.speed
        self.bounce()

        collide_edge = False # whether the bullet collides the edges of the obstacles (instead of the corners)
        collided_obstacle = None
        for obstacle in self.model.obstacles:
            if self.collide_object(obstacle):
                dx = (self.position - obstacle.position).x
                dy = (self.position - obstacle.position).y
                if abs(dx) < obstacle.radius or abs(dy) < obstacle.radius:
                    collide_edge = True
                    collided_obstacle = obstacle
                elif not collide_edge:
                    collided_obstacle = obstacle
        if collided_obstacle:
            normal_vector = collided_obstacle.clip_object_position(self)
            self.speed = self.speed.reflect(normal_vector)
            self.head.vertices.pop(-1)

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
            self.head.vertices.pop(-1)