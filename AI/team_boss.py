import random
from AI.lib.brain import Brain
from AI.lib.attacker import Attacker
from AI.lib.collector import Collector
from AI.lib.navigator import Navigator
from AI.lib.protector import Protector
from AI.lib.Const import *
from AI.lib.utils import *

class TeamAI():
    def __init__(self, helper):
        self.enhancement = [0, 0, 0, 0]
        self.brain = Brain(helper)
        self.navigator = Navigator(self.brain)
        self.collector = Collector(self.brain, self.navigator)
        self.attacker = Attacker(self.brain, self.navigator)
        self.protector = Protector(self.brain)

        self.actionTime = 0
    

    def ModeDecision(self):
        self.actionTime += 1
        nearTargetDistance = (self.brain.helper.get_nearest_player_position() - self.brain.position).length()
        if (self.brain.helper.get_self_gun_type() in (Const.GUN_TYPE_MACHINE_GUN, Const.GUN_TYPE_SHOTGUN) and nearTargetDistance <= BERSERK_DISTANCE) \
            or (nearTargetDistance <= BERSERK_DISTANCE / 3):
            self.brain.mode = Mode.ATTACK
            self.actionTime = 0
            return 
        
        if self.brain.mode != Mode.IDLE and self.actionTime < MAX_ACTION_TIME:
            return 
        
        self.actionTime = 0
        attackPoint = self.brain.time * 5
        collectPoint = (Const.GAME_LENGTH - self.brain.time) / 2
        if self.brain.helper.get_self_gun_type() == Const.GUN_TYPE_MACHINE_GUN:
            attackPoint *= 2
        if self.brain.helper.get_self_gun_type() == Const.GUN_TYPE_SHOTGUN:
            attackPoint *= 10
        if self.brain.helper.get_self_gun_type() == Const.GUN_TYPE_NORMAL_GUN:
            attackPoint /= 20
            collectPoint = collectPoint * 20 + Const.GAME_LENGTH * 5
        if nearTargetDistance <= BERSERK_DISTANCE:
            attackPoint *= 10

        attackPoint //= 1
        collectPoint //= 1
        if random.randint(1, attackPoint + collectPoint) <= attackPoint:
            self.brain.mode = Mode.ATTACK
        else:
            self.brain.mode = Mode.COLLECT


    def decide(self):
        self.brain.Initialize()
        self.ModeDecision()
        if self.brain.mode == Mode.ATTACK:
            self.attacker.Decide()
        if self.brain.mode == Mode.COLLECT:
            self.collector.Decide()
        self.protector.Decide()
        return self.brain.action
    
