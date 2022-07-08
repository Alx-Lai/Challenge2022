from cmath import cos
import math
from random import randint
import pygame as pg

from EventManager.EventManager import *
from Model.GameObject.base_game_object import *
from Model.GameObject.bullet import *
from Model.GameObject.item import *
from Model.GameObject.obstacle import *
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
        pg.mixer.init()

    def load_img(self, path: str):
        image = pg.image.load(path)
        return image.convert_alpha()

    def initialize(self):
        '''
        This method is called when a new game is instantiated.
        '''
        #images
        self.player_images = []
        for player_color in Const.PLAYER_IMAGE_PATH:
            player = []
            for path in player_color:
                player.append(self.load_img(path))
            self.player_images.append(player)

        self.item_buff = [0, self.load_img(Const.BUFF_ATTACK_CD_PATH),
                          self.load_img(Const.BUFF_REPULSION_PATH),
                          self.load_img(Const.BUFF_AUX_lINE_PATH)]
        self.item_gun = [0, self.load_img(Const.MACHINE_GUN_PATH),
                         self.load_img(Const.SNIPER_PATH),
                         self.load_img(Const.SHOT_GUN_PATH)]
        self.normal_field = self.load_img(Const.NORMAL_FIELD_PATH)
        self.RE_field = self.load_img(Const.RE_FIELD_PATH)                
        self.background = self.load_img(Const.BACKGROUND_PATH)
        self.background_top = self.load_img(Const.BACKGROUND_TOP_PATH)
        self.menu = self.load_img(Const.MENU_PATH)
        self.score_background = self.load_img(Const.SCORE_BACKGROUND_PATH)
        self.crown = self.load_img(Const.CROWN_PATH)
        self.background_count = 0
        self.background_color = Const.BACKGROUND_COLOR

    def notify(self, event):
        '''
        Called by EventManager when a event occurs.
        '''
        if isinstance(event, EventInitialize):
            self.initialize()

        elif isinstance(event, EventEveryTick):
            self.display_fps()

            cur_state = self.model.state_machine.peek()
            if cur_state == Const.STATE_MENU:
                self.render_menu()
            elif cur_state == Const.STATE_PLAY:
                self.render_play()
            elif cur_state == Const.STATE_STOP:
                self.render_stop()
            elif cur_state == Const.STATE_ENDGAME:
                self.render_endgame()

    def display_fps(self):
        '''
        Display the current fps on the window caption.
        '''
        pg.display.set_caption(f'{Const.WINDOW_CAPTION} - FPS: {self.model.clock.get_fps():.2f}')

    def print_obj(self, img, TL: Vector2, DR: Vector2, direction: Vector2 = Vector2(1, 0)):
        angle = -direction.as_polar()[1]
        scale = abs(math.cos(math.radians(angle))) + abs(math.sin(math.radians(angle)))
        new_x = int(scale * (DR.x - TL.x))
        new_y = int(scale * (DR.y - TL.y))
        diff_x = new_x - (DR.x - TL.x)
        diff_y = new_y - (DR.y - TL.y)
        tmp_img = pg.transform.rotate(img, angle)
        tmp_img = pg.transform.scale(tmp_img, (new_x, new_y))
        self.screen.blit(tmp_img, (TL.x - diff_x/2, TL.y - diff_y/2))

    def draw_leaderboard(self, text_size = 72, player_size = 4, draw_crown = True,pause = False, endgame = False):
        #text position
        text_interval = Const.WINDOW_SIZE[0]/7
        text_start = Const.WINDOW_SIZE[0]/2 - text_interval*2
        text_top = Const.WINDOW_SIZE[1]/1.75
        player_score = []
        i = 0
        #endgame caption
        if endgame == True:
            caption = Text("CONGRATULATION", 80, (255,255,255))
            caption.blit(self.screen, topleft=(Const.WINDOW_SIZE[0]/4.5, Const.WINDOW_SIZE[1]/4))
        elif pause == True:
            caption = Text("PAUSE", 80, (255,255,255))
            caption.blit(self.screen, topleft=(Const.WINDOW_SIZE[0]/2.6, Const.WINDOW_SIZE[1]/4))
        #init score array
        for player in self.model.players:
            player_score.append(player.score)

        for player in self.model.players:
            #draw score
            score_text = Text(str(int(player.score)), text_size, Const.SCORE_COLOR[player.player_id])
            score_text.blit(self.screen, topleft=(text_start + i*text_interval, text_top))
            #draw player
            radius = player_size * Const.PLAYER_RADIUS * Const.ARENA_GRID_SIZE
            center = (text_start + (i+0.3)*text_interval, text_top - radius)
            self.print_obj(self.player_images[player.player_id][player.gun.type], Vector2(center[0] - radius, center[1] - radius),
                           Vector2(center[0] + radius, center[1] + radius))
            #draw crown
            if draw_crown == True:
                if player_score[i] == max(player_score):
                    self.screen.blit(self.crown, (text_start + (i+0.3)*text_interval, center[1] - radius))
            i += 1
            

    def draw_score(self, text_size = 54, draw_crown = True):
        pg.draw.rect(self.screen, (0,0,0), pg.Rect(Const.ARENA_SIZE[0], 0, Const.WINDOW_SIZE[0] - Const.ARENA_SIZE[0],  Const.WINDOW_SIZE[1]))
        #text position
        text_interval = Const.WINDOW_SIZE[1]/7
        text_start = Const.WINDOW_SIZE[1]/2 - text_interval
        text_left= Const.ARENA_SIZE[0] + 0.1*(Const.WINDOW_SIZE[0] - Const.ARENA_SIZE[0])
        #caption
        caption = Text("SCORE", 32, (255,255,255))
        caption.blit(self.screen, topleft=(text_left, text_start - text_interval))
        #init score array
        player_score = []
        i = 0
        for player in self.model.players:
            player_score.append(player.score)

        for player in self.model.players:
            #draw score
            score_text = Text(str(int(player.score)), text_size, Const.SCORE_COLOR[player.player_id])
            score_text.blit(self.screen, topleft=(text_left, text_start + i*text_interval))
            if draw_crown == True:
                if player_score[i] == max(player_score):
                    self.screen.blit(self.crown, (text_left, text_start + (i-0.5)*text_interval))
            i+=1

    def rand_backgroud_color(self, times):
        if self.background_count == times:
            self.background_color = Const.PLAYER_COLOR[randint(0, 3)]
            self.background_count = 0
        else:
            self.background_count += 1

    def render_menu(self):
        # draw background
        self.screen.fill(Const.BACKGROUND_COLOR)
        self.print_obj(self.menu, Vector2(0, 0), Vector2(Const.WINDOW_SIZE))

        pg.display.flip()

    def render_play(self):
        # draw background
        self.rand_backgroud_color(Const.BACKGROUND_COLOR_SPEED)
        self.screen.fill(self.background_color)
        self.print_obj(self.background_top, Vector2(0, 0), Vector2(Const.ARENA_SIZE))
        self.draw_score()
        # draw obstacles
        for obstacle in self.model.obstacles:
            center = obstacle.position * Const.ARENA_GRID_SIZE
            radius = obstacle.radius * Const.ARENA_GRID_SIZE
            rect = pg.Rect(center.x - radius, center.y - radius, radius * 2, radius * 2)
            self.print_obj(self.RE_field if isinstance(obstacle, RE_Field) else self.normal_field, Vector2(center[0] - radius, center[1] - radius),
                           Vector2(center[0] + radius, center[1] + radius))
            #pg.draw.rect(self.screen, pg.Color('pink') if isinstance(obstacle, RE_Field) else pg.Color('white'), rect)

        # draw bullets
        for bullet in self.model.bullets:
            if isinstance(bullet, Bullet):
                center = bullet.position * Const.ARENA_GRID_SIZE
                center_tail = bullet.tail.position * Const.ARENA_GRID_SIZE
                points = [center] + [vec * Const.ARENA_GRID_SIZE for vec in bullet.vertices] + [center_tail]
                color = Const.PLAYER_COLOR[bullet.attacker.player_id]
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

        # draw items
        for item in self.model.items:
            center = item.position * Const.ARENA_GRID_SIZE
            radius = item.radius * Const.ARENA_GRID_SIZE
            rect = pg.Rect(center.x - radius, center.y - radius, radius * 2, radius * 2)
            if isinstance(item, Item_Buff):
                self.print_obj(self.item_buff[item.type], Vector2(center.x - radius, center.y - radius),
                               Vector2(center.x + radius, center.y + radius))

            elif isinstance(item, Item_Gun):
                self.print_obj(self.item_gun[item.type], Vector2(center.x - radius, center.y - radius),
                               Vector2(center.x + radius, center.y + radius))

        # draw players
        for player in self.model.players:
            if player.killed(): continue
            #print(player.position)
            color = Const.PLAYER_COLOR_RESPAWN[player.player_id] if player.respawning() else Const.PLAYER_COLOR[
                player.player_id]
            center = player.position * Const.ARENA_GRID_SIZE
            aux_line_end = center + player.direction * (player.aux_line_length + 0.5) * Const.ARENA_GRID_SIZE
            radius = Const.PLAYER_RADIUS * Const.ARENA_GRID_SIZE
            rect = pg.Rect(center.x - radius, center.y - radius, radius * 2, radius * 2)

            # aux_line
            pg.draw.aaline(self.screen, pg.Color('white'), center, aux_line_end)

            # player
            self.print_obj(self.player_images[player.player_id][player.gun.type], Vector2(center[0] - radius, center[1] - radius),
                           Vector2(center[0] + radius, center[1] + radius), player.direction)

            # pg.draw.circle(self.screen, color, center, radius)

            # gun using time
            total_use_time = Const.GUN_USE_TIME[player.gun.type]
            stop_angle = (player.gun.use_time / total_use_time) * 2 * math.pi
            pg.draw.arc(self.screen, pg.Color('white'), rect, 0, stop_angle, 8)

            # gun cd
            total_cd = round(player.attack_cd * player.gun.attack_cd_multiplier)
            stop_angle = (player.gun.cd_time / total_cd) * 2 * math.pi
            pg.draw.arc(self.screen, pg.Color('red'), rect, 0, stop_angle, 4)

            # respawning time
            total_respawging_time = Const.PLAYER_RESPAWN_TIME
            stop_angle = (player.respawn_timer / total_respawging_time) * 2 * math.pi
            pg.draw.arc(self.screen, Const.PLAYER_COLOR[player.player_id], rect, 0, stop_angle, 4)
        

        pg.display.flip()

    def render_stop(self):
        # draw background
        self.print_obj(self.score_background, Vector2(0, 0), Vector2(Const.WINDOW_SIZE))
        self.draw_leaderboard(pause=True)
        pg.display.flip()

    def render_endgame(self):
        # draw background
        self.print_obj(self.score_background, Vector2(0, 0), Vector2(Const.WINDOW_SIZE))
        self.draw_leaderboard(endgame=True)
        pg.display.flip()

class Text:
    def __init__(self, text, size, color, font = None, antialias = True, bg = None):
        self.font = pg.font.Font(font, size)
        self.surface = self.font.render(text, antialias, color, bg)
    
    def blit(self, screen, **pos):
        self.pos = self.surface.get_rect(**pos)
        screen.blit(self.surface, self.pos)