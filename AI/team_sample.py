AI_DIR_FORWARD      = 0
AI_DIR_BACKWARD     = 1
AI_DIR_LEFT         = 2
AI_DIR_RIGHT        = 3
AI_DIR_ATTACK       = 4
AI_DIR_STOP         = 5

AI_DIR_NONE = {'forward':False, 'backward':False, 'left':False, 'right':False, 'attack':False}

import random
import math

class TeamAI():
    def __init__(self, helper):
        self.helper = helper
        self.player_id = helper.get_self_id()
        self.AI = AI_DIR_NONE
        self.counter = 0
        self.rotate = 0
        self.wander = False
    
    def reset(self):
        self.AI = {'forward':False, 'backward':False, 'left':False, 'right':False, 'attack':False}
    
    def auto_attack(self):
        if self.helper.get_player_next_attack()[self.player_id] == 0:
            self.counter = 10
            self.AI['attack'] = True
        if self.counter > 0:
            self.AI['forward'] = True 
            self.counter -= 1
    
    def auto_wander(self):
        if self.wander == 0:
            if random.randint(0, 1000) == 0:
                self.wander = random.randint(150, 600)
        if self.wander > 0:
            self.AI['forward'] = True
            self.wander -= 1
        
    def decide(self):
        self.reset()
        if self.wander == 0:
            self.auto_attack()
        self.auto_wander()
        
        if self.rotate == 0:
            self.rotate = random.randint(-100, 100)
        if self.rotate != 0:
            if self.rotate > 0:
                self.rotate -= 1
                if self.rotate > 20:
                    self.AI['left'] = True
            else:
                self.rotate += 1
                if self.rotate < -20:
                    self.AI['right'] = True

        return self.AI
