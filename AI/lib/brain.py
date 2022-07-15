from collections import Counter
from turtle import width
import numpy as np

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

        self.isAttacking = False

        self.edges = [[] for i in range(LENGTH ** 2)] # tuple(node, weight, direc), node indexed by index()
        self.safeNodes = [True] * (LENGTH ** 2)
        self.blocks = [False] * (LENGTH ** 2)
        self.InitGraph()
        
    def Initialize(self):
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
    
    def GetWallSegments(self):
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
        
    def InitGraph(self):
        for pos in self.RE_fields:
            self.safeNodes[Index(pos)] = False
            self.blocks[Index(pos)] = True
            for i in range(8):
                npos = pos + DXY[i] * WIDTH
                self.safeNodes[Index(npos)] = False
                self.blocks[Index(npos)] = True
                for j in range(4):
                    nnpos = npos + DXY[j] * WIDTH
                    self.safeNodes[Index(nnpos)] = False
        
        for pos in self.obstacles:
            self.safeNodes[Index(pos)] = False
            self.blocks[Index(pos)] = True
            for i in range(8):
                npos = pos + DXY[i] * WIDTH
                self.safeNodes[Index(npos)] = False
                self.blocks[Index(npos)] = True
        
        for i in np.arange(0, Const.ARENA_GRID_COUNT, WIDTH):
            pos = pg.Vector2(0, i)
            self.safeNodes[Index(pos)] = False
            for j in range(4):
                npos = pos + DXY[j] * WIDTH
                self.safeNodes[Index(npos)] = False
            pos = pg.Vector2(i, 0)
            self.safeNodes[Index(pos)] = False
            for j in range(4):
                npos = pos + DXY[j] * WIDTH
                self.safeNodes[Index(npos)] = False
            EDGE = Const.ARENA_GRID_COUNT - WIDTH
            self.safeNodes[Index(pg.Vector2(EDGE, i))] = False
            self.safeNodes[Index(pg.Vector2(i, EDGE))] = False

        for x in np.arange(0, Const.ARENA_GRID_COUNT, WIDTH):
            for y in np.arange(0, Const.ARENA_GRID_COUNT, WIDTH):
                pos = pg.Vector2(x, y)
                for i in range(8):
                    npos = pos + DXY[i] * WIDTH
                    if InGraph(npos) and self.safeNodes[Index(npos)]:
                        if i>=4 and (self.blocks[Index(pos+DXY[i-4]*WIDTH)] or self.blocks[Index(pos+DXY[(i-3)%4]*WIDTH)]):
                            continue
                        self.edges[Index(pos)].append((Index(npos), DW[i], i))
    



