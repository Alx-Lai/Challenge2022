from AI.lib.brain import Brain
from AI.lib.utils import *
from AI.lib.Const import *

class Attacker():
    def __init__(self, brain: Brain):
        self.brain = brain
        self.lastScanTime = -ATTACK_TARGET_SCAN_FREQUENCY
        self.targets = []
    
    def directHit(self, target: pg.Vector2):
        """
        Check if target can be hit directly from current position.
        Method: Simulate the shot.
        """
        current = self.brain.position
        delta = target - current
        delta.scale_to_length(SHOOT_SIMULATE_LENGTH)
        while index(current) != index(target):
            current += delta
            if not self.brain.safe_nodes[index(current)]:
                return False
        return True

    def scanTargets(self):
        """
        Get a list of position of attackable targets.
        """
        self.targets = []
        isRespawning = self.brain.helper.get_player_is_respawning()
        for idx, targetPos in enumerate(self.brain.helper.get_player_position()):
            if idx == self.brain.id or isRespawning[idx]:
                continue
            if self.directHit(targetPos):
            # if (tar_pos - self.brain.position).length() < ATTACK_RANGE:
                self.targets.append(targetPos)
    
    def decide(self):
        """
        Main function of Attacker, modify action and return true when attack
        """
        if self.brain.time - self.lastScanTime >= ATTACK_TARGET_SCAN_FREQUENCY:
            self.scanTargets()
            self.lastScanTime = self.brain.time
        
        if self.brain.respawning or self.brain.next_attack > 0 or not self.targets:
            self.brain.is_attacking = False
            return
        
        self.brain.is_attacking = True
        rotate_radian = min([angleBetween(self.brain.direction, target - self.brain.position) for target in self.targets])
        if abs(rotate_radian) > ATTACK_ROTATIONAL_TOLERANCE:
            if rotate_radian < 0:
                self.brain.action['left'] = True
            else:
                self.brain.action['right'] = True
        else:
            self.brain.action['attack'] = True
            self.brain.is_attacking = False