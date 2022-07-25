AI_DIR_FORWARD      = 0
AI_DIR_BACKWARD     = 1
AI_DIR_LEFT         = 2
AI_DIR_RIGHT        = 3
AI_DIR_ATTACK       = 4
AI_DIR_STOP         = 5
from math import atan2, degrees, pi, sqrt
ACTION_NONE = {'forward':False, 'backward':False, 'left':False, 'right':False, 'attack':False}

class TeamAI():
    def __init__(self, helper):
        self.helper = helper
        self.enhancement = [5,3,2,3] 
        self.action = ACTION_NONE.copy()
        self.counter = 0
        self.cnt = 0
        self.cnthide = 0

    def hide(self):
        
        myself = self.helper.get_self_id()
        enemy = self.helper.get_nearest_RE_position()
        ai = self.helper.get_self_position()
        
        barrier = self.helper.get_wall_position()
        if(((enemy.x-ai.x)**2+(enemy.y-ai.y)**2)<5):
            direct =  self.helper.get_self_direction()   
            dx = enemy.x - ai.x
            dy = enemy.y - ai.y
            l = sqrt(dx**2 + dy**2)
            dx, dy = dx/l, dy/l
            # rads = atan2(-dy,dx)
            # rads %= 2*pi
            # degs = degrees(rads)
            if(abs(dx*direct.x)+(dy*direct.y) < 0.15):
                return 0
            else:
                return 3
        return 0

    def auto_get_buff(self):
        from math import atan2 
        a = self.helper.get_nearest_item_info()['position'] - self.helper.get_self_position()
        selfdirection = atan2(a[1],a[0])
        b=atan2(self.helper.get_self_direction()[1],self.helper.get_self_direction()[0])
        if selfdirection == b:
            return {'forward':True, 'backward':False, 'left':False, 'right':False, 'attack':False}
        elif selfdirection > b:
            return {'forward':True, 'backward':False, 'left':False, 'right':True, 'attack':False}
        elif selfdirection < b:
            return {'forward':True, 'backward':False, 'left':True, 'right':False, 'attack':False}

    def decide(self):

        self.cnt += 1

        self.action['attack'] = False
        if self.cnt == 200:
            self.cnt = 0
            self.action['attack'] = True
            return self.action
        return self.hide()
