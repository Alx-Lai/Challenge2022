from AI.lib.brain import Brain
from AI.lib.utils import *
from AI.lib.Const import *
import math

class Attacker():
    def __init__(self, brain: Brain):
        self.brain = brain
        self.lastScanTime = -ATTACK_TARGET_SCAN_FREQUENCY
        self.targets = []
    
    def DirectHit(self, target: pg.Vector2):
        """
        Check if target can be hit directly from current position.
        Method: Simulate the shot.
        """
        current = self.brain.position.copy()
        delta = target - current
        delta.scale_to_length(SHOOT_SIMULATE_LENGTH)
        cnt = 0
        cntMax = Const.ARENA_GRID_COUNT * math.sqrt(2) / SHOOT_SIMULATE_LENGTH
        while Index(current) != Index(target) and cnt <= cntMax:
            current += delta
            cnt += 1
            if self.brain.blocks[Index(current)]:
                return False
        return True

    def getAttackRange(self):
        """
        Get the attack range of current accuracy.
        """
        inAccuracy = self.brain.helper.get_self_attack_accuracy() + ATTACK_ROTATIONAL_TOLERANCE
        attackRange = max(MINIMUM_ATTACK_RANGE, Const.PLAYER_RADIUS / inAccuracy)
        if self.brain.helper.get_self_gun_type() == Const.GUN_TYPE_SHOTGUN:
            attackRange *= SHOTGUN_ATTACK_RANGE_MULTIPLIER
        return attackRange

    def ScanTargets(self):
        """
        Get a list of player_id of attackable players.
        """
        self.targets = []
        isRespawning = self.brain.helper.get_player_is_respawning()
        for idx, targetPos in enumerate(self.brain.helper.get_player_position()):
            if idx != self.brain.id and not isRespawning[idx] and self.DirectHit(targetPos) \
                and (targetPos - self.brain.position).length() < self.getAttackRange():
                self.targets.append(targetPos)    
    
    def shootCheck(self):
        """
        Check if it is safe to shoot at current position.
        """
        pos = self.brain.position.copy()
        delta = self.brain.direction.copy()
        delta.rotate(90).scale_to_length(Const.PLAYER_RADIUS) # Left Delta
        kick = -self.brain.direction * self.brain.helper.get_self_kick()
        return self.brain.safeNodes[Index(pos + delta + kick)] and self.brain.safeNodes[Index(pos - delta + kick)]
    
    def Decide(self):
        """
        Main function of Attacker, modify action and return true when attack
        """
        if self.brain.time - self.lastScanTime >= ATTACK_TARGET_SCAN_FREQUENCY:
            self.ScanTargets()
            self.lastScanTime = self.brain.time
        
        if self.brain.respawning or self.brain.nextAttack > 0 or not self.targets:
            self.brain.mode = Mode.IDLE
            return
        
        # print(self.targets)
        self.brain.mode = Mode.ATTACK
        rotateRadian = min([AngleBetween(self.brain.direction, target - self.brain.position) for target in self.targets])
        if abs(rotateRadian) > ATTACK_ROTATIONAL_TOLERANCE:
            if rotateRadian < 0:
                self.brain.action['left'] = True
            else:
                self.brain.action['right'] = True
        else:
            self.brain.action['forward'] = True
            if self.shootCheck():
                self.brain.action['attack'] = True
                self.brain.mode = Mode.IDLE