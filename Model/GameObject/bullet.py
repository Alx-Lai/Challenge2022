import Const
import pygame as pg
from Model.GameObject.base_game_object import *

class Bullet(Base_Game_Object):
    def __init__(self, model, player, length, repulsion):
        position = player.position + player.direction * (Const.PLAYER_RADIUS * 2)
        super().__init__(model, position, Const.BULLET_RADIUS, True, True)

        self.attacker = player
        self.speed = player.direction * Const.BULLET_SPEED
        self.length = length
        self.repulsion = repulsion

        self.lifespam = Const.BULLET_LIFESPAM

        self.__death = False

    def tick(self):
        super().tick()

        if self.lifespam <= 0:
            self.kill()
        for player in self.model.players:
            if self.collide_object(player):
                player.knock_back(self.repulsion, self.speed.normalize())
                if player.player_id != self.attacker.player_id:
                    self.attacker.score += Const.BULLET_HIT_SCORE
                self.kill()

    def kill(self):
        self.__death = True

    def killed(self):
        return self.__death