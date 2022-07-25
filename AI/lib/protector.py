import pygame as pg
from AI.lib.brain import Brain
from AI.lib.utils import *
from AI.lib.Const import *

class Protector():
    def __init__(self, brain:Brain):
        self.brain = brain
    

    def hitCheck(self, position: pg.Vector2):
        """
        Check if a bullet's position will hit self.
        """
        return (position - self.brain.position).length() <= Const.PLAYER_RADIUS
    

    def FutureCheck(self, ticks: int = 1):
        """
        Check all bullets and react.
        """
        bullets = self.brain.helper.get_bullet_info()
        for tick in range(ticks):
            for bullet in bullets:
                if bullet['lifespan'] < 0:
                    continue
                bullet['lifespan'] -= 1
                bullet['position'] += bullet['speed']
                if self.hitCheck(bullet['position']):
                    if not self.brain.KickCheck(bullet['speed'], bullet['repulsion']) and self.brain.ShootCheck():
                        self.brain.action['attack'] = True
                    return


    def Decide(self):
        self.FutureCheck(10)