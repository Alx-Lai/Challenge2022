import pygame

AI_DIR_FORWARD      = 0
AI_DIR_BACKWARD     = 1
AI_DIR_LEFT         = 2
AI_DIR_RIGHT        = 3
AI_DIR_ATTACK       = 4
AI_DIR_STOP         = 5

ACTION_NONE = {'forward':False, 'backward':False, 'left':False, 'right':False, 'attack':False}

import random

class TeamAI():
    def __init__(self, helper):
        self.helper = helper
        self.enhancement = [0,2,2,3]
        self.action = ACTION_NONE.copy()
        self.player_id = helper.get_self_id()
        self.place = self.helper.get_self_position()
        self.counter = 0
        self.rotate = 0
        self.wander = False
        self.face = self.helper.get_self_direction()
        self.close_enemy = self.helper.get_nearest_player_position()
        self.close_RE = self.helper.get_nearest_RE_position()
        self.want_face = pygame.Vector2(0,0)
        self.face_close_enemy = pygame.Vector2(0,0)

    
    def reset(self):
        self.action = ACTION_NONE.copy()

    def update(self):
        self.want_face = self.want_face = self.place - self.close_RE
    def auto_attack(self):

        if self.helper.get_self_next_attack() == 0:
            self.counter = 10
            self.action['attack'] = True
        if self.counter > 0:
            self.action['forward'] = True 
            self.counter -= 1
    
    def auto_wander(self):
        if self.wander == 0:
            if random.randint(0, 1000) == 0:
                self.wander = random.randint(150, 600)
        if self.wander > 0:
            self.action['forward'] = True
            self.wander -= 1

    def aim(self):
        self.face_close_enemy = self.close_enemy - self.face
        self.r_x=self.close_enemy[0] - self.face[0]
        self.r_y=self.close_enemy[1] - self.face[1]
         
        if self.face_close_enemy !=0:
            if self.r_x > 0:
                if self.r_y > self.r_x:
                    self.action['left'] = True
                elif self.r_y < self.r_x:
                    self.action['right'] = True
            elif self.r_x < 0:
                if self.r_y > self.r_x:
                    self.action['right'] = True
                elif self.rotate_y < self.rotate_x:
                    self.action['left'] = True

    def farfarfromRE(self):
        if (self.close_RE - self.place).length() <= 3:
            self.want_face = self.place - self.close_RE 
            self.rotate_x=self.want_face[0] - self.face[0]
            self.rotate_y=self.want_face[1] - self.face[1]
           
            if self.rotate_x > 0:
                if self.rotate_y > self.rotate_x:
                    self.action['left'] = True
                elif self.rotate_y < self.rotate_x:
                    self.action['right'] = True
            elif self.rotate_x < 0:
                if self.rotate_y > self.rotate_x:
                    self.action['right'] = True
                elif self.rotate_y < self.rotate_x:
                    self.action['left'] = True
            

        else:
            self.aim()
        
    # if < 90 degree, walk
    def dg_walk(self):
        if  pygame.Vector2.dot(self.want_face,self.face)<=0:
            self.action['forward'] = True
            self.update()

    		
    def decide(self):

        self.reset()
        self.dg_walk()
        self.farfarfromRE()
        if self.wander == 0:
            self.auto_attack()
        self.auto_wander()

        return self.action
