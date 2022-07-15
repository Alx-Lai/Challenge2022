import pygame as pg
import heapq as hq
import math 

import Const
from AI.lib.brain import Brain
from AI.lib.utils import *

class Navigator():
    def __init__(self, brain: Brain):
        self.brain = brain

    def dijkstra(self, start: int):
        """
        Run Dijkstra's Algorithm and return two lists ([distance], [pre_index]).
        """
        dis = [math.inf] * (LENGTH ** 2)
        pre = [-1] * (LENGTH ** 2)
        dis[start] = 0
        heap = []
        for (x, w, d) in self.brain.edges[start]:
            hq.heappush(heap, (w, x, d))
        
        while heap:
            distance, node, direction = hq.heappop(heap)
            if dis[node] < math.inf:
                continue
            dis[node] = distance
            pre[node] = direction
            for (x, w, d) in self.brain.edges[node]:
                if dis[x] == math.inf:
                    hq.heappush(heap, (distance + w, x, d))
        return dis, pre
    
    def destination(self) -> pg.Vector2:
        """
        Return a Vector2 representing the best destination to go to, return (-1,-1) if it decides to stay.
        """
        items = self.brain.helper.get_item_info()
        dis, pre = self.dijkstra(index(self.brain.position))


        # if have special gun, neglect gun items
        tmp_items = items
        if self.brain.helper.get_self_gun_type() != Const.GUN_TYPE_NORMAL_GUN:
            items = [item for item in items if item["type"] >= 4]

        # no choice
        if not items:
            items = tmp_items

        # find closet item
        best_item = items[0]
        for item in items[1:]:
            if dis[index(best_item["position"])] > dis[index(item["position"])]:
                best_item = item
        
        # find turning point
        x, y = normalize(best_item["position"])
        dest = pg.Vector2(x, y)
        mem = pre[index(x, y)]
        while pre[index(x, y)] != -1:
            tmp = pre[index(x, y)]
            if mem != tmp:
                dest = pg.Vector2(x, y)
                mem = tmp
            x -= DX[tmp] * WIDTH
            y -= DY[tmp] * WIDTH
        return dest

    def decide(self):
        """
        Main function of Navigator, will modify action to decide movement.
        """
        if self.brain.time % DIJKSTRA_FREQUENCY == 0:
            self.dest = self.destination()

        rotate_radian = angleBetween(self.brain.direction, self.dest - self.brain.position) # radian
        if abs(rotate_radian) > MOVING_ROTATIONAL_TOLERANCE:
            if rotate_radian < 0:
                self.brain.action['left'] = True
            else:
                self.brain.action['right'] = True
            return
        else:
            self.brain.action['forward'] = True