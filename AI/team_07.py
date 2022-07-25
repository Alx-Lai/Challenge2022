AI_DIR_FORWARD      = 0
AI_DIR_BACKWARD     = 1
AI_DIR_LEFT         = 2
AI_DIR_RIGHT        = 3
AI_DIR_ATTACK       = 4
AI_DIR_STOP         = 5

ACTION_NONE = {'forward':False, 'backward':False, 'left':False, 'right':False, 'attack':False}

from math import atan2, pi, degrees
import math
import random
from turtle import position
import pygame



class TeamAI():
    def __init__(self, helper):
        self.helper = helper
        self.enhancement = [0,2,3,1] 
        self.action = ACTION_NONE.copy()
        self.rotating = False
        self.startDir = None
        self.count = 0
        self.count2 = 0
        self.not_item = False
        #self.redwall = self.helper.
    def decide(self):
        self.action = ACTION_NONE.copy()
        self.attack()
        
        # self.action['attack']=True
        
        pos = self.helper.get_self_position()
        dr = self.helper.get_self_direction()

        future_pos = pos + 3 * dr
        '''
        if self.rotating:
            
            vector_a = self.helper.get_self_direction()
            

            angle = math.acos((vector_a*vector_b) / (vector_a.magnitude() * vector_b.magnitude()))

            if abs(angle) < 0.1:
                self.rotating = False
            else:
                self.action['right']= True 
        '''    

        vector_a = self.helper.get_self_direction()
        vector_b = pygame.math.Vector2.normalize(self.helper.get_nearest_item_info()["position"]-self.helper.get_self_position())

        angle = math.acos((vector_a*vector_b) / (vector_a.magnitude() * vector_b.magnitude()))

        if abs(angle) > 0.1 and not self.not_item:
           self.action['right']= True  
        else:
            for wall in self.helper.get_wall_position():
            # print(((future_pos.x - wall.x) ** 2 + (future_pos.y - wall.y) ** 2)**0.5)
                if ((future_pos.x - wall.x) ** 2 + (future_pos.y - wall.y) ** 2)**0.5 < 2: # dis(future_pos, wall) < 2
                    self.action['right']= True
                    vector_a = pygame.math.Vector2.normalize(self.helper.get_nearest_item_info()["position"]-self.helper.get_self_position())
                    vector_b = pygame.math.Vector2.normalize(wall-self.helper.get_self_position())

                    angle = math.acos((vector_a*vector_b))
                    if angle < pi / 6:
                        self.not_item = True
                        self.count2 = 100 
                else:
                    self.action['forward']=True
                
                    
            '''
            if self.count >= 1000 and self.count <= 1150:
                self.action['right'] = True 
            elif self.count > 1150:
                self.count = 0
            '''
            if self.count2 <= 0:
                self.not_item = False
            self.count += 1
            self.count2 -= 1
            



        
        # self.action['forward']=True
        return self.action
    def attack(self):
        vector_a = self.helper.get_self_direction()
        vector_b = pygame.math.Vector2.normalize(self.helper.get_nearest_player_position()-self.helper.get_self_position())

        angle = math.acos((vector_a*vector_b) / (vector_a.magnitude() * vector_b.magnitude()))

        if abs(angle) < self.helper.get_self_basic_attack_accuracy() and  self.helper.get_self_next_attack() == 0:
            self.action['attack']= True     