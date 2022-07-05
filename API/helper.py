import pygame as pg
import Const

class Helper(object):
    def __init__(self, model, index):
        self.model = model
        self.player_id = index

    # get game data
    def get_game_remaining_time(self) -> int:
        '''return game remaining time'''
        return self.model.timer // Const.FPS

    # general
    def get_self_id(self) -> int:
        '''return your id '''
        return self.player_id

    def get_player_id(self) -> list:
        """return all player's id, use id as index"""
        return [player.player_id for player in self.model.players]

    def get_player_respawn_count(self) -> list:
        """return all player's remaining respawn count, use id as index"""
        return [player.respawn_count for player in self.model.players]

    def get_player_score(self) -> list:
        """return all player's score, use id as index"""
        return [player.score for player in self.model.players]

    def get_player_respawn_time(self) -> list:
        """return all player's remaining respawn time, use id as index"""
        return [player.respawn_timer // Const.FPS for player in self.model.players]

    # movement
    def get_player_position(self) -> list:
        """return all player's position, use id as index"""
        return [player.position for player in self.model.players]

    def get_player_direction(self) -> list:
        """return all player's direction, use id as index"""
        return [player.direction for player in self.model.players]

    # attack
    def get_player_kick(self):
        pass

    def get_player_repulsion(self):
        pass

    def get_player_attack_cd(self):
        pass

    def get_player_next_attack(self) -> list:
        """return the remaining time until every player's next attack in frames, use id as index."""
        return [player.gun.cd_time for player in self.model.players]
    
    def get_player_attack_speed(self) -> list:
        """return the attack speed of every play in shots per second, use id as index."""
        return [player.attack_speed * player.gun.attack_speed_multiplier for player in self.model.players]

    def get_player_attack_range(self) -> list:
        """return the attack range of every player in grids, use id as index."""
        return [player.bullet_lifespan * player.gun.bullet_lifespan_multiplier * Const.BULLET_SPEED for player in self.model.players]

    def get_player_attack_accuracy(self) -> list:
        """return the attack accuracy of every player in radian, use id as index."""
        return [player.attack_accuracy * player.gun.bullet_accuracy_multiplier for player in self.model.players]

    def get_player_basic_attack_speed(self) -> list:
        """return the basic attack speed without multiplier from gun of every play in shots per second, use id as index."""
        return [player.attack_speed for player in self.model.players]

    def get_player_basic_attack_range(self) -> list:
        """return the basic attack range without multiplier from gun of every player in grids, use id as index."""
        return [player.bullet_lifespan * Const.BULLET_SPEED for player in self.model.players]

    def get_player_basic_attack_accuracy(self) -> list:
        """return the basic attack accuracy without multiplier from gun of every player in radian, use id as index."""
        return [player.attack_accuracy for player in self.model.players]

    def get_player_gun_type(self):
        pass

    def get_player_gun_remaining_time(self):
        pass

    def get_bullet_info(self):
        pass

    # get buff info
    def get_player_buff_count(self) -> list:
        """return the amount of buffs on every player."""
        return [
            [{
                "type": Const.BUFF_TYPE_ATTACK_SPEED,
                "count": Const.PLAYER_QUOTA_ATTACK_SPEED - player.quota_attack_speed
            }, {
                "type": Const.BUFF_TYPE_REPULSION,
                "count": Const.PLAYER_QUOTA_REPULSION - player.quota_repulsion
            }, {
                "type": Const.BUFF_TYPE_ATTACK_ACCURACY,
                "count": Const.PLAYER_QUOTA_ATTACK_ACCURACY - player.quota_attack_accuracy
            }
            ] for player in self.model.players
        ]

    def get_player_specific_buff_count(self, buff_type: int) -> list:
        """return the amount of specific buff on every player."""
        ret = []
        for buff_dict in self.get_player_buff_count():
            for buff_info in buff_dict:
                if buff_info["type"] == buff_type:
                    ret.append(buff_info["count"])
        return ret 
    
    def get_specific_player_buff_count(self, player_id: int) -> list:
        """return the amount of buffs on specific player."""
        if player_id not in range(Const.PLAYER_NUMBER):
            return []
        else:
            return self.get_player_buff_count()[player_id]

    # get item data
    def get_item_info(self):
        pass

    # get field data
    def get_wall_position(self):
        pass

    def get_RE_field_position(self):
        pass
