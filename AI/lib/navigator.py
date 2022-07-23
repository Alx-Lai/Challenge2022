import pygame as pg

import Const
from AI.lib.brain import Brain
from AI.lib.utils import *

class Navigator():
    def __init__(self, brain: Brain):
        self.brain = brain
    

    def CheckTarget(self, target: pg.Vector2) -> None:
        """
        Check if the target location is safe to approach and change to a nearby location if not. 
        """
        if self.brain.isWalkable[Index(target)]:
            return 
        distance = 0
        while distance <= MAX_ALT_DISTANCE:
            distance += WIDTH
            for i in range(8):
                pos = target + DXY[i] * distance
                if self.brain.isWalkable[Index(pos)]:
                    target = pos
                    return 
        # print(target, " Failed to get safe location.")
        target = self.brain.position


    def Simplify(self, target: pg.Vector2) -> pg.Vector2:
        """
        Return a Vector2 representing the first turning corner. 
        """
        self.CheckTarget(target)
        pos = Normalize(target)
        dest = pos.copy()
        mem = self.brain.dijkstraPrevious[Index(pos)]
        while self.brain.dijkstraPrevious[Index(pos)] != -1:
            tmp = self.brain.dijkstraPrevious[Index(pos)]
            if mem != tmp:
                dest = pos.copy()
                mem = tmp
            pos -= DXY[tmp] * WIDTH
        return dest
    

    def BoostCheck(self):
        minAngle = min(AngleBetween(vec, self.brain.direction) for vec in DXY[:4])
        if minAngle < BOOST_CHECK_ANGLE_TOLERANCE:
            # if parallel to horizontal or verical line, consider reflective shot
            return self.brain.ShootCheck(1 * BOOST_CHECK_MULTIPLIER)
        else:
            return self.brain.ShootCheck(1)


    def Decide(self, target: pg.Vector2):
        """
        Main function of Navigator, will modify action to decide movement.
        """
        target = self.Simplify(target)
        rotateRadian = AngleBetween(-self.brain.direction, target - self.brain.position) # radian
        if abs(rotateRadian) > MOVING_ROTATIONAL_TOLERANCE:
            if rotateRadian < 0:
                self.brain.action['left'] = True
            else:
                self.brain.action['right'] = True
            return
        else:
            if (target - self.brain.position).length() >= self.brain.helper.get_self_kick() and self.BoostCheck():
                self.brain.action['attack'] = True
            self.brain.action['backward'] = True