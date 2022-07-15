import pygame as pg
import Const
from EventManager.EventManager import *
from Model.Model import GameEngine

class Audio():

    def __init__(self, ev_manager: EventManager, model: GameEngine, q_mode: bool):
        self.ev_manager = ev_manager
        self.model = model
        ev_manager.register_listener(self)

        self.q_mode = q_mode

        if not self.q_mode:
            pg.mixer.init()

            self.menu_music = pg.mixer.Sound(Const.MENU_MUSIC_PATH)
            self.background_music = pg.mixer.Sound(Const.BACKGROUND_MUSIC_PATH)
            self.normal_gun_sound = pg.mixer.Sound(Const.NORMAL_GUN_SOUND_PATH)
            self.sniper_sound = pg.mixer.Sound(Const.SNIPER_SOUND_PATH)
            self.shotgun_sound = pg.mixer.Sound(Const.SHOT_GUN_SOUND_PATH)
            self.machine_gun_sound = pg.mixer.Sound(Const.MACHINE_GUN_SOUND_PATH)
            self.player_died_sound = pg.mixer.Sound(Const.PLAYER_DIED_SOUND_PATH)
            self.player_killed_sound = pg.mixer.Sound(Const.PLAYER_KILLED_SOUND_PATH)
            self.player_get_hit_sound = pg.mixer.Sound(Const.PLAYER_HIT_SOUND_PATH)
            self.player_hit_wall_sound = pg.mixer.Sound(Const.PLAYER_HIT_WALL_SOUND_PATH)
            self.player_pick_up_item_sound = pg.mixer.Sound(Const.PLAYER_PICKUP_ITEM_SOUND_PATH)
            self.player_switch_gun_sound = pg.mixer.Sound(Const.PLAYER_SWITCH_GUN_SOUND_PATH)

            self.menu_music.set_volume(0.5)
            self.background_music.set_volume(1)
            self.normal_gun_sound.set_volume(0.2)
            self.sniper_sound.set_volume(0.2)
            self.shotgun_sound.set_volume(0.1)
            self.machine_gun_sound.set_volume(0.2)
            self.player_died_sound.set_volume(0.8)
            self.player_killed_sound.set_volume(0.5)
            self.player_pick_up_item_sound.set_volume(0.4)
            self.player_get_hit_sound.set_volume(0.7)
            self.player_hit_wall_sound.set_volume(0.2)
            self.player_switch_gun_sound.set_volume(0.7)

    
    def notify(self, event):
        if self.q_mode:
            return

        if isinstance(event, EventPlayerAttackSuccess):
            if event.gun_type == Const.GUN_TYPE_NORMAL_GUN:
                self.normal_gun_sound.play()
            elif event.gun_type == Const.GUN_TYPE_MACHINE_GUN:
                self.machine_gun_sound.play()
            elif event.gun_type == Const.GUN_TYPE_SHOTGUN:
                self.shotgun_sound.play()
            elif event.gun_type == Const.GUN_TYPE_SNIPER:
                self.sniper_sound.play()
        
        elif isinstance(event, EventPlayerBuffed):
            self.player_pick_up_item_sound.play()

        elif isinstance(event, EventPlayerSwitchGun):
            self.player_switch_gun_sound.play()
        
        elif isinstance(event, EventPlayerDead):
            self.player_died_sound.play()

        elif isinstance(event, EventPlayerRemove):
            self.player_killed_sound.play()

        elif isinstance(event, EventPlayerGetHit):
            self.player_get_hit_sound.play()

        elif isinstance(event, EventPlayerHitWall):
            self.player_hit_wall_sound.play()
        
        elif isinstance(event, EventInitialize):
            self.menu_music.play(-1)
        
        elif isinstance(event, EventStop):
            pg.mixer.pause()
                
        elif isinstance(event, EventContinue):
            pg.mixer.unpause()

        elif isinstance(event, EventStateChange):
            if event.state in {Const.STATE_MENU, Const.STATE_ENDGAME} and self.menu_music.get_num_channels() == 0:
                self.background_music.stop()
                self.menu_music.play(-1)

            elif event.state in {Const.STATE_PLAY} and self.background_music.get_num_channels() == 0:
                self.menu_music.stop()
                self.background_music.play(-1)
        
        elif isinstance(event, EventTimesUp):
            self.background_music.stop()
            self.menu_music.play(-1)
        
