import pygame as pg
import Const
from EventManager.EventManager import *
from Model.Model import GameEngine

class Audio():
    pg.mixer.init()
    menu_music = pg.mixer.Sound("./View/source/Everen Maxwell - Hyperphantasia [NCS Release].mp3")
    background_music = pg.mixer.Sound("./View/source/background_beta.mp3")
    normal_gun_sound = pg.mixer.Sound("./View/source/normal_gun.mp3")
    sniper_sound = pg.mixer.Sound("./View/source/sniper.mp3")
    shotgun_sound = pg.mixer.Sound("./View/source/shotgun.mp3")
    machine_gun_sound = pg.mixer.Sound("./View/source/machine_gun.mp3")
    player_died_sound = pg.mixer.Sound("./View/source/player_died.wav")
    player_killed_sound = pg.mixer.Sound("./View/source/player_killed.mp3")
    player_get_hit_sound = pg.mixer.Sound("./View/source/wall_bump.mp3")
    player_hit_wall_sound = pg.mixer.Sound("./View/source/wall_bump.mp3")
    player_pick_up_item_sound = pg.mixer.Sound("./View/source/pick_up_item.mp3")
    switch_gun_sound = pg.mixer.Sound("./View/source/switch_weapon.mp3")

    def __init__(self, ev_manager: EventManager, model: GameEngine):
            self.ev_manager = ev_manager
            self.model = model
            ev_manager.register_listener(self)

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
            self.switch_gun_sound.set_volume(0.7)

    
    def notify(self, event):
        if isinstance(event, EventPlayerAttackSuccess):
            match event.gun_type:
                case Const.GUN_TYPE_NORMAL_GUN:
                    self.normal_gun_sound.play()
                case Const.GUN_TYPE_MACHINE_GUN:
                    self.machine_gun_sound.play()
                case Const.GUN_TYPE_SHOTGUN:
                    self.shotgun_sound.play()
                case Const.GUN_TYPE_SNIPER:
                    self.sniper_sound.play()
        
        elif isinstance(event, EventPlayerBuffed):
            self.player_pick_up_item_sound.play()

        elif isinstance(event, EventPlayerSwitchGun):
            self.switch_gun_sound.play()
        
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
            pg.mixer.unpause()
                
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
        