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
        self.enhancement = [0, 0, 0, 0]
        self.action = ACTION_NONE.copy()
        self.player_id = helper.get_self_id()
        self.counter = 0
        self.rotate = 0
        self.wander = False
    
    def reset(self):
        self.action = ACTION_NONE.copy()
    
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
                    self.action['left'] = True
            else:
                self.rotate += 1
                if self.rotate < -20:
                    self.action['right'] = True

        return self.action
