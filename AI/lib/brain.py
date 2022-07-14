from API.helper import *
import Const

ACTION_NONE = {'forward':False, 'backward':False, 'left':False, 'right':False, 'attack':False}

class Brain():
    """
    Stores all the common information for AI and libraries.
    """
    def __init__(self, helper: Helper):
        self.helper = helper
        self.action = ACTION_NONE.copy()

        self.id = helper.get_self_id()
        self.obstacles = helper.get_wall_position()
        self.RE_fields = helper.get_RE_field_position()
        self.wall_segments = self.get_wall_segments()

        self.is_attacking = False
        
    def initialize(self):
        """
        Initialize every time TeamAI.decide() is called (every tick).
        """
        self.action = ACTION_NONE.copy()

        self.time = self.helper.get_game_time()
        self.position = self.helper.get_player_position()[self.id]
        self.direction = self.helper.get_player_direction()[self.id]
        self.speed = self.helper.get_player_speed()[self.id]

        self.next_attack = self.helper.get_player_next_attack()[self.id]
        self.alive = self.helper.get_player_respawn_time()[self.id] == 0
    
    def get_wall_segments(self):
        """
        Decompose all obstacles and RE_fields into wall segments.
        """
        delta = [pg.Vector2(-1, -1), pg.Vector2(1, -1), pg.Vector2(1, 1), pg.Vector2(-1, 1), pg.Vector2(-1, -1)]
        ret = []
        for pos in self.obstacles:
            for i in range(4):
                ret.append((pos+delta[i]*Const.OBSTACLE_RADIUS, pos+delta[i+1]*Const.OBSTACLE_RADIUS))
        for pos in self.RE_fields:
            for i in range(4):
                ret.append((pos+delta[i]*Const.RE_FIELD_RADIUS, pos+delta[i+1]*Const.RE_FIELD_RADIUS))
        return ret


        
        




