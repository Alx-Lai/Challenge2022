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

    def get_player_next_attack(self) -> list:
        """return the remaining time (frames) until every player's next attck, use id as index"""
        return [player.gun.cd_time for player in self.model.players]

    def get_player_attack_range(self) -> list:
        """return the attack range of every player, use id as index"""
        return [player.bullet_trace_time * player.gun.bullet_trace_time_multiplier for player in self.model.players]

    def get_player_attack_accuracy(self):
        pass

    def get_player_aux_length(self) -> list:
        """return the auxiliary line length of every player, use id as index"""
        return [player.aux_line_length for player in self.model.players]

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
