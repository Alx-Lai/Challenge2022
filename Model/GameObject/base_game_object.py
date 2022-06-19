import pygame as pg
import Const
import copy
import math
from pygame.math import Vector2

class Base_Circle_Object:
    '''
    An abstract class for circle game objects.
    '''
    def __init__(self, model, position, radius):
        self.model = model
        self.radius = radius
        self.position = position
        self.direction = Vector2(1.0, 0.0) # facing rightward
        self.speed = Vector2(0.0, 0.0)
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
        Run whenever EventEveryTick() arises.
        '''
        self.lifespam -= 1
        self.position += self.speed / Const.FPS
        self.clip_position()

    def collide_object(self, obj):
        '''
        Check if the object collides with another one.
        '''
        if isinstance(obj, Base_Circle_Object):
            return (self.position - obj.position).length_squared() <= (self.radius + obj.radius) ** 2
        if isinstance(obj, Base_Square_Object):
            dx = (self.position - obj.position).x
            dy = (self.position - obj.position).y
            if abs(dx) > obj.radius + self.radius or abs(dy) > obj.radius + self.radius:
                return False
            if abs(dx) <= obj.radius or abs(dy) <= obj.radius:
                return True
            corner = obj.position + obj.radius * Vector2((dx>0)-(dx<0), (dy>0)-(dy<0))
            return (corner - self.position).length_squared() <= self.radius ** 2
    
    def kill(self):
        '''
        Kill the object.
        '''
        self.__death = True

    def killed(self):
        '''
        Check if the object has been killed.
        '''
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


class Base_Square_Object:
    '''
    An abstract class for square game objects.
    '''
    def __init__(self, model, position, radius):
        self.model = model
        self.radius = radius
        self.position = position
        self.direction = Vector2(1.0, 0.0) # facing rightward
        self.speed = Vector2(0.0, 0.0)
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
        Run whenever EventEveryTick() arises.
        '''
        self.lifespam -= 1
        self.position += self.speed / Const.FPS
        self.clip_position()

    def collide_object(self, obj):
        '''
        Check if the object collides with another one.
        '''
        if isinstance(obj, Base_Circle_Object):
            dx = (obj.position - self.position).x
            dy = (obj.position - self.position).y
            if abs(dx) > self.radius + obj.radius or abs(dy) > self.radius + obj.radius:
                return False
            if abs(dx) <= self.radius or abs(dy) <= self.radius:
                return True
            corner = self.position + self.radius * Vector2((dx>0)-(dx<0), (dy>0)-(dy<0))
            return (corner - obj.position).length_squared() <= obj.radius ** 2
        if isinstance(obj, Base_Square_Object):
            dx = (obj.position - self.position).x
            dy = (obj.position - self.position).y
            return abs(dx) <= self.radius + obj.radius and abs(dy) <= self.radius + obj.radius
    
    def kill(self):
        '''
        Kill the object.
        '''
        self.__death = True

    def killed(self):
        '''
        Check if the object has been killed.
        '''
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