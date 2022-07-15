from AI.lib.brain import Brain
from AI.lib.utils import *
from AI.lib.Const import *

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
        # print("----- start -----")
        while Index(current) != Index(target):
            # print(F"current:{current}, idx:{Index(current)} ; target:{target}, idx:{Index(target)}")
            current += delta
            if self.brain.blocks[Index(current)]:
                return False
        return True

    def ScanTargets(self):
        """
        Get a list of player_id of attackable players.
        """
        self.targets = []
        isRespawning = self.brain.helper.get_player_is_respawning()
        for idx, targetPos in enumerate(self.brain.helper.get_player_position()):
            if idx != self.brain.id and not isRespawning[idx] and self.DirectHit(targetPos) and (targetPos - self.brain.position).length() < ATTACK_RANGE:
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
            self.brain.isAttacking = False
            return
        
        self.brain.isAttacking = True
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
                self.brain.isAttacking = False