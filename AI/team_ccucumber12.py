AI_DIR_FORWARD      = 0
AI_DIR_BACKWARD     = 1
AI_DIR_LEFT         = 2
AI_DIR_RIGHT        = 3
AI_DIR_ATTACK       = 4
AI_DIR_STOP         = 5

ACTION_NONE = {'forward':False, 'backward':False, 'left':False, 'right':False, 'attack':False}

import random
from AI.lib.attacker import Attacker
from AI.lib.navigator import Navigator
from AI.lib.brain import Brain

class TeamAI():
    def __init__(self, helper: Helper):
        self.brain = Brain(helper)
        self.navigator = Navigator(self.brain)
        self.attacker = Attacker(self.brain)
    
    def rollAttack(self) -> bool:
        prob = 1200 - min(1200, self.brain.time)
        return random.randint(0, prob) == 0
    
    def decide(self):
        self.brain.initialize()

        if self.brain.is_attacking or self.rollAttack():
            self.attacker.decide()
        if not self.brain.is_attacking:
            self.navigator.decide()
        return self.brain.action
    
