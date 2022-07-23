from cgitb import handler
import imp, traceback, signal
import Const
from API.helper import Helper
from EventManager.EventManager import *
import Model.Model
import os

ACTION_NONE = {'forward':False, 'backward':False, 'left':False, 'right':False, 'attack':False}

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
        self.debug_mode = 'DEBUG' in modes
        self.timeout_mode = 'NOTIMEOUT' not in modes
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
                action = None
                if self.debug_mode:
                    action = self.player_AI[player.player_id].decide()
                else:
                    try:
                        if self.signal_support: signal.setitimer(signal.ITIMER_REAL, Const.API_TIMEOUT)
                        action = self.player_AI[player.player_id].decide()
                        if self.signal_support: signal.setitimer(signal.ITIMER_REAL, 0)
                    except:
                        pass

                if not isinstance(action, dict):
                    temp = action
                    action = ACTION_NONE.copy()
                    if temp == 0:
                        action['forward'] = True
                    elif temp == 1:
                        action['backward'] = True
                    elif temp == 2:
                        action['left'] = True
                    elif temp == 3:
                        action['right'] = True
                    elif temp == 4:
                        action['attack'] = True
                
                # move
                idle = True
                if 'forward' in action.keys() and action['forward']:
                    self.ev_manager.post(EventPlayerMove(player.player_id, Const.PLAYER_MOVE_FORWARD))
                    idle = False
                if 'backward' in action.keys() and action['backward']:
                    self.ev_manager.post(EventPlayerMove(player.player_id, Const.PLAYER_MOVE_BACKWARD))
                    idle = False
                if idle:
                    self.ev_manager.post(EventPlayerNoMove(player.player_id))

                # rotate
                if 'left' in action.keys() and action['left']:
                    self.ev_manager.post(EventPlayerRotate(player.player_id, Const.PLAYER_ROTATE_LEFT))
                if 'right' in action.keys() and action['right']:
                    self.ev_manager.post(EventPlayerRotate(player.player_id, Const.PLAYER_ROTATE_RIGHT))

                # attack
                if 'attack' in action.keys() and action['attack']:
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
            try:
                player.enhance(self.player_AI[player.player_id].enhancement)
            except:
                self.load_msg(str(player.player_id), player.player_name, "Cannot load enhancement")    
            self.load_msg(str(player.player_id), player.player_name, "Successful to Load")

    def load_msg(self, player_id, player_name ,msg):
        print(f"[{str(player_id)}] team_{player_name}.py: {msg}")