from collections import Counter
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

        self.is_attacking = False

        self.edges = [[] for i in range(LENGTH ** 2)] # tuple(node, weight, direc), node indexed by index()
        self.safe_nodes = [True] * (LENGTH ** 2)
        self.init_graph()
        
    def initialize(self):
        """
        Initialize every time TeamAI.decide() is called (every tick).
        """
        self.action = ACTION_NONE.copy()

        self.time = self.helper.get_game_time()
        self.position = self.helper.get_self_position()
        self.direction = self.helper.get_self_direction()
        self.speed = self.helper.get_self_speed()

        self.next_attack = self.helper.get_self_next_attack()
        self.respawning = self.helper.get_self_is_respawning()
    
    def get_wall_segments(self):
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
        
    def init_graph(self):
        for pos in self.RE_fields:
            self.safe_nodes[index(pos)] = False
            for i in range(8):
                nx = pos.x + WIDTH * DX[i]
                ny = pos.y + WIDTH * DY[i]
                self.safe_nodes[index(nx, ny)] = False
                for j in range(4):
                    nnx = nx + WIDTH * DX[j]
                    nny = ny + WIDTH * DY[j]
                    self.safe_nodes[index(nnx, nny)] = False
        
        for pos in self.obstacles:
            self.safe_nodes[index(pos)] = False
            for i in range(8):
                nx = pos.x + WIDTH * DX[i]
                ny = pos.y + WIDTH * DY[i]
                self.safe_nodes[index(nx, ny)] = False
        
        for i in np.arange(0, Const.ARENA_GRID_COUNT, WIDTH):
            self.safe_nodes[index(0, i)] = False
            for j in range(4):
                nx = 0 + WIDTH * DX[j]
                ny = i + WIDTH * DY[j]
                self.safe_nodes[index(nx, ny)] = False
            self.safe_nodes[index(i, 0)] = False
            for j in range(4):
                nx = i + WIDTH * DX[j]
                ny = 0 + WIDTH * DY[j]
                self.safe_nodes[index(nx, ny)] = False

        for x in np.arange(0, Const.ARENA_GRID_COUNT, WIDTH):
            for y in np.arange(0, Const.ARENA_GRID_COUNT, WIDTH):
                for i in range(8):
                    nx = x + WIDTH * DX[i]
                    ny = y + WIDTH * DY[i]
                    if in_graph(nx, ny) and self.safe_nodes[index(nx, ny)]:
                        self.edges[index(x, y)].append((index(nx, ny), DW[i], i))
    



