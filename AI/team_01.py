AI_DIR_FORWARD      = 0
AI_DIR_BACKWARD     = 1
AI_DIR_LEFT         = 2
AI_DIR_RIGHT        = 3
AI_DIR_ATTACK       = 4
AI_DIR_STOP         = 5

ACTION_NONE = {'forward':False, 'backward':False, 'left':False, 'right':False, 'attack':False}

import pygame

class TeamAI():
    def __init__(self, helper):
        self.helper = helper
        self.enhancement = [1,1,2,1] 
        self.action = ACTION_NONE.copy()
    
    def reset(self):
        self.action = ACTION_NONE.copy()
    
    def red(self):
        position = self.helper.get_self_position()
        face = self.helper.get_self_direction()
        red = self.helper.get_nearest_RE_position()

        vec, normal1, normal2 = pygame.Vector2(), pygame.Vector2(), pygame.Vector2()
        vec.x, vec.y = position.x - red.x, position.y - red.y
        normal1 = pygame.Vector2.normalize(vec)
        normal2 = pygame.Vector2.normalize(face)
        if vec.magnitude() <= 3:
            if normal1 == normal2:
                if self.helper.get_self_next_attack() == 0:
                    self.action['attack'] = True
                else:
                    self.action['backward'] = True
            else:
                self.action['right'] = True
                self.action['forward'] = True
        else:
            self.action['forward'] = True
        
    

    def decide(self):
        self.reset()
        self.red()

        if self.helper.get_self_next_attack() == 0:
            self.action['attack'] = True
            self.action['right'] = True
            self.action['forward'] = True
        return self.action