import Const
from Model.GameObject.base_game_object import *

class Item_Gun(Base_Square_Object):
    def __init__(self, model, position, gun_type):
        super().__init__(model, position, Const.ITEM_RADIUS)
        self.type = gun_type

    def tick(self):
        '''
        Run whenever EventEveryTick() arises.
        '''
        for player in self.model.players:
            if self.collide_object(player):
                player.switch_gun(self.type)
                self.kill()
                return