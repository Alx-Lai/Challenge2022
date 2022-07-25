AI_DIR_FORWARD      = 0
AI_DIR_BACKWARD     = 1
AI_DIR_LEFT         = 2
AI_DIR_RIGHT        = 3
AI_DIR_ATTACK       = 4
AI_DIR_STOP         = 5

ACTION_NONE = {'forward':False, 'backward':False, 'left':False, 'right':False, 'attack':False}

import random
import math

class TeamAI():
    def __init__(self, helper):
        self.helper = helper
        self.enhancement = [4,2,4,3]
        self.action = ACTION_NONE.copy()
        self.player_id = helper.get_self_id()
        self.counter = 0
        self.rotate = 0
        self.wander = False
        # print(self.helper.get_nearest_RE_position())  
        # print(self.helper.get_self_kick())

    def reset(self):
        self.action = ACTION_NONE.copy()
    
    def auto_attack(self):
        if self.helper.get_self_next_attack() == 0:
            self.action['attack'] = True

    
    def auto_wander(self):
        tmp = random.randint(0, 1000)
        self.action['forward'] = True
        if tmp%2:
            self.action['left'] = True
        else:
            self.action['right'] = True
        
        
#   新code{

    def avoid_wall(self):
        RE = self.helper.get_nearest_RE_position()
        position = self.helper.get_self_position()
        if (position - RE).dot(self.helper.get_self_direction()) / ((position - RE).magnitude() * self.helper.get_self_direction().magnitude()) >= 0.5:
            self.action['forward'] = True
        elif RE[0] - position[0] < 3.0 and RE[1] - position[1] < 3.0:
            self.action['right'] = True
            self.action['left'] = False
            self.action['forward'] = False
        elif RE[0] - position[0] < 3.0 and RE[1] - position[1] > -3.0:
            self.action['left'] = True
            self.action['right'] = False
            self.action['forward'] = False
        elif RE[0] - position[0] > -3.0 and RE[1] - position[1] < 3.0:
            self.action['right'] = True
            self.action['left'] = False
            self.action['forward'] = False
        elif RE[0] - position[0] > -3.0 and RE[1] - position[1] > -3.0:
            self.action['left'] = True
            self.action['right'] = False
            self.action['forward'] = False
####        return self.action 


    def distance(self, object_position):
        return (object_position - self.helper.get_self_position()).magnitude()
        
    def danger(self):
        if self.distance(self.helper.get_nearst_RE_position) < get_self_kick() + 3:
            return 1
        else:
            return 0
    

    def item(self):
        dict1=self.get_nearest_item_info()
        item_position=dict1["position"]
        my_position=self.get_self_position()
        my_dir=self.get_self_direction()
        vec=(item_position[0]-my_position[0],item_postion[1]-my_position[1])            
        while my_position.cross(vec)!=0:
            self.action['left'] = True

        if my_position.cross(vec)==0:
            self.action['forward'] = True

#   }

    def decide(self):
        self.reset()

#   以下是新code
        if self.distance(self.helper.get_nearest_RE_position()) < self.helper.get_self_kick() + 2.5:            #如果快出事了 
            self.avoid_wall()

        else:               #如果沒事
            self.auto_attack()
            self.auto_wander()
        return self.action




    # def decide(self):
        
    #     self.auto_wander()
        
    #     if self.rotate == 0:
    #         self.rotate = random.randint(-100, 100)
    #     if self.rotate != 0:
    #         if self.rotate > 0:
    #             self.rotate -= 1
    #             if self.rotate > 20:
    #                 self.action['left'] = True
    #         else:
    #             self.rotate += 1
    #             if self.rotate < -20:
    #                 self.action['right'] = True
        

