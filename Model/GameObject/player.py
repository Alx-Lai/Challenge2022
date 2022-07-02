import Const
import copy
from EventManager.EventManager import *
from Model.GameObject.base_game_object import *
from Model.GameObject.obstacle import *
from Model.Gun.gun import *

class Player(Base_Circle_Object):
    '''
    Represent a player.
    '''
    def __init__(self, model, player_id: int):
        super().__init__(model, copy.deepcopy(Const.PLAYER_INIT_POSITION[player_id]), Const.PLAYER_RADIUS)

        self.player_id = player_id
        self.score = 0
        self.gun = Normal_Gun(model, self)

        self.attack_cd = Const.PLAYER_ATTACK_CD
        self.attack_kick = Const.PLAYER_ATTACK_KICK
        self.aux_line_length = Const.PLAYER_AUX_LINE_LENGTH

        self.bullet_trace_time = Const.BULLET_TRACE_TIME
        self.bullet_repulsion = Const.BULLET_REPULSION

        self.quota_attack_cd = Const.PLAYER_QUOTA_ATTACK_CD
        self.quota_repulsion = Const.PLAYER_QUOTA_REPULSION
        self.quota_aux_line_length = Const.PLAYER_QUOTA_AUX_LINE_LENGTH

        self.death_count = 0
        self.respawn_count = Const.PLAYER_MAX_RESPAWN_COUNT[player_id]
        self.respawn_timer = 0

    def tick(self):
        '''
        Run whenever EventEveryTick() arises.
        '''
        if self.respawning():
            self.respawn_timer -= 1
        
        super().tick()
        self.gun.tick()
        if self.x <= Const.PLAYER_RADIUS or self.x >= Const.ARENA_GRID_COUNT-Const.PLAYER_RADIUS or \
           self.y <= Const.PLAYER_RADIUS or self.y >= Const.ARENA_GRID_COUNT-Const.PLAYER_RADIUS :
            if not self.invisible():
                self.model.ev_manager.post(EventPlayerDead(self.player_id))
                self.kill()
                return
        
        collide_edge = False # whether the bullet collides the edges of the obstacles (instead of the corners)
        collided_obstacles = []
        for obstacle in self.model.obstacles:
            if self.collide_object(obstacle):
                if isinstance(obstacle, RE_Field) and not self.invisible():
                    self.model.ev_manager.post(EventPlayerDead(self.player_id))
                    self.kill()
                    return

                dx = (self.position - obstacle.position).x
                dy = (self.position - obstacle.position).y
                if abs(dx) < obstacle.radius or abs(dy) < obstacle.radius:
                    collide_edge = True
                    collided_obstacles.append((True, obstacle))
                else:
                    collided_obstacles.append((False, obstacle))
        if len(collided_obstacles):
            if collide_edge:
                for obstacle in collided_obstacles:
                    if not obstacle[0]:
                        collided_obstacles.remove(obstacle)
            for obstacle in collided_obstacles:
                normal_vector = obstacle[1].clip_object_position(self)
                self.speed = self.speed.reflect(normal_vector)
                
    def move_direction(self, direction: int):
        '''
        Increase the player's speed along it's facing direction.
        Can move either forward or backward.
        '''
        new_speed = Const.PLAYER_BASE_SPEED * self.direction * direction
        self.speed = (self.speed * 9 + new_speed) / 10

    def stop_moving(self):
        '''
        Decrease the player's speed.
        '''
        self.speed = (self.speed * 9) / 10

    def rotate(self, direction: int):
        '''
        Rotate the player leftward or rightward.
        '''
        self.direction = self.direction.rotate_rad(Const.PLAYER_ROTATION_SPEED * direction)

    def knock_back(self, distance, direction):
        '''
        Repulse the player along the given direction.
        '''
        self.speed += distance * direction

    def attack(self):
        '''
        Fire a bullet towards the player's facing direction.
        '''
        self.gun.shoot()
    
    def switch_gun(self, gun_type):
        '''
        Switch the player's gun.
        '''
        match gun_type:
            case Const.GUN_TYPE_NORMAL_GUN:
                self.gun = Normal_Gun(self.model, self)
            case Const.GUN_TYPE_MACHINE_GUN:
                self.gun = Machine_Gun(self.model, self)
            case Const.GUN_TYPE_SNIPER:
                self.gun = Sniper(self.model, self)
            case Const.GUN_TYPE_SHOTGUN:
                self.gun = Shotgun(self.model, self)
        self.model.ev_manager.post(EventPlayerSwitchGun(self.player_id, gun_type))

    def quota_enough(self, buff_type):
        '''
        Check if the quota of a buff is enough
        '''
        match buff_type:
            case Const.BUFF_TYPE_ATTACK_CD:
                return self.quota_attack_cd > 0
            case Const.BUFF_TYPE_REPULSION:
                return self.quota_repulsion > 0
            case Const.BUFF_TYPE_AUX_LINE_LENGTH:
                return self.quota_aux_line_length > 0


    def buff(self, buff_type):
        '''
        Add permanent buff to the player.
        '''
        match buff_type:
            case Const.BUFF_TYPE_ATTACK_CD:
                self.attack_cd += Const.BUFF_VALUE_ATTACK_CD
                self.quota_attack_cd -= 1
            case Const.BUFF_TYPE_REPULSION:
                self.bullet_repulsion += Const.BUFF_VALUE_REPULSION
                self.quota_repulsion -= 1
            case Const.BUFF_TYPE_AUX_LINE_LENGTH:
                self.aux_line_length += Const.BUFF_VALUE_AUX_LINE_LENGTH
                self.quota_aux_line_length -= 1
        self.model.ev_manager.post(EventPlayerBuffed(self.player_id, buff_type))

    
    def kill(self):
        '''
        Kill the player.
        '''
        if self.respawn_count <= 0:
            self.score += Const.PLAYER_ALIVE_SCORE[self.model.death_cnt]
            self.model.ev_manager.post(EventPlayerRemove(self.player_id))
            print(self.player_id, self.score)
            super().kill()
        
        self.respawn_count -= 1
        self.respawn_timer = Const.PLAYER_RESPAWN_TIME
        self.death_count += 1
        self.position = copy.deepcopy(Const.PLAYER_INIT_POSITION[self.player_id])
        self.speed = Vector2(0, 0)
        self.gun = Normal_Gun(self.model, self)
    
    def respawning(self):
        '''
        Check if the player is respawning.
        '''
        return self.respawn_timer > 0
    
    def invisible(self):
        '''
        Check if the player is invisible (cannot be seen/hit).
        '''
        return self.respawning() or self.killed()
