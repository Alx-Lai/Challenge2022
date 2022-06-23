import Const
from EventManager.EventManager import *
from Model.GameObject.base_game_object import *
from pygame.math import Vector2

class Obstacle(Base_Square_Object):
    '''
    Represent an obstacle that block every object's movement.
    '''
    def __init__(self, model, position, radius):
        super().__init__(model, position, radius)
    
    def clip_object_position(self, obj):
        '''
        Clip an collided object's position to avoid overlapping
        '''
        if not isinstance(obj, Base_Circle_Object): return None
        if not self.collide_object(obj): return None

        dx = (obj.position - self.position).x
        dy = (obj.position - self.position).y
        if abs(dx) < self.radius or abs(dy) < self.radius:
            if abs(dx) > abs(dy):
                obj.x = self.x + (self.radius + obj.radius) * ((dx>0)-(dx<0))
                return Vector2(1, 0)
            else:
                obj.y = self.y + (self.radius + obj.radius) * ((dy>0)-(dy<0))
                return Vector2(0, 1)
        else:
            corner = self.position + self.radius * Vector2((dx>0)-(dx<0), (dy>0)-(dy<0))
            direction = obj.position - corner
            direction.scale_to_length(obj.radius)
            obj.position = corner + direction
            return direction.normalize()


class RE_Field(Obstacle):
    '''
    Represent an obstacle that block every object's movement.
    If a player rams into it, the player dies.
    '''
    def __init__(self, model, position, radius):
        super().__init__(model, position, radius)