AI_DIR_FORWARD      = 0
AI_DIR_BACKWARD     = 1
AI_DIR_LEFT         = 2
AI_DIR_RIGHT        = 3
AI_DIR_ATTACK       = 4
AI_DIR_STOP         = 5

AI_DIR_NONE = {'forward':False, 'backward':False, 'left':False, 'right':False, 'attack':False}

import random
import math
from AI.lib.attacker import Attacker
from AI.lib.navigator import Navigator
from API.helper import *

class TeamAI():
    def __init__(self, helper: Helper):
        self.helper = helper
        self.action = AI_DIR_NONE.copy()
        self.navigator = Navigator(self.helper, self.action)
        self.isAttacking = [False]
        self.attacker = Attacker(self.helper, self.action, self.isAttacking)
        self.id = self.helper.get_self_id()
      
    def initialize(self):
        for k in self.action:
            self.action[k] = False
        self.time = self.helper.get_game_time()
    
    def rollAttack(self) -> bool:
        prob = 1200 - min(1200, self.time)
        return random.randint(0, prob) == 0
    
    def decide(self):
        self.initialize()

        if self.isAttacking[0] or self.rollAttack():
            self.attacker.decide()
        if not self.isAttacking[0]:
            self.navigator.decide()
        return self.action
