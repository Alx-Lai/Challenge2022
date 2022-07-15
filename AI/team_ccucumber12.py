import random
from AI.lib.brain import Brain
from AI.lib.attacker import Attacker
from AI.lib.navigator import Navigator
from AI.lib.Const import *
from AI.lib.utils import AngleBetween

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
        # print(AngleBetween(self.brain.helper.get_self_direction(), pg.Vector2(1, 0)))
        # return 2


        self.brain.Initialize()

        if self.brain.isAttacking or self.rollAttack():
            self.attacker.Decide()
        if not self.brain.isAttacking:
            self.navigator.Decide()
        return self.brain.action
    
