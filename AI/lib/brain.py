from collections import Counter
import numpy as np
import math

from API.helper import *
from AI.lib.utils import *
from AI.lib.Const import *
import Const

class Brain():
    """
    Stores all the common information for AI and libraries.
    """
    def __init__(self, helper: Helper):
        self.helper = helper
        self.action = ACTION_NONE.copy()
        self.id = helper.get_self_id()
        self.time = helper.get_game_time()
        self.obstacles = helper.get_wall_position()
        self.RE_fields = helper.get_RE_field_position()
        # self.wall_segments = self.get_wall_segments()

        self.mode = Mode.IDLE

        self.edges = [[] for i in range(LENGTH ** 2)] # tuple(node, weight, direc), node indexed by index()
        self.isWalkable = [True] * (LENGTH ** 2)    # Construct Graph 
        self.isDanger = [False] * (LENGTH ** 2)     # RE_Fields
        self.isObstacle = [False] * (LENGTH ** 2)   # All obstacles
        self.InitGraph()
        
    def Initialize(self) -> None:
        """
        Initialize every time TeamAI.decide() is called (every tick).
        """
        self.action = ACTION_NONE.copy()

        self.time = self.helper.get_game_time()
        self.position = self.helper.get_self_position()
        self.direction = self.helper.get_self_direction()
        self.speed = self.helper.get_self_speed()

        self.nextAttack = self.helper.get_self_next_attack()
        self.respawning = self.helper.get_self_is_respawning()
    
    def GetWallSegments(self) -> list:
        """
        Decompose all obstacles and RE_fields into wall segments.
        """
        delta = [pg.Vector2(-1, -1), pg.Vector2(1, -1), pg.Vector2(1, 1), pg.Vector2(-1, 1), pg.Vector2(-1, -1)]
        walls = Counter()
        for pos in self.obstacles:
            for i in range(4):
                p1, p2 = (pos+delta[i]*Const.OBSTACLE_RADIUS, pos+delta[i+1]*Const.OBSTACLE_RADIUS)
                walls[(p1.x, p1.y, p2.x, p2.y)] += 1
        for pos in self.RE_fields:
            for i in range(4):
                p1, p2 = (pos+delta[i]*Const.RE_FIELD_RADIUS, pos+delta[i+1]*Const.RE_FIELD_RADIUS)
                walls[(p1.x, p1.y, p2.x, p2.y)] += 1
        return [(pg.Vector2(k[0], k[1]), pg.Vector2(k[2], k[3])) for k, v in walls.items() if v == 1]
        
    def InitGraph(self) -> None:
        for pos in self.RE_fields:
            self.isWalkable[Index(pos)] = False
            self.isDanger[Index(pos)] = True
            self.isObstacle[Index(pos)] = True
            for i in range(8):
                npos = pos + DXY[i] * WIDTH
                self.isWalkable[Index(npos)] = False
                self.isDanger[Index(npos)] = True
                self.isObstacle[Index(npos)] = True
                for j in range(4):
                    nnpos = npos + DXY[j] * WIDTH
                    self.isWalkable[Index(nnpos)] = False
                    self.isDanger[Index(nnpos)] = True
        
        for pos in self.obstacles:
            self.isWalkable[Index(pos)] = False
            self.isObstacle[Index(pos)] = True
            for i in range(8):
                npos = pos + DXY[i] * WIDTH
                self.isWalkable[Index(npos)] = False
                self.isObstacle[Index(npos)] = True
        
        for i in np.arange(0, Const.ARENA_GRID_COUNT, WIDTH):
            pos = pg.Vector2(0, i)
            self.isWalkable[Index(pos)] = False
            self.isDanger[Index(pos)] = True
            for j in range(4):
                npos = pos + DXY[j] * WIDTH
                self.isWalkable[Index(npos)] = False
                self.isDanger[Index(npos)] = True
            pos = pg.Vector2(i, 0)
            self.isWalkable[Index(pos)] = False
            self.isDanger[Index(pos)] = True
            for j in range(4):
                npos = pos + DXY[j] * WIDTH
                self.isWalkable[Index(npos)] = False
                self.isDanger[Index(npos)] = True
            EDGE = Const.ARENA_GRID_COUNT - WIDTH
            self.isWalkable[Index(pg.Vector2(EDGE, i))] = False
            self.isWalkable[Index(pg.Vector2(i, EDGE))] = False
            self.isDanger[Index(pg.Vector2(EDGE, i))] = False
            self.isDanger[Index(pg.Vector2(i, EDGE))] = False


        for x in np.arange(0, Const.ARENA_GRID_COUNT, WIDTH):
            for y in np.arange(0, Const.ARENA_GRID_COUNT, WIDTH):
                pos = pg.Vector2(x, y)
                for i in range(8):
                    npos = pos + DXY[i] * WIDTH
                    if InGraph(npos) and self.isWalkable[Index(npos)]:
                        if i>=4 and (self.isObstacle[Index(pos+DXY[i-4]*WIDTH)] or self.isObstacle[Index(pos+DXY[(i-3)%4]*WIDTH)]):
                            continue
                        self.edges[Index(pos)].append((Index(npos), DW[i], i))

    def SegmentClearCheck(self, p1: pg.Vector2, p2: pg.Vector2) -> bool:
        """
        Check if segment(p1, p2) has no block in between.
        Method: Simulate a shot from p1 to p2.
        """
        current = p1.copy()
        delta = p2 - p1
        if delta.length() <= SEGMENT_CLEAR_SIMULATE_LENGTH * 2:
            return True
        delta.scale_to_length(SEGMENT_CLEAR_SIMULATE_LENGTH)
        cnt = 0
        cntMax = Const.ARENA_GRID_COUNT * math.sqrt(2) / SEGMENT_CLEAR_SIMULATE_LENGTH
        while Index(current) != Index(p2) and cnt <= cntMax:
            current += delta
            cnt += 1
            if self.isObstacle[Index(current)]:
                return False
        return True
    
    def SegmentSafeCheck(self, p1: pg.Vector2, p2: pg.Vector2) -> bool:
        """
        Check if segment(p1, p2) is safe.
        Method: Simulate a shot from p1 to p2.
        """
        current = p1.copy()
        delta = p2 - p1
        if delta.length() <= SEGMENT_CLEAR_SIMULATE_LENGTH * 2:
            return True
        delta.scale_to_length(SEGMENT_CLEAR_SIMULATE_LENGTH)
        cnt = 0
        cntMax = Const.ARENA_GRID_COUNT * math.sqrt(2) / SEGMENT_CLEAR_SIMULATE_LENGTH
        while Index(current) != Index(p2) and cnt <= cntMax:
            current += delta
            cnt += 1
            if self.isDanger[Index(current)]:
                return False
        return True
    
    def KickCheck(self, direction: pg.Vector2, power: float = -1, targetId: int = -1) -> bool:
        """
        Check if player will be safe after receiving a kick.
        """
        if targetId == -1:
            targetId = self.id
        kick = direction.copy()
        if power != -1:
            kick.scale_to_length(power)
        
        pos = self.helper.get_player_position()[targetId]
        radius = kick.copy()
        radius.scale_to_length(Const.PLAYER_RADIUS)
        if not self.SegmentSafeCheck(pos, pos+radius+kick):
            return False
        radius.rotate(90)
        return self.SegmentSafeCheck(pos+radius, pos+radius+kick) and self.SegmentSafeCheck(pos-radius, pos-radius+kick)

    def ShootCheck(self, multiplier: float = 1.0):
        """
        Check if it is safe to shoot at current position.
        """
        return self.KickCheck(-self.direction, self.helper.get_self_kick() * multiplier)