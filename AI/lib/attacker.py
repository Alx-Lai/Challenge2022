from AI.lib.utils import *
from AI.lib.brain import Brain

ROTATE_TOLERANCE = 0.03 # radian
SCAN_FREQUENCY = 10 # frames per scan
ATTACK_RANGE = 10.0 # grids

class Attacker():
    def __init__(self, brain: Brain):
        self.brain = brain
        self.lastScanTime = -SCAN_FREQUENCY
        self.targets = []
        
    def scanTargets(self):
        """
        Get a list of position of attackable targets.
        """
        self.targets = []
        tar_alive = [time == 0 for time in self.brain.helper.get_player_respawn_time()]
        for idx, tar_pos in enumerate(self.brain.helper.get_player_position()):
            if idx == self.brain.id or not tar_alive[idx]:
                continue
            if (self.brain.position - tar_pos).length() < ATTACK_RANGE:
                self.targets.append(tar_pos)
    
    def decide(self):
        """
        Main function of Attacker, modify action and return true when attack
        """
        if self.brain.time - self.lastScanTime >= SCAN_FREQUENCY:
            self.scanTargets()
            self.lastScanTime = self.brain.time
        
        if not self.brain.alive or self.brain.next_attack > 0 or not self.targets:
            self.brain.is_attacking = False
            return
        
        self.brain.is_attacking = True
        rotate_radian = min([angle_between(self.brain.direction, target - self.brain.position) for target in self.targets])
        if abs(rotate_radian) > ROTATE_TOLERANCE:
            if rotate_radian < 0:
                self.brain.action['left'] = True
            else:
                self.brain.action['right'] = True
        else:
            self.brain.action['attack'] = True
            self.brain.is_attacking = False