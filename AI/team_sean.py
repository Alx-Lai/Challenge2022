AI_DIR_FORWARD      = 0
AI_DIR_BACKWARD     = 1
AI_DIR_LEFT         = 2
AI_DIR_RIGHT        = 3
AI_DIR_ATTACK       = 4
AI_DIR_STOP         = 5

AI_DIR_NONE = {'forward':False, 'backward':False, 'left':False, 'right':False, 'attack':False}

TASK_NONE = 0
TASK_SHOOT_NEAR = 1
TASK_ESCAPE_RE = 4
TASK_NEAR_ITEM = 2
TASK_WANDER = 3
TASK_RESPAWN = 5

ATTACK_SUCCESS = 1
ATTACK_FAIL = 0

import random
import math
import Const
from pygame import Vector2

def to_radian(angle: float) -> float:
    """
    turn angle to radian
    """
    return angle * math.pi / 180

class TeamAI():
    def __init__(self, helper):
        self.helper = helper
        self.player_id = helper.get_self_id()
        self.AI = AI_DIR_NONE
        self.counter = 0
        self.rotate = 0
        self.wander = 0
        self.in_task = TASK_NONE
    
    def reset(self):
        self.AI = {'forward':False, 'backward':False, 'left':False, 'right':False, 'attack':False}
    
    def auto_attack(self):
        if self.helper.get_player_next_attack()[self.player_id] == 0 \
            and self.helper.get_player_respawn_time()[self.player_id] == 0:
            self.AI['attack'] = True
            return ATTACK_SUCCESS
        else:
            return ATTACK_FAIL
    
    def auto_wander(self):
        if self.wander == 0:
            if random.randint(0, 1000) == 0:
                self.wander = random.randint(150, 600)
        if self.wander > 0:
            self.AI['forward'] = True
            self.wander -= 1

    def get_rotation_radian(self, tar_pos: Vector2) -> int:
        """
        return the difference between the direction to target position
        and my direction
        """
        self_pos = self.helper.get_self_position()
        self_dir = self.helper.get_self_direction()
        angle = (tar_pos - self_pos).angle_to(self_dir)
        if (angle > 180):
            angle -= 360
        if (angle < -180):
            angle += 360
        radian = to_radian(angle)
        return round(radian / self.helper.get_self_rotation_speed())

    def task_shoot_init(self):
        self.rotate = self.get_rotation_radian(self.helper.get_nearest_player_position())

    def task_escape_RE_init(self):
        self.rotate = self.get_rotation_radian(self.helper.get_nearest_RE_position())
        self.wander = -1 / self.helper.get_self_base_speed() / 10
        # print(self.wander)

    def task_near_item_init(self):
        self_pos = self.helper.get_self_position()
        item_pos = self.helper.get_nearest_item_info()['position']
        RE_pos = self.helper.get_nearest_RE_position()

        if (self_pos - item_pos).length() < (self_pos - RE_pos).length():
            self.rotate = self.get_rotation_radian(2 * self_pos - item_pos)
            self.wander = -1 / self.helper.get_self_base_speed() / 10
        else:
            self.in_task = TASK_WANDER
            self.task_escape_RE_init()

    def task_wander_init(self):
        field_sum = Vector2(0, 0)
        self_pos = self.helper.get_self_position()
        RE_pos = self.helper.get_RE_field_position()
        RE_pos += [Vector2(0, y) for y in range(31)]
        RE_pos += [Vector2(30, y) for y in range(31)]
        RE_pos += [Vector2(x, 0) for x in range(31)]
        RE_pos += [Vector2(x, 30) for x in range(31)]
        obstacle_pos =  self.helper.get_wall_position()
        for pos in RE_pos:
            field_sum += (self_pos - pos).normalize() * 2 / ((self_pos - pos).length() ** 2)
        for pos in obstacle_pos:
            field_sum += (self_pos - pos).normalize() * 1 / ((self_pos - pos).length() ** 2)

        self.rotate = self.get_rotation_radian(self_pos - field_sum)
        self.wander = -1 / self.helper.get_self_base_speed() / 10
        # print(field_sum)

    def check_dir(self, pos):
        radian_dif = self.get_rotation_radian(pos);
        if abs(radian_dif) < self.helper.get_self_attack_accuracy() / 2:
            return True
        else:
            return False

    def reset_status(self):
        self.in_task = TASK_NONE
        self.wander = 0
        self.rotate = 0
        
    def decide(self):
        self.reset()

        # print(self.helper.get_bullet_info())

        if self.helper.get_self_respawn_time() != 0 \
                and self.in_task != TASK_RESPAWN:
            self.reset_status()

        if self.in_task == TASK_NONE:
            if self.helper.get_self_respawn_time() != 0:
                self.in_task = TASK_RESPAWN
            else:
                self_pos = self.helper.get_self_position()
                nearest_player = self.helper.get_nearest_player_position()
                nearest_item = self.helper.get_nearest_item_info()['position']
                nearest_RE = self.helper.get_nearest_RE_position()
                if self_pos.distance_to(nearest_player) < self_pos.distance_to(nearest_RE) and \
                    self_pos.distance_to(nearest_player) < self_pos.distance_to(nearest_item):
                    self.in_task = TASK_SHOOT_NEAR
                elif self_pos.distance_to(nearest_item) < self_pos.distance_to(nearest_RE):
                    self.in_task = TASK_NEAR_ITEM
                elif self_pos.distance_to(nearest_RE) <= 2.0:
                    self.in_task = TASK_ESCAPE_RE
                else:
                    self.in_task = TASK_WANDER

            if self.in_task == TASK_SHOOT_NEAR:
                self.task_shoot_init()
            elif self.in_task == TASK_NEAR_ITEM:
                self.task_near_item_init()
            elif self.in_task == TASK_WANDER:
                self.task_wander_init()
            elif self.in_task == TASK_ESCAPE_RE:
                self.task_escape_RE_init()
            elif self.in_task == TASK_RESPAWN:
                self.task_escape_RE_init()

        if self.in_task == TASK_SHOOT_NEAR:
            if self.rotate == 0:
                if self.helper.get_self_next_attack() == 0:
                    if self.check_dir(self.helper.get_nearest_player_position()):
                        self.auto_attack()
                    self.in_task = TASK_NONE
        elif self.in_task == TASK_ESCAPE_RE or self.in_task == TASK_RESPAWN:
            if self.rotate == 0:
                if self.helper.get_self_respawn_time() == 0 \
                        and self.helper.get_self_next_attack() == 0:
                    if self.check_dir(self.helper.get_nearest_RE_position()):
                        self.auto_attack()
                    self.in_task = TASK_NONE
                    self.wander = 0
                if self.wander == 0:
                    self.in_task = TASK_NONE
        elif self.in_task == TASK_NEAR_ITEM:
            if self.rotate == 0:
                if self.helper.get_self_next_attack() == 0 \
                        and self.helper.get_self_respawn_time() == 0:
                    if self.check_dir(2 * self.helper.get_self_position() \
                            - self.helper.get_nearest_item_info()['position']):
                        self.auto_attack()
                    self.in_task = TASK_NONE
                    self.wander = 0
                if self.wander == 0:
                    self.in_task = TASK_NONE
        elif self.in_task == TASK_WANDER:
            if self.rotate == 0:
                if self.helper.get_self_next_attack() == 0 \
                        and self.helper.get_self_respawn_time() == 0:
                    self.auto_attack()
                    self.in_task = TASK_NONE
                    self.wander = 0
                if self.wander == 0:
                    self.in_task = TASK_NONE

        if self.rotate != 0:
            if self.rotate > 0:
                self.rotate -= 1
                self.AI['left'] = True
            else:
                self.rotate += 1
                self.AI['right'] = True
        elif self.wander != 0:
            if self.wander > 0 :
                self.wander -= 1
                self.AI['forward'] = True
            else:
                self.wander += 1
                self.AI['backward'] = True

        return self.AI
