import Const
import random
from Model.GameObject.bullet import *
from Model.GameObject.item import *
from pygame.math import Vector2

class Item_Generator:
    def __init__(self, model):
        self.model = model
        self.generate_cd = 0
        while len(self.model.items) < Const.ITEM_MAX:
            self.generate()

    def generate(self):
        while True:
            generated_item = None
            if random.randint(1, 2) == 1:
                px = random.random() * (Const.ARENA_GRID_COUNT - 2 * Const.ITEM_BUFF_RADIUS) + Const.ITEM_BUFF_RADIUS
                py = random.random() * (Const.ARENA_GRID_COUNT - 2 * Const.ITEM_BUFF_RADIUS) + Const.ITEM_BUFF_RADIUS
                generated_item = Item_Buff(self.model, Vector2(px, py), random.randint(1, 3))
            else:
                px = random.random() * (Const.ARENA_GRID_COUNT - 2 * Const.ITEM_GUN_RADIUS) + Const.ITEM_GUN_RADIUS
                py = random.random() * (Const.ARENA_GRID_COUNT - 2 * Const.ITEM_GUN_RADIUS) + Const.ITEM_GUN_RADIUS
                generated_item = Item_Gun(self.model, Vector2(px, py), random.randint(1, 3))

            collided = False
            for bullet in self.model.bullets:
                if isinstance(bullet, Bullet) and bullet.trace_collide_object(generated_item):
                    collided = True
                    break
            for obstacle in self.model.obstacles:
                if generated_item.collide_object(obstacle):
                    collided = True
                    break
            for item in self.model.items:
                if generated_item.collide_object(item):
                    collided = True
                    break
            for player in self.model.players:
                if generated_item.collide_object(player):
                    collided = True
                    break
            if not collided:
                self.model.items.append(generated_item)
                return

    def tick(self):
        self.generate_cd -= 1
        if self.generate_cd <= 0:
            while len(self.model.items) < Const.ITEM_MAX:
                self.generate()
                self.generate_cd = Const.ITEM_GENERATOR_COOLDOWN
                break