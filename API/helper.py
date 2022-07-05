import pygame as pg
from Model.Model import *
import Const

class Helper(object):
    def __init__(self, model: GameEngine, index):
        self.model = model
        self.player_id = index

    # get game data
    def get_game_remaining_time(self):
        return self.model.timer

    # general
    def get_self_id(self):
        return self.player_id

    def get_player_id(self):
        return [player.player_id for player in self.model.players]

    def get_player_life(self):
        return [player.respawn_count for player in self.model.players]

    def get_player_score(self):
        return [player.score for player in self.model.players]

    def get_player_respawn_time(self):
        """
        If the player is respawning, return how many remaining time for
        that player need to respawn
        """
        return [player.respawn_timer for player in self.model.players if player.respawning()]

    # movement
    def get_player_position(self):
        return [player.position for player in self.model.players]

    def get_player_direction(self):
        return [player.direction for player in self.model.players]

    # attack
    def get_player_kick(self):
        pass

    def get_player_repulsion(self):
        pass

    def get_player_attack_cd(self):
        pass

    def get_player_next_attack(self):
        pass

    def get_players_attack_range(self):
        pass

    def get_player_attack_accuracy(self):
        pass

    def get_player_aux_length(self):
        pass

    def get_player_gun_type(self):
        pass

    def get_player_gun_remaining_time(self):
        pass

    def get_bullet_info(self):
        pass


    # get item data
    def get_item_info(self):
        pass

    # get field data
    def get_wall_position(self):
        pass

    def get_RE_field_position(self):
        pass
