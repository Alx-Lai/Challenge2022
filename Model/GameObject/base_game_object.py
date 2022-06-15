import pygame as pg
import Const
import copy
import math
from pygame.math import Vector2

class Base_Game_Object:
    '''
    An abstract class for game objects.
    '''
    def __init__(self, model, position, radius):
        self.model = model
        self.position = position
        self.radius = radius
        self.direction = Vector2(1.0, 0.0) # facing rightwards
        self.speed = Vector2(0.0, 0.0)
        self.bounce = False
        self.__death = False
        self.lifespam = math.inf

    def clip_position(self):
        '''
        Clip the object's position to make it stay in the screen.
        '''
        self.x = max(self.radius, min(Const.ARENA_GRID_COUNT - self.radius, self.x))
        self.y = max(self.radius, min(Const.ARENA_GRID_COUNT - self.radius, self.y))

    def tick(self):
        '''
        Take actions in every tick.
        '''
        self.lifespam -= 1
        self.position += self.speed / Const.FPS

        if self.bounce:
            if self.x < self.radius or Const.ARENA_GRID_COUNT - self.radius < self.x:
                self.speed.x = -self.speed.x
            if self.y < self.radius or Const.ARENA_GRID_COUNT - self.radius < self.y:
                self.speed.y = -self.speed.y

        self.clip_position()

    def collide_object(self, obj):
        '''
        Check if the object collides with another
        '''
        return (self.position - obj.position).length_squared() <= (self.radius + obj.radius) ** 2
    
    def kill(self):
        '''
        Kill the object.
        '''
        self.__death = True

    def killed(self):
        return self.__death


    @property
    def x(self):
        return self.position.x
    @x.setter
    def x(self, value):
        self.position.x = value
    
    @property
    def y(self):
        return self.position.y
    @y.setter
    def y(self, value):
        self.position.y = value