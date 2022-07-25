AI_DIR_FORWARD      = 0
AI_DIR_BACKWARD     = 1
AI_DIR_LEFT         = 2
AI_DIR_RIGHT        = 3
AI_DIR_ATTACK       = 4
AI_DIR_STOP         = 5

ACTION_NONE = {'forward':True, 'backward':False, 'left':False, 'right':False, 'attack':False}

import random

class TeamAI():
    def __init__(self, helper):
        self.helper = helper
        self.enhancement = [1,3,1,2]
        self.action = ACTION_NONE.copy()
        self.player_id = helper.get_self_id()
        self.counter = 0
        self.rotate = 0
        self.wander = False
    
    def reset(self):
        self.action = ACTION_NONE.copy()
    
    def turn_up(self) :

         l = self.helper.get_player_direction()
         # print(l[self.helper.get_self_id()].normalize())
         if abs(l[self.helper.get_self_id()].normalize().x) > 0.01 or abs(l[self.helper.get_self_id()].normalize().y+1)>0.01  :  
                 self.action['left'] = True
        
    def turn_down(self) :

         l = self.helper.get_player_direction()
         # print(l[self.helper.get_self_id()].normalize())
         if abs(l[self.helper.get_self_id()].normalize().x) > 0.01 or abs(l[self.helper.get_self_id()].normalize().y-1)>0.01  :  
                 self.action['left'] = True
        
    def turn_left(self) :

         l = self.helper.get_player_direction()
         # print(l[self.helper.get_self_id()].normalize())
         if abs(l[self.helper.get_self_id()].normalize().x+1) > 0.01 or abs(l[self.helper.get_self_id()].normalize().y)>0.01  :  
                 self.action['left'] = True

    def turn_right(self) :

         l = self.helper.get_player_direction()
         # print(l[self.helper.get_self_id()].normalize())
         if abs(l[self.helper.get_self_id()].normalize().x-1) > 0.01 or abs(l[self.helper.get_self_id()].normalize().y)>0.01  :  
                 self.action['left'] = True  
    
    def wall_distance(self) :#回傳最近的障礙物距離
          return ( (self.helper.get_self_position().x-self.helper.get_nearest_RE_position().x) ** 2 + (self.helper.get_self_position().y-self.helper.get_nearest_RE_position().y) ** 2 )**0.5 
    def innerproduct(self) :#回傳最近牆內積
          return (self.helper.get_self_position().normalize().x * self.helper.get_nearest_RE_position().normalize().x) +  (self.helper.get_self_position().normalize().y * self.helper.get_nearest_RE_position().normalize().y)
    
    def attackornot(self): #如果後方牆壁太近，不發射
         if self.wall_distance() < 3  :
             return False
         return True    

    def auto_attack(self):
        if not self.attackornot():
            return
        if self.helper.get_self_next_attack() == 0:
            self.counter = 10
            self.action['attack'] = True
        if self.counter > 0:
            self.action['forward'] = True 
            self.counter -= 1

    
    def get_nearest_item(self):
        l = self.helper.get_player_direction()

        if self.helper.get_nearest_item_info()['position'].x - self.helper.get_self_position().x > 1:#confirm if the nearest item is on my rght side
            if abs(l[self.helper.get_self_id()].normalize().x-1) > 0.1 or abs(l[self.helper.get_self_id()].normalize().y)>0.1  :
                     
                self.action['forward'] = False
                self.action['left'] = True

        elif self.helper.get_nearest_item_info()['position'].x - self.helper.get_self_position().x < -1:#confirm if the nearest item is on my left side
            if abs(l[self.helper.get_self_id()].normalize().x+1) > 0.1 or abs(l[self.helper.get_self_id()].normalize().y)>0.1  :
                self.action['forward'] = False
                self.action['left'] = True
        else:
            if self.helper.get_nearest_item_info()['position'].y - self.helper.get_self_position().y > 1: #confirm if the nearest item is above me
               if abs(l[self.helper.get_self_id()].normalize().x) > 0.1 or abs(l[self.helper.get_self_id()].normalize().y-1)>0.1  :  
                    self.action['left'] = True
                    self.action['forward'] = False
            elif self.helper.get_nearest_item_info()['position'].y - self.helper.get_self_position().y < 1:#confirm if the nearest item is below me
               if abs(l[self.helper.get_self_id()].normalize().x) > 0.1 or abs(l[self.helper.get_self_id()].normalize().y+1)>0.1  :  
                    self.action['left'] = True
                    self.action['forward'] = False

        
    def decide(self):
        self.reset()
        self.action['forward'] = True

        #print(self.wall_distance())
        if abs((self.helper.get_nearest_item_info()['position'] - self.helper.get_self_position()).magnitude()) > 2:
            self.auto_attack()
        
        self.get_nearest_item()

    
        x = self.helper.get_self_position().x
        y = self.helper.get_self_position().y

        #x_move = self.helper.get_self_direction().x
        #y_move = self.helper.get_self_direction().y

        ss = self.helper.get_nearest_RE_position()
        

        #x_re = self.helper.get_nearest_RE_position().x
        #y_re = self.helper.get_nearest_RE_position().y

        param = 0.8
        l = self.helper.get_player_direction()
        xd = l[self.helper.get_self_id()].normalize().x
        yd = l[self.helper.get_self_id()].normalize().y

        for i in range(1):
            if ss.x - 0.5 <= x + param <= ss.x :

                if ss.y - 0.5 <= y + param <=ss.y:
                   
                    self.action['right'] = False
                    if abs(l[self.helper.get_self_id()].normalize().x+1) > 0.5 or abs(l[self.helper.get_self_id()].normalize().y)>0.5  :
            
                        self.action['forward'] = False
                        self.action['left'] = True
                    #player在左上
                elif ss.y + 0.5 >= y - param >= ss.y:
               
                    self.action['right'] = False
                    if abs(l[self.helper.get_self_id()].normalize().x+1) > 0.5 or abs(l[self.helper.get_self_id()].normalize().y)>0.5  :  
          
                        self.action['forward'] = False
                        self.action['left'] = True
                    #player在左下
            elif ss.x + 0.5 >= x - param >= ss.x :
                if ss.y - 0.5 <= y + param <= ss.y:
                     self.action['left'] = False
                     if abs(l[self.helper.get_self_id()].normalize().x-1) > 0.5 or abs(l[self.helper.get_self_id()].normalize().y)>0.5  :
                     
                        self.action['forward'] = False
                        self.action['left'] = True
                elif ss.y + 0.5 >= y - param >= ss.y:
                    self.action['left'] = False
                    if abs(l[self.helper.get_self_id()].normalize().x-1) > 0.5 or abs(l[self.helper.get_self_id()].normalize().y)>0.5  :  
                       
                        self.action['forward'] = False
                        self.action['left'] = True 
                    #player在右下
        #print( self.action['forward'])
        return self.action
    