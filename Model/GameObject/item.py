import Const
from Model.GameObject.base_game_object import *

class Item_Gun(Base_Square_Object):
    '''
    Pickable gun item.
    '''
    def __init__(self, model, position, gun_type):
        super().__init__(model, position, Const.ITEM_GUN_RADIUS)
        self.type = gun_type

    def tick(self):
        '''
        Run whenever EventEveryTick() arises.
        '''
        for player in self.model.players:
            if not player.invisible() and self.collide_object(player):
                player.switch_gun(self.type)
                self.kill()
                return


class Item_Buff(Base_Square_Object):
    '''
    Pickable buff item.
    '''
    def __init__(self, model, position, buff_type):
        super().__init__(model, position, Const.ITEM_BUFF_RADIUS)
        self.type = buff_type

    def tick(self):
        '''
        Run whenever EventEveryTick() arises.
        '''
        for player in self.model.players:
            if not player.respawning() and self.collide_object(player) and player.quota_enough(self.type):
                player.buff(self.type)
                self.kill()
                return