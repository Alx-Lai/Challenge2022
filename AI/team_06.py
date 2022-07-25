# AI_DIR_FORWARD      = 0
# AI_DIR_BACKWARD     = 1
# AI_DIR_LEFT         = 2
# AI_DIR_RIGHT        = 3
# AI_DIR_ATTACK       = 4
# AI_DIR_STOP         = 5

# ACTION_NONE = {'forward':False, 'backward':False, 'left':False, 'right':False, 'attack':False}

# import random

# class TeamAI():
#     def __init__(self, helper):
#         self.helper = helper
#         self.enhancement = [0, 0, 0, 0]
#         self.action = ACTION_NONE.copy()
#         self.player_id = helper.get_self_id()
#         self.counter = 0#希望連續旋轉量
#         self.rotate = 0#
#         self.wander = False
#         self.temp = 0
#         self.place = self.helper.get_self_position()
#         self.action = ACTION_NONE.copy()




#     def reset(self):
#         self.action = ACTION_NONE.copy()
    
#     def auto_attack(self):
#         if self.helper.get_self_next_attack() == 0:
#             self.counter = 10
#             self.action['attack'] = True
#         if self.counter > 0:
#             self.action['forward'] = True 
#             self.counter -= 1
    
#     def auto_wander(self):
#         if self.wander == 0:
#             if random.randint(0, 1000) == 0:
#                 self.wander = random.randint(150, 600)
#         if self.wander > 0:
#             self.action['forward'] = True
#             self.wander -= 1
    
#     def rotate_to(self,v):
#         if abs(self.helper.get_self_direction().angle_to(v)) > 2:
#             self.action['right'] =True
#         else:
#             self.action['left'] = True
#     def goback(self,v):
#         if (self.place - v):
#             self.action['forward'] = True
#         else:
#             self.action['backward'] = True
#             def red(self):
#         allposition = self.helper.get_player_position()
#         red = self.helper.get_nearest_RE_position()
#         #避開紅色
#         if red.x-self.position.x<=5 or red.y-self.position.y<=5:
#             m=(red.y-self.position.y)/(red.x-self.position.x)
#             while self.face!=m:
#                 if m > 0:
#                     return 2
#                 elif m < 0:
#                     return 3
#             if self.helper.get_self_next_attack()==0:
#                 self.action['attack']=True
#             else:
#                 return 1
#     def red(self):
#         allposition = self.helper.get_player_position()
#         red = self.helper.get_nearest_RE_position()
#         #避開紅色
#         if red.x-self.position.x<=5 or red.y-self.position.y<=5:
#             m=(red.y-self.position.y)/(red.x-self.position.x)
#             while self.face!=m:
#                 if m > 0:
#                     return 2
#                 elif m < 0:
#                     return 3
#             if self.helper.get_self_next_attack()==0:
#                 self.action['attack']=True
#             else:
#                 return 1
#     def decide(self):
#         self.reset()
        
#         if self.wander == 0:
#             self.auto_attack()
#         self.auto_wander()
        
#         if self.rotate == 0:
            
#             self.rotate = random.randint(-180, 180)
            
#         if 
#             if self.rotate != 0:
#                 if self.rotate > 0:
#                     self.rotate -= 1
#                     if self.rotate > 20:
#                         self.action['left'] = True
#                 else:
#                     self.rotate += 1
#                     if self.rotate < -20:
#                         self.action['right'] = True
#                 self.counter = 2
            
#         if self.counter > 0:
#             self.action['forward'] = True 
#             self.counter -= 1
#         # else:
#         #     self.action['forward'] = False
#         if self.helper.get_self_next_attack() == 0:
#             self.action['attack'] = True
#         self.rotate_to(self.place - self.helper.get_self_position())
#         self.goback(self.helper.get_self_position())
        


#         return self.action
        #回傳原點的xy存起來
        #隨機轉再開砲



