from AI.lib.utils import *
from API.helper import *

ROTATE_TOLERANCE = 0.03 # radian
SCAN_FREQUENCY = 10 # frames per scan
ATTACK_RANGE = 10.0 # grids

class Attacker():
    def __init__(self, helper: Helper, action, isAttacking):
        self.helper = helper
        self.action = action
        self.id = helper.get_self_id()

        self.isAttacking = isAttacking
        self.lastScanTime = -SCAN_FREQUENCY
        self.targets = []
        
    def initialize(self):
        self.pos = self.helper.get_player_position()[self.id]
        self.dir = self.helper.get_player_direction()[self.id]
        self.cd = self.helper.get_player_next_attack()[self.id]
        self.alive = self.helper.get_player_respawn_time()[self.id] == 0
        self.time = self.helper.get_game_time()
        if self.time - self.lastScanTime >= SCAN_FREQUENCY:
            self.scanTargets()
            self.lastScanTime = self.time
        
    def scanTargets(self):
        """
        Get a list of position of attackable targets.
        """
        self.targets = []
        tar_alive = [time == 0 for time in self.helper.get_player_respawn_time()]
        for idx, tar_pos in enumerate(self.helper.get_player_position()):
            if idx == self.id or not tar_alive[idx]:
                continue
            if (self.pos - tar_pos).length() < ATTACK_RANGE:
                self.targets.append(tar_pos)
    
    def decide(self):
        """
        Main function of Attacker, modify action and return true when attack
        """
        # print("----- start -----")
        self.initialize()
        if not self.alive or self.cd > 0 or not self.targets:
            self.isAttacking[0] = False
            return
        
        self.isAttacking[0] = True
        rotate_radian = min([angle_between(self.dir, target - self.pos) for target in self.targets])
        if abs(rotate_radian) > ROTATE_TOLERANCE:
            if rotate_radian < 0:
                self.action['left'] = True
            else:
                self.action['right'] = True
        else:
            self.action['attack'] = True
            self.isAttacking[0] = False



        
        
