AI_DIR_FORWARD      = 0
AI_DIR_BACKWARD     = 1
AI_DIR_LEFT         = 2
AI_DIR_RIGHT        = 3
AI_DIR_ATTACK       = 4
AI_DIR_STOP         = 5
 
ACTION_NONE = {'forward':False, 'backward':False, 'left':False, 'right':False, 'attack':False}
from enum import auto
from math import *
#import time
 
class TeamAI():
    def __init__(self, helper):
        self.helper = helper
        self.enhancement = [2,0,0,1] 
        self.action = ACTION_NONE.copy()
        self.wander = False
 
    def reset(self):
        self.action = ACTION_NONE.copy()
    
    def decide(self):
        selfid =  self.helper.get_self_id()
        ids = []
        ids = self.helper.get_player_id()
 
        for i in self.helper.get_player_id():
            if i != selfid:
               #print(self.helper.get_player_position()[ids[i]])
               pass
        self.reset()
        self.item_info()
        self.forward()
        
        return self.action
    def auto_attack(self):
        indexx = self.helper.get_nearest_RE_position()[0]-self.helper.get_self_position()[0]
        indexy = self.helper.get_nearest_RE_position()[1]-self.helper.get_self_position()[1]
        lenth = sqrt(indexx**2 + indexy**2)  
        if self.helper.get_self_next_attack() == 0:
            self.counter = 20
            self.action['attack'] = True
        if self.counter > 0:
            self.action['forward'] = True 
            self.counter -= 1
        if indexx + self.helper.get_self_direction()[0] == 0 and indexy + self.helper.get_self_direction()[1] == 0:
            self.action['attack'] = False

    def item_info(self):
        nearest_item_info = []
    def forward(self):
        vector_A = self.helper.get_self_direction()
        vector_AB = self.helper.get_nearest_item_info()['position'] - self.helper.get_self_position()
        theta = acos(vector_A*vector_AB / vector_AB.magnitude())
        if  3.11 < theta:
            self.action['backward'] = True
            self.auto_attack()
        else:
            self.action['left'] = True
            #time.sleep(1)
            #self.auto_attack()
    
        vector_wall = self.helper.get_nearest_RE_position() - self.helper.get_self_position()
        indexx = vector_wall[0]
        indexy = vector_wall[1]
        lenth = sqrt(indexx**2 + indexy**2)
        if lenth <= 1.5:
            self.action['left'] = True
            self.action['forward'] = False
            if indexx * self.helper.get_self_direction()[0] + indexy * self.helper.get_self_direction()[1] == 0:
                self.action['left'] = False
                self.action['forward'] = True
