AI_DIR_FORWARD      = 0
AI_DIR_BACKWARD     = 1
AI_DIR_LEFT         = 2
AI_DIR_RIGHT        = 3
AI_DIR_ATTACK       = 4
AI_DIR_STOP         = 5
 
ACTION_NONE = {'forward':False, 'backward':False, 'left':False, 'right':False, 'attack':False}
 
import math
 
class TeamAI():
    def __init__(self, helper):
        self.helper = helper
        self.enhancement = [5,2,5,2] 
        self.action = ACTION_NONE.copy()
 
    def angle(self, v1, v2):
        co = (v1[0]*v2[0] + v1[1]*v2[1]) / (v1.magnitude()*v2.magnitude())
        return math.acos(co)
 
    def decide(self):
        d = self.helper.get_self_position() - self.helper.get_nearest_RE_position()
 
        # dodge the RE
            
        if (d[0]**2 + d[1]**2) ** 0.5 < 3 and (self.angle(d, self.helper.get_self_direction()) > math.pi/10):        
            if (d[0]**2 + d[1]**2) ** 0.5 < 2:
                return {'forward':False, 'backward':False, 'left':False, 'right':True, 'attack':False}
            else:
                return {'forward':True, 'backward':False, 'left':False, 'right':True, 'attack':False}
        else:
            if (d[0]**2 + d[1]**2) ** 0.5 < 2:
                return {'forward':True, 'backward':False, 'left':False, 'right':False, 'attack':False}
        
        if (d[0]**2 + d[1]**2) ** 0.5 < 4:        
            return {'forward':True, 'backward':False, 'left':False, 'right':False, 'attack':False}
        else:
            return {'forward':True, 'backward':False, 'left':False, 'right':False, 'attack':True}
            # return {'forward':True, 'backward':False, 'left':False, 'right':False, 'attack':False}