import random
from AI.lib.brain import Brain
from AI.lib.attacker import Attacker
from AI.lib.navigator import Navigator
from AI.lib.protector import Protector
from AI.lib.Const import *
from AI.lib.utils import AngleBetween

class TeamAI():
    def __init__(self, helper):
        self.enhancement = [0, 0, 0, 0]
        self.brain = Brain(helper)
        self.navigator = Navigator(self.brain)
        self.attacker = Attacker(self.brain)
    
    def decide(self):
        self.brain.Initialize()

        if self.brain.mode == Mode.ATTACK:
            self.attacker.Decide()
        elif self.brain.mode == Mode.COLLECT:
            self.navigator.Decide()
        else:
            if random.randint(0, 1) == 0:
                self.attacker.Decide()
            else:
                self.navigator.Decide()
        return self.brain.action
    
