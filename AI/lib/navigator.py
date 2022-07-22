import pygame as pg
import heapq as hq
import math 

import Const
from AI.lib.brain import Brain
from AI.lib.utils import *

class Navigator():
    def __init__(self, brain: Brain):
        self.brain = brain
        self.lastDijkstraTime = -DIJKSTRA_FREQUENCY
        self.target = pg.Vector2(0, 0)

    def Dijkstra(self, start: int):
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
    
    def Destination(self) -> pg.Vector2:
        """
        Return a Vector2 representing the best destination to go to, return (-1,-1) if it decides to stay.
        """
        items = self.brain.helper.get_item_info()
        dis, pre = self.Dijkstra(Index(self.brain.position))

        # if have special gun, neglect gun items
        tmpItems = items
        if self.brain.helper.get_self_gun_type() != Const.GUN_TYPE_NORMAL_GUN:
            items = [item for item in items if item["type"] >= 4]

        # no choice
        if not items:
            items = tmpItems

        # find closet item
        bestItem = items[0]
        for item in items[1:]:
            if dis[Index(bestItem["position"])] > dis[Index(item["position"])]:
                bestItem = item
        
        # find turning point
        pos = Normalize(bestItem["position"])
        dest = pos.copy()
        mem = pre[Index(pos)]
        while pre[Index(pos)] != -1:
            tmp = pre[Index(pos)]
            if mem != tmp:
                dest = pos.copy()
                mem = tmp
            pos -= DXY[tmp] * WIDTH
        return dest
    
    def BoostCheck(self):
        minAngle = min(AngleBetween(vec, self.brain.direction) for vec in DXY[:4])
        if minAngle < BOOST_CHECK_ANGLE_TOLERANCE:
            # if parallel to horizontal or verical line, consider reflective shot
            return self.brain.ShootCheck(4)
        else:
            return self.brain.ShootCheck(1)


    def Decide(self):
        """
        Main function of Navigator, will modify action to decide movement.
        """
        if self.brain.time - self.lastDijkstraTime >= DIJKSTRA_FREQUENCY:
            self.dest = self.Destination()

        self.brain.mode = Mode.IDLE
        rotateRadian = AngleBetween(-self.brain.direction, self.dest - self.brain.position) # radian
        if abs(rotateRadian) > MOVING_ROTATIONAL_TOLERANCE:
            if rotateRadian < 0:
                self.brain.action['left'] = True
            else:
                self.brain.action['right'] = True
            return
        else:
            if (self.dest - self.brain.position).length() >= self.brain.helper.get_self_kick() and self.BoostCheck():
                self.brain.action['attack'] = True
            self.brain.action['backward'] = True