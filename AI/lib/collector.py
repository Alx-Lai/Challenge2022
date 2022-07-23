import pygame as pg
import math

import Const
from AI.lib.brain import Brain
from AI.lib.navigator import Navigator
from AI.lib.utils import *

class Collector():
    def __init__(self, brain: Brain, navigator: Navigator):
        self.brain = brain
        self.navigator = navigator
        self.target = None # type = item
        self.lastScanTime = -ITEM_SCAN_FREQUENCY


    def Scoring(self, item) -> float:
        """
        Calculate the score of a specific item, considering position, time, type, etc.
        """
        if not self.brain.isWalkable[Index(item["position"])]:
            return -math.inf
        score = -(self.brain.dijkstraDistance[Index(item["position"])]) / (MAX_DISTANCE)
        if item["type"] <= 3: # gun
            if self.brain.helper.get_self_gun_type == Const.GUN_TYPE_NORMAL_GUN:
                score += -(self.brain.time) / (Const.GAME_LENGTH * 2)
        else: # buff
            score += (self.brain.time) / (Const.GAME_LENGTH * 2)
        return score
        

    def ScanItem(self) -> None:
        """
        Scan all items and setup a best target.
        """
        self.lastScanTime = self.brain.time
        items = self.brain.helper.get_item_info()
        if not items:
            self.target = None
            return 

        self.target = items[0]
        for item in items[1:]:
            if self.Scoring(self.target) < self.Scoring(item):
                self.target = item


    def CheckTarget(self) -> bool:
        """
        Check if the target item is still available. 
        """
        if not self.target in self.brain.helper.get_item_info():
            self.target = None
        return self.target != None


    def Decide(self):
        """
        Main function of collector, will find a item target and control via navigator.
        """
        if self.target == None or self.brain.time - self.lastScanTime >= ITEM_SCAN_FREQUENCY:
            self.ScanItem()
        if not self.CheckTarget():
            self.brain.mode = Mode.IDLE
            return False

        self.brain.mode = Mode.COLLECT
        self.navigator.Decide(self.target["position"])