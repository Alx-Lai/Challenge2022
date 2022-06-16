import math
import pygame as pg

from EventManager.EventManager import *
from Model.GameObject.bullet import *
from Model.Model import GameEngine
import Const


class GraphicalView:
    '''
    Draws the state of GameEngine onto the screen.
    '''
    background = pg.Surface(Const.ARENA_SIZE)

    def __init__(self, ev_manager: EventManager, model: GameEngine):
        '''
        This function is called when the GraphicalView is created.
        For more specific objects related to a game instance
            , they should be initialized in GraphicalView.initialize()
        '''
        self.ev_manager = ev_manager
        ev_manager.register_listener(self)

        self.model = model

        self.screen = pg.display.set_mode(Const.WINDOW_SIZE)
        pg.display.set_caption(Const.WINDOW_CAPTION)
        self.background.fill(Const.BACKGROUND_COLOR)

    def initialize(self):
        '''
        This method is called when a new game is instantiated.
        '''
        pass

    def notify(self, event):
        '''
        Called by EventManager when a event occurs.
        '''
        if isinstance(event, EventInitialize):
            self.initialize()

        elif isinstance(event, EventEveryTick):
            self.display_fps()

            cur_state = self.model.state_machine.peek()
            if cur_state == Const.STATE_MENU: self.render_menu()
            elif cur_state == Const.STATE_PLAY: self.render_play()
            elif cur_state == Const.STATE_STOP: self.render_stop()
            elif cur_state == Const.STATE_ENDGAME: self.render_endgame()

    def display_fps(self):
        '''
        Display the current fps on the window caption.
        '''
        pg.display.set_caption(f'{Const.WINDOW_CAPTION} - FPS: {self.model.clock.get_fps():.2f}')

    def render_menu(self):
        # draw background
        self.screen.fill(Const.BACKGROUND_COLOR)

        # draw text
        font = pg.font.Font(None, 36)
        text_surface = font.render("Press [space] to start ...", 1, pg.Color('gray88'))
        text_center = (Const.ARENA_SIZE[0] / 2, Const.ARENA_SIZE[1] / 2)
        self.screen.blit(text_surface, text_surface.get_rect(center=text_center))

        pg.display.flip()

    def render_play(self):
        # draw background
        self.screen.fill(Const.BACKGROUND_COLOR)
        # draw bullets
        for bullet in self.model.items:
            if isinstance(bullet, Bullet):
                points = [vec * Const.ARENA_GRID_SIZE for vec in bullet.vertices]
                color = Const.PLAYER_COLOR[bullet.attacker.player_id]
                center = bullet.position * Const.ARENA_GRID_SIZE
                radius = Const.BULLET_RADIUS * Const.ARENA_GRID_SIZE
                rect = pg.Rect(center.x - radius, center.y - radius, radius * 2, radius * 2)

                # trace
                if len(points) > 1:
                    pg.draw.lines(self.screen, Const.PLAYER_COLOR[bullet.attacker.player_id], False, points, 3)
                
                # bullet
                match bullet.gun_type:
                    case Const.GUN_TYPE_NORMAL_GUN:
                        pg.draw.circle(self.screen, color, center, radius)
                    case Const.GUN_TYPE_MACHINE_GUN:
                        pg.draw.circle(self.screen, color, center, radius / 1.5)
                    case Const.GUN_TYPE_SNIPER:
                        pg.draw.rect(self.screen, color, rect)
                    case Const.GUN_TYPE_SHOTGUN:
                        pg.draw.circle(self.screen, color, center, radius)

        # draw players
        for player in self.model.players:
            color = Const.PLAYER_COLOR[player.player_id]
            center = player.position * Const.ARENA_GRID_SIZE
            aux_line_end = center + player.direction * (player.aux_line_length + 0.5) * Const.ARENA_GRID_SIZE
            radius = Const.PLAYER_RADIUS * Const.ARENA_GRID_SIZE
            rect = pg.Rect(center.x - radius, center.y - radius, radius * 2, radius * 2)

            # aux_line
            pg.draw.aaline(self.screen, pg.Color('white'), center, aux_line_end )

            # player
            pg.draw.circle(self.screen, color, center, radius)

            # gun using time
            total_use_time = Const.GUN_USE_TIME[player.gun.type] * Const.FPS
            stop_angle = (player.gun.use_time / total_use_time) * 2 * math.pi
            pg.draw.arc(self.screen, pg.Color('white'), rect, 0, stop_angle, 8)

            # gun cd
            total_cd = player.attack_cd * player.gun.attack_cd_multiplier * Const.FPS
            stop_angle = (player.gun.cd_time / total_cd) * 2 * math.pi
            pg.draw.arc(self.screen, pg.Color('red'), rect, 0, stop_angle, 4)


        pg.display.flip()

    def render_stop(self):
        pass

    def render_endgame(self):
        # draw background
        self.screen.fill(Const.BACKGROUND_COLOR)

        pg.display.flip()
