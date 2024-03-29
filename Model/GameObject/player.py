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
    def __init__(self, model, player_id: int, name: str, is_AI: bool):
        super().__init__(model, copy.deepcopy(Const.PLAYER_INIT_POSITION[player_id]), Const.PLAYER_RADIUS)

        self.player_id = player_id
        self.score = 0
        self.base_speed = Const.PLAYER_BASE_SPEED
        self.gun = Normal_Gun(model, self)
        self.repulsion_resistance = Const.PLAYER_REPULSION_RESISTANCE

        self.attack_speed = Const.PLAYER_ATTACK_SPEED
        self.attack_kick = Const.PLAYER_ATTACK_KICK
        self.attack_accuracy = Const.PLAYER_ATTACK_ACCURACY
        self.attack_ammo = Const.PLAYER_ATTACK_AMMO
        self.aux_line_length = Const.PLAYER_AUX_LINE_LENGTH

        self.bullet_lifespan = Const.BULLET_LIFESPAN
        self.bullet_trace_time = Const.BULLET_TRACE_TIME
        self.bullet_repulsion = Const.BULLET_REPULSION

        self.quota_attack_speed = Const.PLAYER_QUOTA_ATTACK_SPEED
        self.quota_repulsion = Const.PLAYER_QUOTA_REPULSION
        self.quota_attack_accuracy = Const.PLAYER_QUOTA_ATTACK_ACCURACY

        self.death_count = 0
        self.respawn_count = Const.PLAYER_MAX_RESPAWN_COUNT[player_id]
        self.respawn_timer = 0

        self.player_name = name
        self.is_AI = is_AI

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

                self.model.ev_manager.post(EventPlayerHitWall())
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
        new_speed = self.base_speed * self.direction * direction
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
        if gun_type == Const.GUN_TYPE_NORMAL_GUN:
            self.gun = Normal_Gun(self.model, self)
        elif gun_type == Const.GUN_TYPE_MACHINE_GUN:
            self.gun = Machine_Gun(self.model, self)
        elif gun_type == Const.GUN_TYPE_SNIPER:
            self.gun = Sniper(self.model, self)
        elif gun_type == Const.GUN_TYPE_SHOTGUN:
            self.gun = Shotgun(self.model, self)
        self.model.ev_manager.post(EventPlayerSwitchGun(self.player_id, gun_type))

    def quota_enough(self, buff_type):
        '''
        Check if the quota of a buff is enough
        '''
        if buff_type == Const.BUFF_TYPE_ATTACK_SPEED:
            return self.quota_attack_speed > 0
        if buff_type == Const.BUFF_TYPE_REPULSION:
            return self.quota_repulsion > 0
        if buff_type == Const.BUFF_TYPE_ATTACK_ACCURACY:
            return self.quota_attack_accuracy > 0


    def buff(self, buff_type):
        '''
        Add permanent buff to the player.
        '''
        if buff_type == Const.BUFF_TYPE_ATTACK_SPEED:
            self.attack_speed += Const.BUFF_VALUE_ATTACK_SPEED
            self.quota_attack_speed -= 1
        if buff_type == Const.BUFF_TYPE_REPULSION:
            self.bullet_repulsion += Const.BUFF_VALUE_REPULSION
            self.quota_repulsion -= 1
        if buff_type == Const.BUFF_TYPE_ATTACK_ACCURACY:
            self.attack_accuracy += Const.BUFF_VALUE_ATTACK_ACCURACY
            self.quota_attack_accuracy -= 1
        self.model.ev_manager.post(EventPlayerBuffed(self.player_id, buff_type))

    
    def kill(self):
        '''
        Kill the player.
        '''
        if self.respawn_count <= 0:
            super().kill()
            self.score += Const.PLAYER_ALIVE_SCORE[self.model.death_cnt]
            self.model.ev_manager.post(EventPlayerRemove(self.player_id))
        
        self.respawn_count -= 1
        self.respawn_timer = Const.PLAYER_RESPAWN_TIME
        self.death_count += 1
        self.position = copy.deepcopy(Const.PLAYER_INIT_POSITION[self.player_id])
        self.speed = Vector2(0, 0)
        self.gun = Normal_Gun(self.model, self)
    
    def respawning(self):
        return self.respawn_timer > 0
    
    def invisible(self):
        return self.respawning() or self.killed()

    def enhance(self, enhancement: list):
        '''
        apply the bonus enhancement
        '''
        self.base_speed *= (1 + Const.ENHANCEMENT_BASE_SPEED * enhancement[0])
        self.attack_speed *= (1 + Const.ENHANCEMENT_ATTACK_SPEED \
                * enhancement[1])
        self.bullet_repulsion *= (1 + Const.ENHANCEMENT_BULLET_REPULSION \
                * enhancement[2])
        self.repulsion_resistance *= (1 \
                + Const.ENHANCEMENT_REPULSION_RESISTANCE \
                * enhancement[3])
