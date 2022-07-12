from cgitb import handler
import imp, traceback, signal
from xmlrpc.client import Boolean
import pygame as pg
import Const
from API.helper import Helper
from EventManager.EventManager import *
import Model.Model
import os

AI_DIR_NONE = {'forward':False, 'backward':False, 'left':False, 'right':False, 'attack':False}

class Interface(object):
    def __init__(self, ev_manager, model : Model.Model, modes : list):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
        """
        self.ev_manager = ev_manager
        ev_manager.register_listener(self)
        self.model = model
        self.player_AI = {}
        self.is_init_AI = False
        self.debug_mode = 'NODEBUG' not in modes
        self.timeout_mode = 'TIMEOUT' in modes
        self.signal_support = False

        if self.timeout_mode and os.name != 'nt':
            signal.signal(signal.SIGALRM, handler)
            self.signal_support = True
        elif self.timeout_mode:
            print('Windows not Support Timeout')

    def notify(self, event: BaseEvent):
        """
        Receive events posted to the message queue.
        """
        if isinstance(event, EventEveryTick):
            cur_state = self.model.state_machine.peek()
            if cur_state == Const.STATE_PLAY:
                self.API_play()
        elif isinstance(event, EventQuit):
            pass
        elif isinstance(event, EventInitialize):
            self.initialize()

    def handler(signum, frame):
        raise TimeoutError

    def API_play(self):
        for player in self.model.players:
            if player.is_AI:
                AI_dir = None
                if self.debug_mode:
                    AI_dir = self.player_AI[player.player_id].decide()
                else:
                    try:
                        if self.signal_support: signal.setitimer(signal.ITIMER_REAL, Const.API_TIMEOUT)
                        AI_dir = self.player_AI[player.player_id].decide()
                        if self.signal_support: signal.setitimer(signal.ITIMER_REAL, 0)
                    except:
                        pass

                if not isinstance(AI_dir, dict):
                    temp = AI_dir
                    AI_dir = AI_DIR_NONE
                    if temp == 0:
                        AI_dir['forward'] = True
                    elif temp == 1:
                        AI_dir['backward'] = True
                    elif temp == 2:
                        AI_dir['left'] = True
                    elif temp == 3:
                        AI_dir['right'] = True
                    elif temp == 4:
                        AI_dir['attack'] = True
                
                # move
                no_move = True
                if 'forward' in AI_dir.keys() and AI_dir['forward']:
                    self.ev_manager.post(EventPlayerMove(player.player_id, Const.PLAYER_MOVE_FORWARD))
                    no_move = False
                if 'backward' in AI_dir.keys() and AI_dir['backward']:
                    self.ev_manager.post(EventPlayerMove(player.player_id, Const.PLAYER_MOVE_BACKWARD))
                    no_move = False
                if no_move:
                    self.ev_manager.post(EventPlayerNoMove(player.player_id))

                # rotate
                if 'left' in AI_dir.keys() and AI_dir['left']:
                    self.ev_manager.post(EventPlayerRotate(player.player_id, Const.PLAYER_ROTATE_LEFT))
                if 'right' in AI_dir.keys() and AI_dir['right']:
                    self.ev_manager.post(EventPlayerRotate(player.player_id, Const.PLAYER_ROTATE_RIGHT))

                # attack
                if 'attack' in AI_dir.keys() and AI_dir['attack']:
                    self.ev_manager.post(EventPlayerAttack(player.player_id))

    def initialize(self):
        if self.is_init_AI:
            return
        self.is_init_AI = True

        for player in self.model.players:
            if player.player_name == "manual":
                continue

            # load ./AI/Team_<name>.py file
            try:
                loadtmp = imp.load_source('', f"./AI/team_{player.player_name}.py")
            except:
                self.load_msg(str(player.player_id), player.player_name, "AI can't load")
                player.player_name, player.is_AI = "Error", False
                continue
            self.load_msg(str(player.player_id), player.player_name, "Loading")

            # init TeamAI class
            try:
                self.player_AI[player.player_id] = loadtmp.TeamAI(Helper(self.model, player.player_id))
            except:
                self.load_msg(str(player.player_id), player.player_name, "AI init crashed")
                traceback.print_exc()
                player.player_name, player.is_AI = "Error", False
                continue
            self.load_msg(str(player.player_id), player.player_name, "Successful to Load")

    def load_msg(self, player_id, player_name ,msg):
        print(f"[{str(player_id)}] team_{player_name}.py: {msg}")