AI_DIR_FORWARD      = 0
AI_DIR_BACKWARD     = 1
AI_DIR_LEFT         = 2
AI_DIR_RIGHT        = 3
AI_DIR_ATTACK       = 4
AI_DIR_STOP         = 5

ACTION_NONE = {'forward':False, 'backward':False, 'left':False, 'right':False, 'attack':False}

import random

class TeamAI():
    def __init__(self, helper):
        self.helper = helper
        self.enhancement = [1,1,1,2]
        self.action = ACTION_NONE.copy()
        self.player_id = helper.get_self_id()
        self.counter = 0#希望連續旋轉量
        self.rotate = 0#
        self.wander = False
        self.temp = 0
        self.place = self.helper.get_self_position()
        self.action = ACTION_NONE.copy()




    def reset(self):
        self.action = ACTION_NONE.copy()
    
    # def auto_attack(self):
    #     if self.helper.get_self_next_attack() == 0:
    #         self.counter = 10
    #         self.action['attack'] = True
    #     if self.counter > 0:
    #         self.action['forward'] = True 
    #         self.counter -= 1
    
    def auto_wander(self):
        if self.wander == 0:
            if random.randint(0, 1000) == 0:
                self.wander = random.randint(150, 600)
        if self.wander > 0:
            self.action['forward'] = True
            self.wander -= 1
    
    def rotate_to(self,v):
        if abs(self.helper.get_self_direction().angle_to(v)) > 2:
            self.action['right'] =True
        else:
            self.action['left'] = True
    # def goback(self,v):
    #     if (self.place - v):
    #         self.action['forward'] = True
    #     else:
    #         self.action['backward'] = True



    def goback(self,v):
        if (self.place - v):
            self.action['forward'] = True
        else:
            self.action['backward'] = True

    # def red(self):
    #     red = self.helper.get_nearest_RE_position()
    #     #避開紅色
    #     if red.x-self.position.x<=5 or red.y-self.position.y<=5:
    #         m=(red.y-self.position.y)/(red.x-self.position.x)
    #         if self.face!=m:
    #             if m > 0:
    #                 return 2
    #             elif m < 0:
    #                 return 3
    #         if self.helper.get_self_next_attack()==0:
    #             self.action['attack']=True
    #         else:
    #             return 1


    def decide(self):
        self.reset()

        # if self.wander == 0:
        #     self.auto_attack()
        # self.auto_wander()
        


        #避開紅色
        reds = self.helper.get_nearest_RE_position()

        if self.rotate == 0:
            self.rotate = random.randint(-180, 180)

        makechange = False
        if reds.x - self.place.x == 0:
            m = (reds.y-self.place.y)/(reds.x-self.place.x + 0.00001) 
        else:
            m = (reds.y-self.place.y)/(reds.x-self.place.x) 

        if reds.x-self.place.x<=5 or reds.y-self.place.y<=5:
            makechange = True

        if makechange == True:
            self.rotate = random.randint(-180, 180)


        elif self.rotate != 0:
            if self.rotate > 0:
                self.rotate -= 1
                if self.rotate > 20:
                    if m > 0 and makechange:
                        self.action['left'] = True
            else:
                self.rotate += 1
                if self.rotate < -20:
                    if m > 0 and makechange:
                        self.action['right'] = True
            self.counter = 5

        
            
        if self.counter > 0:
            self.action['forward'] = True 
            self.counter -= 1
        # if self.helper.get_self_next_attack() == 0:
        #     self.action['attack'] = True



        self.rotate_to(self.place - self.helper.get_self_position())
        self.goback(self.helper.get_self_position())
        
        
        if makechange == True:
            randomnum1 = random.randint(-30, 180)
            randomnum2 = random.randint(-180, 30)

            if randomnum1 > 0:
                self.action['forward'] = True 
            else:
                self.action['forward'] = False


        if makechange and randomnum2 > 0:
            self.action['attack'] = False 
        else:
            self.action['attack'] = True 


        return self.action



