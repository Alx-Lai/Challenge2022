import pygame as pg
import Const

class Helper(object):
    def __init__(self, model, index):
        self.model = model
        self.player_id = index

    # get game data
    def get_game_remaining_time(self):
        pass

    # general
    def get_self_id(self):
        pass

    def get_player_id(self):
        pass

    def get_player_life(self):
        pass

    def get_player_score(self):
        pass

    def get_player_respawn_time(self):
        pass

    # movement
    def get_player_position(self):
        pass

    def get_player_direction(self):
        pass

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
