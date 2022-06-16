import Const
import math
from Model.GameObject.bullet import *

class Normal_Gun:
    '''
    Represents a normal gun.
    '''
    def __init__(self, model, player):
        self.model = model
        self.player = player
        self.type = Const.GUN_TYPE_NORMAL_GUN
        self.use_time = math.inf
        self.cd_time = 0

        self.attack_cd_multiplier = 1
        self.attack_kick_multiplier = 1
        self.aux_line_length_multiplier = 1

        self.bullet_trace_time_multiplier = 1
        self.bullet_repulsion_multiplier = 1
    
    def tick(self):
        if self.in_cd():
            self.cd_time -= 1
        
        if self.in_use():
            self.use_time -= 1
        else:
            self.player.gun = Normal_Gun(self.model, self.player)
    
    def shoot(self):
        if self.in_cd():
            return
        
        player = self.player
        self.cd_time = player.attack_cd * self.attack_cd_multiplier * Const.FPS
        player.knock_back(player.attack_kick * self.attack_kick_multiplier, -player.direction)
        self.model.items.append(Bullet(self.model, player, player.direction, \
                                       player.bullet_trace_time * self.bullet_trace_time_multiplier, \
                                       player.bullet_repulsion * self.bullet_repulsion_multiplier, self.type))
    
    def in_cd(self):
        '''
        Check if the gun is still in cooldown.
        '''
        return self.cd_time > 0
    
    def in_use(self):
        return self.use_time > 0


class Machine_Gun(Normal_Gun):
    '''
    Represents a machine gun.
    '''
    def __init__(self, model, player):
        super().__init__(model, player)
        self.type = Const.GUN_TYPE_MACHINE_GUN
        self.use_time = 10 * Const.FPS

        self.attack_cd_multiplier = 0.25
        self.attack_kick_multiplier = 0.25
        self.aux_line_length_multiplier = 1

        self.bullet_trace_time_multiplier = 1
        self.bullet_repulsion_multiplier = 1/3


class Sniper(Normal_Gun):
    '''
    Represents a sniper.
    '''
    def __init__(self, model, player):
        super().__init__(model, player)
        self.type = Const.GUN_TYPE_SNIPER
        self.use_time = 20 * Const.FPS

        self.attack_cd_multiplier = 1
        self.attack_kick_multiplier = 1.5
        self.aux_line_length_multiplier = 1

        self.bullet_trace_time_multiplier = 2
        self.bullet_repulsion_multiplier = 2


class Shotgun(Normal_Gun):
    '''
    Represents a shotgun.
    '''
    def __init__(self, model, player):
        super().__init__(model, player)
        self.type = Const.GUN_TYPE_SHOTGUN
        self.use_time = 20 * Const.FPS
    
    def shoot(self):
        if self.in_cd():
            return
        
        player = self.player
        self.cd_time = player.attack_cd * self.attack_cd_multiplier * Const.FPS
        player.knock_back(player.attack_kick * self.attack_kick_multiplier, -player.direction)
        for delta in range(-2, 3, 1):
            direction = player.direction.rotate_rad(delta * (math.pi / 36))
            self.model.items.append(Bullet(self.model, player, direction, \
                                           player.bullet_trace_time * self.bullet_trace_time_multiplier, \
                                           player.bullet_repulsion * self.bullet_repulsion_multiplier, self.type))