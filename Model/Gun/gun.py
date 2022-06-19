import Const
import math
from EventManager.EventManager import *
from Model.GameObject.bullet import *

class Gun:
    '''
    An abstract class for guns.
    '''
    def __init__(self, model, player, gun_type):
        self.model = model
        self.player = player
        self.type = gun_type
        self.cd_time = 0

        self.use_time = Const.GUN_USE_TIME[gun_type] * Const.FPS
        self.attack_cd_multiplier = Const.GUN_ATTACK_CD_MULTIPLIER[gun_type]
        self.attack_kick_multiplier = Const.GUN_ATTACK_KICK_MULTIPLIER[gun_type]
        self.aux_line_length_multiplier = Const.GUN_AUX_LINE_LENGTH_MULTIPLIER[gun_type]

        self.bullet_trace_time_multiplier = Const.GUN_BULLET_TRACE_TIME_MULTIPLIER[gun_type]
        self.bullet_repulsion_multiplier = Const.GUN_BULLET_REPULSION_MULTIPLIER[gun_type]
    
    def tick(self):
        '''
        Run whenever EventEveryTick() arises.
        '''
        if self.in_cd():
            self.cd_time -= 1
        
        if self.in_use():
            self.use_time -= 1
        else:
            self.player.switch_gun(Const.GUN_TYPE_NORMAL_GUN)
    
    def shoot(self):
        '''
        Fire a bullet.
        '''
        if self.in_cd():
            return
        
        player = self.player
        self.cd_time = round(player.attack_cd * self.attack_cd_multiplier * Const.FPS)
        player.knock_back(player.attack_kick * self.attack_kick_multiplier, -player.direction)
        self.model.bullets.append(Bullet(self.model, player, player.direction, \
                                         player.bullet_trace_time * self.bullet_trace_time_multiplier, \
                                         player.bullet_repulsion * self.bullet_repulsion_multiplier, self.type))
        self.model.ev_manager.post(EventPlayerAttackSuccess(player.player_id, self.type))
    
    def in_cd(self):
        '''
        Check if the gun is still in cooldown.
        '''
        return self.cd_time > 0
    
    def in_use(self):
        '''
        Check if the gun's using time does not run out.
        '''
        return self.use_time > 0


class Normal_Gun(Gun):
    '''
    Represents a normal gun.
    '''
    def __init__(self, model, player):
        super().__init__(model, player, Const.GUN_TYPE_NORMAL_GUN)


class Machine_Gun(Gun):
    '''
    Represents a machine gun.
    '''
    def __init__(self, model, player):
        super().__init__(model, player, Const.GUN_TYPE_MACHINE_GUN)


class Sniper(Gun):
    '''
    Represents a sniper.
    '''
    def __init__(self, model, player):
        super().__init__(model, player, Const.GUN_TYPE_SNIPER)


class Shotgun(Gun):
    '''
    Represents a shotgun.
    '''
    def __init__(self, model, player):
        super().__init__(model, player, Const.GUN_TYPE_SHOTGUN)
    
    def shoot(self):
        '''
        Fire 5 bullets.
        '''
        if self.in_cd():
            return
        
        player = self.player
        self.cd_time = player.attack_cd * self.attack_cd_multiplier * Const.FPS
        player.knock_back(player.attack_kick * self.attack_kick_multiplier, -player.direction)
        for delta in range(-2, 3, 1):
            direction = player.direction.rotate_rad(delta * (Const.SHOTGUN_ATTACK_ANGLE / 2))
            self.model.bullets.append(Bullet(self.model, player, direction, \
                                             player.bullet_trace_time * self.bullet_trace_time_multiplier, \
                                             player.bullet_repulsion * self.bullet_repulsion_multiplier, self.type))
        self.model.ev_manager.post(EventPlayerAttackSuccess(player.player_id, self.type))