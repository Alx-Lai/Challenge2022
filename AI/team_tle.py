AI_DIR_FORWARD      = 0
AI_DIR_BACKWARD     = 1
AI_DIR_LEFT         = 2
AI_DIR_RIGHT        = 3
AI_DIR_ATTACK       = 4
AI_DIR_STOP         = 5

ACTION_NONE = {'forward':False, 'backward':False, 'left':False, 'right':False, 'attack':False}

class TeamAI():
    def __init__(self, helper):
        self.helper = helper
        self.enhancement = [0, 0, 0, 0] 
        self.action = ACTION_NONE.copy()
    
    def decide(self):
        while True:
            pass
        return None