import pygame as pg
import numpy as np
import heapq as hq
import math 
import Const
from AI.lib.brain import Brain
from AI.lib.utils import *

SCALE = 2
WIDTH = 1 / SCALE
LEN = int(Const.ARENA_GRID_COUNT * SCALE)

dx = [0, 1, 0, -1, 1, 1, -1, -1] # D, R, U, L, DR, UR, UL, DL
dy = [1, 0, -1, 0, 1, -1, -1, 1]
dw = [1] * 4 + [math.sqrt(2)] * 4

ROTATE_TOLERANCE = 0.03 # radian
DIJKSTRA_FREQUENCY = 3 # frames per evaluate

class Navigator():
    def __init__(self, brain: Brain):
        self.brain = brain

        self.edges = [[] for i in range(LEN ** 2)] # tuple(node, weight, direc), node indexed by index()
        self.safe_nodes = [True] * (LEN ** 2)
        self.init_graph()

    def in_graph(self, x, y) -> bool:
        return 0 < min(x, y) and max(x, y) < Const.ARENA_GRID_COUNT

    def init_graph(self):
        for pos in self.brain.RE_fields:
            self.safe_nodes[self.index(pos)] = False
            for i in range(8):
                nx = pos.x + WIDTH * dx[i]
                ny = pos.y + WIDTH * dy[i]
                self.safe_nodes[self.index(nx, ny)] = False
                for j in range(4):
                    nnx = nx + WIDTH * dx[j]
                    nny = ny + WIDTH * dy[j]
                    self.safe_nodes[self.index(nnx, nny)] = False
        
        for pos in self.brain.obstacles:
            self.safe_nodes[self.index(pos)] = False
            for i in range(8):
                nx = pos.x + WIDTH * dx[i]
                ny = pos.y + WIDTH * dy[i]
                self.safe_nodes[self.index(nx, ny)] = False
        
        for i in np.arange(0, Const.ARENA_GRID_COUNT, WIDTH):
            self.safe_nodes[self.index(0, i)] = False
            for j in range(4):
                nx = 0 + WIDTH * dx[j]
                ny = i + WIDTH * dy[j]
                self.safe_nodes[self.index(nx, ny)] = False
            self.safe_nodes[self.index(i, 0)] = False
            for j in range(4):
                nx = i + WIDTH * dx[j]
                ny = 0 + WIDTH * dy[j]
                self.safe_nodes[self.index(nx, ny)] = False

        for x in np.arange(0, Const.ARENA_GRID_COUNT, WIDTH):
            for y in np.arange(0, Const.ARENA_GRID_COUNT, WIDTH):
                for i in range(8):
                    nx = x + WIDTH * dx[i]
                    ny = y + WIDTH * dy[i]
                    if self.in_graph(nx, ny) and self.safe_nodes[self.index(nx, ny)]:
                        self.edges[self.index(x, y)].append((self.index(nx, ny), dw[i], i))
    
    def normalize(self, px, py = -1):
        if py == -1:
            nx = round(px.x * SCALE) / SCALE
            ny = round(px.y * SCALE) / SCALE
        else:
            nx = round(px * SCALE) / SCALE
            ny = round(py * SCALE) / SCALE
        return (nx, ny)


    def index(self, px, py = -1):
        if py == -1:
            if not self.in_graph(px.x, px.y):
                return 0
            x = round(px.x * SCALE)
            y = round(px.y * SCALE)
        else:
            if not self.in_graph(px, py):
                return 0
            x = round(px * SCALE)
            y = round(py * SCALE)
        return y + x * LEN

    def dijkstra(self, start: int):
        """
        Run Dijkstra's Algorithm and return two lists ([distance], [pre_index]).
        """
        dis = [math.inf] * (LEN ** 2)
        pre = [-1] * (LEN ** 2)
        dis[start] = 0
        heap = []
        for (x, w, d) in self.edges[start]:
            hq.heappush(heap, (w, x, d))
        
        while heap:
            distance, node, direction = hq.heappop(heap)
            if dis[node] < math.inf:
                continue
            dis[node] = distance
            pre[node] = direction
            for (x, w, d) in self.edges[node]:
                if dis[x] == math.inf:
                    hq.heappush(heap, (distance + w, x, d))
        return dis, pre
    
    def destination(self) -> pg.Vector2:
        """
        Return a Vector2 representing the best destination to go to, return (-1,-1) if it decides to stay.
        """
        items = self.brain.helper.get_item_info()
        dis, pre = self.dijkstra(self.index(self.brain.position))


        # if have special gun, neglect gun items
        tmp_items = items
        if self.brain.helper.get_player_gun_type()[self.brain.id] != Const.GUN_TYPE_NORMAL_GUN:
            items = [item for item in items if item["type"] >= 4]

        # no choice
        if not items:
            items = tmp_items

        # find closet item
        best_item = items[0]
        for item in items[1:]:
            if dis[self.index(best_item["position"])] > dis[self.index(item["position"])]:
                best_item = item
        
        # find turning point
        x, y = self.normalize(best_item["position"])
        dest = pg.Vector2(x, y)
        mem = pre[self.index(x, y)]
        while pre[self.index(x, y)] != -1:
            tmp = pre[self.index(x, y)]
            if mem != tmp:
                dest = pg.Vector2(x, y)
                mem = tmp
            x -= dx[tmp] * WIDTH
            y -= dy[tmp] * WIDTH
        return dest

    def decide(self):
        """
        Main function of Navigator, will modify action to decide movement.
        """
        if self.brain.time % DIJKSTRA_FREQUENCY == 0:
            self.dest = self.destination()

        rotate_radian = angle_between(self.brain.direction, self.dest - self.brain.position) # radian
        if abs(rotate_radian) > ROTATE_TOLERANCE:
            if rotate_radian < 0:
                self.brain.action['left'] = True
            else:
                self.brain.action['right'] = True
            return
        else:
            self.brain.action['forward'] = True