import random
from AI.lib.brain import Brain
from AI.lib.attacker import Attacker
from AI.lib.navigator import Navigator
from AI.lib.Const import *

class TeamAI():
    def __init__(self, helper):
        self.enhancement = [0, 0, 0, 0]
        self.brain = Brain(helper)
        self.navigator = Navigator(self.brain)
        self.attacker = Attacker(self.brain)
    
    def rollAttack(self) -> bool:
        # prob = 1200 - min(1200, self.brain.time)
        prob = 0
        return random.randint(0, prob) == 0
    
    def decide(self):
        self.brain.initialize()

        if self.brain.is_attacking or self.rollAttack():
            self.attacker.decide()
        if not self.brain.is_attacking:
            self.navigator.decide()
        return self.brain.action
    
