AI_DIR_FORWARD      = 0
AI_DIR_BACKWARD     = 1
AI_DIR_LEFT         = 2
AI_DIR_RIGHT        = 3
AI_DIR_ATTACK       = 4
AI_DIR_STOP         = 5

AI_DIR_NONE = {'forward':False, 'backward':False, 'left':False, 'right':False, 'attack':False}

import random
import math
from AI.lib.navigator import Navigator

class TeamAI():
    def __init__(self, helper):
        self.helper = helper
        self.action = AI_DIR_NONE.copy()
        self.navigator = Navigator(self.helper, self.action)
        self.id = helper.get_self_id()
        self.counter = 0
      
    def initialize(self):
        for k in self.action:
            self.action[k] = False
    
    def decide(self):
        self.initialize()
        self.navigator.decide()

        return self.action
