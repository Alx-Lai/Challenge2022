from AI.lib.brain import Brain
from AI.lib.navigator import Navigator
from AI.lib.utils import *
from AI.lib.Const import *
import math

class Attacker():
    def __init__(self, brain: Brain, navigator: Navigator):
        self.brain = brain
        self.navigator = navigator
        self.lastScanTime = -ATTACK_TARGET_SCAN_FREQUENCY
        self.target = None
        self.attackReady = False
    
    def DirectHit(self, target: pg.Vector2) -> bool:
        """
        Check if target can be hit directly from current position.
        Method: Simulate the shot.
        """
        current = self.brain.position.copy()
        delta = target - current
        delta.scale_to_length(SHOOT_SIMULATE_LENGTH)
        cnt = 0
        cntMax = MAX_DISTANCE / SHOOT_SIMULATE_LENGTH
        while Index(current) != Index(target) and cnt <= cntMax:
            current += delta
            cnt += 1
            if self.brain.isObstacle[Index(current)]:
                return False
        return True


    def GetAttackRange(self) -> float:
        """
        Get the attack range of current accuracy.
        """
        inAccuracy = self.brain.helper.get_self_attack_accuracy() + ATTACK_ROTATIONAL_TOLERANCE
        attackRange = max(MINIMUM_ATTACK_RANGE, Const.PLAYER_RADIUS / inAccuracy)
        if self.brain.helper.get_self_gun_type() == Const.GUN_TYPE_SHOTGUN:
            attackRange *= SHOTGUN_ATTACK_RANGE_MULTIPLIER
        return attackRange


    def InAttackRange(self, target: pg.Vector2) -> bool:
        """
        Check if the target position is in current attack range. 
        """
        distance = (self.brain.position - target).length()
        return distance < self.GetAttackRange()


    def Scoring(self, target: pg.Vector2) -> float:
        """
        Calculate the score of a specific target, considering position, attack range, direct hit, etc.
        """
        score = -((self.brain.position - target).length()) / (MAX_DISTANCE)
        if self.DirectHit(target) and self.InAttackRange(target):
            score += 1
        return score


    def ScanTarget(self):
        """
        Scan all players and setup a best target. 
        """
        self.lastScanTime = self.brain.time
        tmpTarget = self.target
        self.target = None

        isRespawning = self.brain.helper.get_player_is_respawning()
        isAlive = self.brain.helper.get_player_is_alive()
        for idx in range(Const.PLAYER_NUMBER):
            if idx == self.brain.id or not isAlive[idx] or isRespawning[idx]:
                continue
            if self.target == None or self.Scoring(self.brain.playerPosition[self.target]) < self.Scoring(self.brain.playerPosition[idx]):
                self.target = idx
        if tmpTarget != self.target:
            self.attackReady = False
    

    def CheckTarget(self) -> bool:
        """
        Check if the target player is still attackable. 
        """
        idx = self.target
        if idx == None or not self.brain.helper.get_player_is_alive()[idx] or self.brain.helper.get_player_is_respawning()[idx]:
            self.target = None
        return self.target != None


    def GetAttackPosition(self, idx: int, position: pg.Vector2) -> pg.Vector2:
        """
        Get a position to attack current target.
        """
        return position + self.brain.playerHabit[idx] * ATTACK_POSITION_PREDICT_TIME


    def Decide(self):
        """
        Main function of Attacker, modify action and return true when attack
        """
        if self.target == None or self.brain.time - self.lastScanTime >= ATTACK_TARGET_SCAN_FREQUENCY:
            self.ScanTarget()
        if not self.CheckTarget():
            self.brain.mode = Mode.IDLE
            return
        
        self.brain.mode = Mode.ATTACK
        idx = self.target
        distance = (self.brain.playerPosition[idx] - self.brain.position).length()
        position = self.brain.playerPosition[idx] + self.brain.playerHabit[idx] * (distance / Const.BULLET_SPEED)
        if self.attackReady or (self.DirectHit(position) and self.InAttackRange(position)):
            self.attackReady = True
            rotateRadian = AngleBetween(self.brain.direction, position - self.brain.position)
            if abs(rotateRadian) > ATTACK_ROTATIONAL_TOLERANCE:
                if rotateRadian < 0:
                    self.brain.action['left'] = True
                else:
                    self.brain.action['right'] = True
            else:
                self.brain.action['forward'] = True
                if self.brain.ShootCheck():
                    self.brain.action['attack'] = True
                    self.brain.mode = Mode.IDLE
                    self.attackReady = False
        else:
            position = self.GetAttackPosition(self.target, position)
            self.navigator.Decide(position)