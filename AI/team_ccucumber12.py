import random
from AI.lib.brain import Brain
from AI.lib.attacker import Attacker
from AI.lib.navigator import Navigator
from AI.lib.protector import Protector
from AI.lib.Const import *
from AI.lib.utils import *

class TeamAI():
    def __init__(self, helper):
        self.enhancement = [0, 0, 0, 0]
        self.brain = Brain(helper)
        self.navigator = Navigator(self.brain)
        self.attacker = Attacker(self.brain)
        self.protector = Protector(self.brain)
    
    def ModeDecision(self):
        if self.brain.mode != Mode.IDLE:
            return 
        attackPoint = self.brain.time 
        collectPoint = (Const.GAME_LENGTH - self.brain.time) 
        if self.brain.helper.get_self_gun_type() == Const.GUN_TYPE_MACHINE_GUN:
            attackPoint *= 5
        if random.randint(1, attackPoint + collectPoint) <= attackPoint:
            self.brain.mode = Mode.ATTACK
        else:
            self.brain.mode = Mode.COLLECT

    def decide(self):
        self.brain.Initialize()
        self.ModeDecision()

        if self.brain.mode == Mode.ATTACK:
            self.attacker.Decide()
        if self.brain.mode in (Mode.IDLE, Mode.COLLECT):
            self.navigator.Decide()
        self.protector.Decide()
        return self.brain.action
    
