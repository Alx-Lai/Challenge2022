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
        self.target = None
        self.lastScanTime = -ITEM_SCAN_FREQUENCY


    def Scoring(self, item) -> float:
        """
        Calculate the score of a specific item, considering position, time, type...
        """
        if not self.brain.isWalkable[Index(item["position"])]:
            return -math.inf
        score = (Const.ARENA_GRID_COUNT * math.sqrt(2) - self.brain.dijkstraDistance[Index(item["position"])]) / (Const.ARENA_GRID_COUNT * math.sqrt(2))
        if item["type"] >= 4:
            if self.brain.helper.get_self_gun_type == Const.GUN_TYPE_NORMAL_GUN:
                score += (Const.GAME_LENGTH - self.brain.time) / (Const.GAME_LENGTH * 2)
        else:
            score += (self.brain.time) / (Const.GAME_LENGTH * 2)
        return score
        

    def ScanItem(self) -> None:
        """
        Scan all items and setup a best choice. 
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


    def CheckItem(self) -> bool:
        """
        Check if target item is still available. 
        """
        return self.target != None and self.target in self.brain.helper.get_item_info()


    def Decide(self):
        """
        Main function of Navigator, will modify action to decide movement.
        """
        if self.brain.time - self.lastScanTime >= ITEM_SCAN_FREQUENCY:
            self.ScanItem()
        if not self.CheckItem():
            self.brain.mode = Mode.IDLE
            return False

        self.brain.mode = Mode.COLLECT
        self.navigator.Decide(self.target["position"])