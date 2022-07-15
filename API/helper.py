import pygame as pg
import Const
from Model.GameObject.bullet import *
from Model.GameObject.item import *
from Model.GameObject.obstacle import *

class Helper(object):
    def __init__(self, model, index):
        self.model = model
        self.player_id = index

    # get game data
    def get_game_time(self) -> int:
        """return game time, use 1 frame as unit"""
        return Const.GAME_LENGTH - self.model.timer

    def get_game_remaining_time(self) -> int:
        """return game remaining time, use 1 frame as unit"""
        return self.model.timer

    # get self data
    # general
    def get_self_id(self) -> int:
        """return your id"""
        return self.player_id

    def get_self_respawn_count(self) -> int:
        """return a int as your remaining respawn count."""
        return self.model.players[self.player_id].respawn_count

    def get_self_score(self) -> int:
        """return a int as your score."""
        return self.model.players[self.player_id].score

    def get_self_respawn_time(self) -> int:
        """return a int as your remaining respawn time."""
        return self.model.players[self.player_id].respawn_timer

    def get_self_is_respawning(self) -> bool:
        """return a bool representing whether you are respawning or not."""
        return self.model.players[self.player_id].respawning()

    def get_self_position(self) -> pg.Vector2:
        """return a Vector2 as your position."""
        return self.model.players[self.player_id].position.copy()

    def get_self_direction(self) -> pg.Vector2:
        """return a Vector2 as your direction."""
        return self.model.players[self.player_id].direction.copy()

    # movement
    def get_self_speed(self) -> pg.Vector2:
        """return a Vector2 as your speed."""
        return self.model.players[self.player_id].speed.copy()

    def get_self_rotation_speed(self) -> int:
        """
        return a int as your rotation speed, 
        use radian per frame as unit.
        """
        return Const.PLAYER_ROTATION_SPEED

    def get_self_base_speed(self) -> int:
        """return a int as your base speed value."""
        return self.model.players[self.player_id].base_speed

    # attack
    def get_self_kick(self) -> float:
        """return a float as your kick."""
        return self.model.players[self.player_id].attack_kick \
            * self.model.players[self.player_id].gun.attack_kick_multiplier \
            * 10

    def get_self_repulsion(self) -> float:
        """return a float as your repulsion."""
        return self.model.players[self.player_id].bullet_repulsion \
            * self.model.players[self.player_id].gun.bullet_repulsion_multiplier \
            * 10

    def get_self_attack_cd(self) -> int:
        """return a int as your attack cd, use frame as unit."""
        return round( \
            1 / (self.model.players[self.player_id].attack_speed \
            * self.model.players[self.player_id].gun.attack_speed_multiplier) \
            * Const.FPS)

    def get_self_next_attack(self) -> int:
        """
        return a int as the remaining time until your next attack, 
        use frame as unit.
        """
        return self.model.players[self.player_id].gun.cd_time

    def get_self_attack_speed(self) -> float:
        """
        return a float as your attack speed in shots per second.
        """
        return self.model.players[self.player_id].attack_speed * \
            self.model.players[self.player_id].gun.attack_speed_multiplier

    def get_self_attack_range(self) -> float:
        """return a float as your attack range"""
        return self.model.players[self.player_id].bullet_lifespan \
            * self.model.players[self.player_id].gun.bullet_lifespan_multiplier \
            * Const.BULLET_SPEED

    def get_self_attack_accuracy(self) -> float:
        """return a float as your attack accuracy in radian"""
        return self.model.players[self.player_id].attack_accuracy \
            * self.model.players[self.player_id].gun.bullet_accuracy_multiplier

    def get_self_basic_attack_speed(self) -> float:
        """
        return a float as your attack speed 
        without multiplier in shot per second
        """
        return self.model.players[self.player_id].attack_speed

    def get_self_basic_attack_range(self) -> float:
        """return a float as your attack range without multiplier"""
        return self.model.players[self.player_id].bullet_lifespan \
            * Const.BULLET_SPEED

    def get_self_basic_attack_accuracy(self) -> float:
        """
        return a float as your attack accuracy 
        without multiplier in radian
        """
        return self.model.players[self.player_id].attack_accuracy

    def get_self_gun_type(self) -> int:
        """
        return a int as your gun type, 0 as normal gun, 
        1 as machine gun, 2 as sniper, 3 as shot gun
        """
        return self.model.players[self.player_id].gun.type

    def get_self_gun_remaining_time(self) -> int:
        """return a int as your remaining gun using time in frame"""
        return self.model.players[self.player_id].gun.use_time

    # buff
    def get_self_buff_count(self) -> dict:
        """return the amount of buffs on you."""
        player = self.model.players[self.player_id]
        return [
            {
                "type": Const.BUFF_TYPE_ATTACK_SPEED,
                "count": Const.PLAYER_QUOTA_ATTACK_SPEED - player.quota_attack_speed
            }, {
                "type": Const.BUFF_TYPE_REPULSION,
                "count": Const.PLAYER_QUOTA_REPULSION - player.quota_repulsion
            }, {
                "type": Const.BUFF_TYPE_ATTACK_ACCURACY,
                "count": Const.PLAYER_QUOTA_ATTACK_ACCURACY - player.quota_attack_accuracy
            }
        ]

    def get_self_specific_buff_count(self, buff_type: int) -> int:
        """return the amount of specific buff on you."""
        for buff_info in self.get_self_buff_count():
            if buff_info["type"] == buff_type:
                return buff_info["count"]

    # get all player data
    # general
    def get_player_id(self) -> list:
        """return all player's id, use id as index."""
        return [player.player_id for player in self.model.players]

    def get_player_respawn_count(self) -> list:
        """return all player's remaining respawn count, 
        use id as index.
        """
        return [player.respawn_count for player in self.model.players]

    def get_player_score(self) -> list:
        """return all player's score, use id as index."""
        return [player.score for player in self.model.players]

    def get_player_respawn_time(self) -> list:
        """return all player's remaining respawn time, 
        use id as index, 1 frame as unit.
        """
        return [player.respawn_timer for player in self.model.players]

    def get_player_is_respawning(self) -> list:
        """
        return a bool list represent all player is respawning or not, 
        use id as index
        """
        return [player.respawning() for player in self.model.players]

    def get_player_is_alive(self) -> list:
        """
        return a bool list represent all player is killed or not,
        use id as index
        """
        return [player.killed() for player in self.model.players]

    # movement
    def get_player_position(self) -> list:
        """return Vector2 list represent all player's position, use id as index"""
        return [player.position.copy() for player in self.model.players]

    def get_player_direction(self) -> list:
        """return Vector2 list represent all player's direction, use id as index"""
        return [player.direction.copy() for player in self.model.players]

    def get_player_speed(self) -> list:
        """
        return a Vector2 list represent all player's speed,
        use id as index.
        """
        return [player.speed.copy() for player in self.model.players]

    def get_player_base_speed(self) -> list:
        """
        return a float list represent all player's base speed,
        use id as index
        """
        return [player.base_speed for player in self.model.players]

    def get_player_rotation_speed(self) -> list:
        """
        return a float list represent all player's rotation speed,
        use id as index, radian as unit.
        """
        return [Const.PLAYER_ROTATION_SPEED for player in self.model.players]

    # attack
    def get_player_kick(self) -> list:
        """return all player's kick, id as index, grid as unit."""
        return [player.attack_kick * player.gun.attack_kick_multiplier * 10 \
                for player in self.model.players]

    def get_player_repulsion(self) -> list:
        """return all player's repulsion, 
        id as index, grid as unit.
        """
        return [player.bullet_repulsion * player.gun.bullet_repulsion_multiplier * 10 \
                for player in self.model.players]

    def get_player_attack_cd(self) -> list:
        """return all player's attack cd, id as index,
        1 frame as unit
        """
        return [round( \
            1 / (player.attack_speed \
            * player.gun.attack_speed_multiplier) * Const.FPS) \
            for player in self.model.players]

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

    def get_player_gun_type(self) -> list:
        """return all player's gun type, id as index,
        return 0 as normal gun, 1 as machine gun,
        2 as sniper, 3 as shot gun
        """
        return [player.gun.type for player in self.model.players]

    def get_player_gun_remaining_time(self) -> list:
        return [player.gun.use_time for player in self.model.players]

    # get specific player data
    def get_nearest_player_position(self) -> pg.Vector2:
        """
        return the position of the nearest player
        """
        players_pos = self.get_player_position()
        self_pos = players_pos.pop(self.get_self_id())
        nearest_pos = players_pos[0]
        for pos in players_pos:
            if (pos - self_pos).length() < (nearest_pos - self_pos).length():
                nearest_pos = pos
        return nearest_pos

    def get_nearest_player_id(self) -> int:
        """
        return the id of the nearest player
        """
        players_pos = self.get_player_position()
        self_pos = players_pos[self.get_self_id()]
        nearest_id = (self.get_self_id() + 1) % Const.PLAYER_NUMBER
        for i in range(Const.PLAYER_NUMBER):
            if i == self.get_self_id():
                continue
            if (players_pos[i] - self_pos).length() \
                < (players_pos[nearest_id] - self_pos).length():
                nearest_id = i
        return nearest_id

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

    def get_bullet_info(self) -> list:
        """get the information of the bullet."""
        return [
            {
                "speed": bullet.speed.copy(), "position": bullet.position.copy(),
                "repulsion": bullet.repulsion, "lifespam": bullet.lifespam,
                "attacker": bullet.attacker.player_id
            }
            for bullet in self.model.bullets if isinstance(bullet, Bullet)
        ]

    # get item data
    def get_item_info(self) -> list:
        """get the position and type of the items."""
        return [
            {
                "position": item.position.copy(), "type": item.type
            }
            for item in self.model.items
        ]

    def get_specific_item_info(self, item_type: int) -> list:
        """get the position and type of specific items."""
        return [item_info for item_info in self.get_item_info() \
                if item_info["type"] == item_type]

    def get_nearest_item_info(self) -> list:
        """
        get nearest RE or boundary position
        """
        items_info = self.get_item_info()
        self_pos = self.get_player_position()[self.player_id]
        nearest_info = items_info[0]
        for info in items_info:
            if (nearest_info['position'] - self_pos).length() \
                    >= (info['position'] - self_pos).length():
                nearest_info = info
        return nearest_info

    # get field data
    def get_wall_position(self) -> list:
        """return all obstacles"""
        return [wall.position.copy() for wall in self.model.obstacles]

    def get_RE_field_position(self) -> list:
        """return RE_Field obstacles"""
        return [RE_field.position.copy() for RE_field in self.model.obstacles \
                if isinstance(RE_field,RE_Field)]

    def get_nearest_RE_position(self) -> pg.Vector2:
        """
        get nearest RE or boundary position
        """
        REs_pos = self.get_RE_field_position()
        self_pos = self.get_player_position()[self.get_self_id()]
        REs_pos += [Vector2(self_pos.x, 0), Vector2(self_pos.x, 30), \
            Vector2(0, self_pos.y), Vector2(30, self_pos.y)]
        nearest_pos = REs_pos[0]
        for pos in REs_pos:
            if (nearest_pos - self_pos).length() >= (pos - self_pos).length():
                nearest_pos = pos
        return nearest_pos
