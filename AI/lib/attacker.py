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
        SIMULATE_DELTA = 0.5
        delta = SIMULATE_DELTA
        direction = target - self.brain.position
        current = self.brain.position

    def directHit2(self, target: pg.Vector2):
        """
        Check if target can be hit directly from current position.
        Method: Check every wall segments.
        """
        position = self.brain.position
        for seg in self.brain.wall_segments:
            if banana(position, target, seg[0], seg[1]):
                return False
        return True

    def scanTargets(self):
        """
        Get a list of position of attackable targets.
        """
        self.targets = []
        tar_alive = [time == 0 for time in self.brain.helper.get_player_respawn_time()]
        for idx, tar_pos in enumerate(self.brain.helper.get_player_position()):
            if idx == self.brain.id or not tar_alive[idx]:
                continue
            # if self.directHit(tar_pos):
            if (tar_pos - self.brain.position).length() < ATTACK_RANGE:
                self.targets.append(tar_pos)
    
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