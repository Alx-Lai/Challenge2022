import random
import pygame as pg

from EventManager.EventManager import *
from Model.GameObject.item_generator import *
from Model.GameObject.player import *
from Model.GameObject.obstacle import *
from Map.map_generator import map_gen
import Const



class StateMachine(object):
    '''
    Manages a stack based state machine.
    peek(), pop() and push() perform as traditionally expected.
    peeking and popping an empty stack returns None.

    TL;DR. Just for game state recording.
    '''

    def __init__(self):
        self.statestack = []

    def peek(self):
        '''
        Returns the current state without altering the stack.
        Returns None if the stack is empty.
        '''
        try:
            return self.statestack[-1]
        except IndexError:
            # empty stack
            return None

    def pop(self):
        '''
        Returns the current state and remove it from the stack.
        Returns None if the stack is empty.
        '''
        try:
            return self.statestack.pop()
        except IndexError:
            # empty stack
            return None

    def push(self, state: int):
        '''
        Push a new state onto the stack.
        Returns the pushed value.
        '''
        self.statestack.append(state)
        return state

    def clear(self):
        '''
        Clear the stack.
        '''
        self.statestack = []


class GameEngine:
    '''
    The main game engine. The main loop of the game is in GameEngine.run()
    '''

    def __init__(self, ev_manager: EventManager, map_name: str, AI_names: list):
        '''
        This function is called when the GameEngine is created.
        For more specific objects related to a game instance
            , they should be initialized in GameEngine.initialize()
        '''
        self.ev_manager = ev_manager
        ev_manager.register_listener(self)
        self.state_machine = StateMachine()
        self.map_name = map_name

        self.AI_names = AI_names
        while len(self.AI_names) < Const.PLAYER_NUMBER:
            self.AI_names.append('manual')

    def initialize(self):
        '''
        This method is called when a new game is instantiated.
        '''
        self.clock = pg.time.Clock()
        
        self.state_machine.push(Const.STATE_MENU)
        self.players = [Player(self, i, self.AI_names[i], self.AI_names[i] != 'manual') for i in range(Const.PLAYER_NUMBER)]
        self.death_cnt = 0
        self.obstacles = map_gen(self, self.map_name)
        self.bullets = []
        self.items = []
        self.item_generator = Item_Generator(self)
        self.alive_score_add = False

    def notify(self, event: BaseEvent):
        '''
        Called by EventManager when a event occurs.
        '''
        if isinstance(event, EventInitialize):
            self.initialize()

        elif isinstance(event, EventEveryTick):
            # Peek the state of the game and do corresponding work
            cur_state = self.state_machine.peek()
            if cur_state == Const.STATE_MENU:
                self.update_menu()
            elif cur_state == Const.STATE_PLAY:
                self.update_objects()

                self.timer -= 1
                if self.timer == 0:
                    self.ev_manager.post(EventTimesUp())
            elif cur_state == Const.STATE_ENDGAME:
                self.update_endgame()

        elif isinstance(event, EventStateChange):
            if event.state == Const.STATE_POP:
                if self.state_machine.pop() is None:
                    self.ev_manager.post(EventQuit())
            else:
                self.state_machine.push(event.state)

        elif isinstance(event, EventQuit):
            self.running = False

        elif isinstance(event, EventPlayerMove):
            self.players[event.player_id].move_direction(event.direction)

        elif isinstance(event, EventPlayerNoMove):
            self.players[event.player_id].stop_moving()

        elif isinstance(event, EventPlayerRotate):
            self.players[event.player_id].rotate(event.direction)

        elif isinstance(event, EventPlayerAttack):  # invisible players cannot attack
            if not self.players[event.player_id].invisible():
                self.players[event.player_id].attack()

        elif isinstance(event, EventPlayerRemove):
            self.death_cnt += 1

        elif isinstance(event, EventTimesUp):
            self.state_machine.push(Const.STATE_ENDGAME)

    def update_menu(self):
        '''
        Update the objects in welcome scene.
        For example: game title, hint text
        '''
        pass

    def update_objects(self):
        '''
        Update the objects not controlled by user.
        For example: obstacles, items, special effects
        '''
        self.item_generator.tick()

        for player in self.players:
            if not player.killed(): player.tick()

        for obstacle in self.obstacles:
            if obstacle.killed():
                self.obstacles.remove(obstacle)
            else:
                obstacle.tick()

        for bullet in self.bullets:
            if bullet.killed():
                self.bullets.remove(bullet)
            else:
                bullet.tick()

        for item in self.items:
            if item.killed():
                self.items.remove(item)
            else:
                item.tick()

    def update_endgame(self):
        '''
        Update the objects in endgame scene.
        For example: scoreboard
        '''
        if not self.alive_score_add:
            self.alive_score_add = True
            for i in range(Const.PLAYER_NUMBER):
                if self.players[i].respawn_count >= 0:
                    self.players[i].score += Const.PLAYER_ALIVE_SCORE[3]

    def run(self):
        '''
        The main loop of the game is in this function.
        This function activates the GameEngine.
        '''
        self.running = True
        # Tell every one to start
        self.timer = Const.GAME_LENGTH
        self.ev_manager.post(EventInitialize())
        self.screen = pg.display.set_mode(Const.WINDOW_SIZE)
        self.font = pg.font.SysFont('Comic Sans MS', 20)
        while self.running:
            self.ev_manager.post(EventEveryTick())
            self.clock.tick(Const.FPS)           
            if self.death_cnt >= Const.PLAYER_NUMBER-1:
                self.state_machine.push(Const.STATE_ENDGAME)


