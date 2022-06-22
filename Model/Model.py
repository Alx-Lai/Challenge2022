import random
import time
import pygame as pg

from EventManager.EventManager import *
from Model.GameObject.item_generator import *
from Model.GameObject.player import *
from Model.GameObject.obstacle import *
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

    def push(self, state):
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

    def __init__(self, ev_manager: EventManager):
        '''
        This function is called when the GameEngine is created.
        For more specific objects related to a game instance
            , they should be initialized in GameEngine.initialize()
        '''
        self.ev_manager = ev_manager
        ev_manager.register_listener(self)

        self.state_machine = StateMachine()

    def initialize(self):
        '''
        This method is called when a new game is instantiated.
        '''
        self.clock = pg.time.Clock()
        self.state_machine.push(Const.STATE_MENU)
        self.players = [Player(self, i) for i in range(Const.PLAYER_NUMBER)]
        self.death_cnt = Const.PLAYER_INIT_DEATH_CNT
        self.obstacles = [Obstacle(self, Const.OBSTACLE_POSITION[i], Const.OBSTACLE_RADIUS) for i in range(len(Const.OBSTACLE_POSITION))] + \
                         [RE_Field(self, Const.RE_FIELD_POSITION[i], Const.RE_FIELD_RADIUS) for i in range(len(Const.RE_FIELD_POSITION))]
        self.bullets = []
        self.items = []
        self.item_generator = Item_Generator(self)

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

        elif isinstance(event, EventPlayerAttack): # invisible players cannot attack
            if not self.players[event.player_id].invisible():
                self.players[event.player_id].attack()

        elif isinstance(event, EventTimesUp):
            self.state_machine.push(Const.STATE_ENDGAME)

        elif isinstance(event, EventPlayerRemove):
            self.death_cnt += 1

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
            if obstacle.killed(): self.obstacles.remove(player)
            else: obstacle.tick()

        for obstacle in self.obstacles:
            if obstacle.killed(): self.obstacles.remove(player)
            else: obstacle.tick()

        for bullet in self.bullets:
            if bullet.killed(): self.bullets.remove(bullet)
            else: bullet.tick()

        for item in self.items:
            if item.killed(): self.items.remove(item)
            else: item.tick()

    def update_endgame(self):
        '''
        Update the objects in endgame scene.
        For example: scoreboard
        '''
        for i in range(Const.PLAYER_NUMBER):
            if self.players[i].respawn_count >= 0:
                self.players[i].score += Const.PLAYER_ALIVE_SCORE[3]
                print(i, self.players[i].score)
        scoreboard = pg.display.set_mode(Const.WINDOW_SIZE)
        scoreboard.fill((0,0,0))
        font = pg.font.SysFont('Comic Sans MS', 20)
        player0_score = font.render(f"Score:{self.players[0].score}", True, (255, 255, 255))
        player1_score = font.render(f"Score:{self.players[1].score}", True, (255, 255, 255))
        player2_score = font.render(f"Score:{self.players[2].score}", True, (255, 255, 255))
        player3_score = font.render(f"Score:{self.players[3].score}", True, (255, 255, 255))
        scoreboard.blit(player0_score, (10, 30))
        scoreboard.blit(player1_score, (Const.ARENA_SIZE[0]-110, 30))
        scoreboard.blit(player2_score, (10, Const.ARENA_SIZE[0]-40))
        scoreboard.blit(player3_score, (Const.ARENA_SIZE[0]-110, Const.ARENA_SIZE[0]-40))
        pg.display.flip()
        time.sleep(10)
        self.running = False
        self.state_machine.push(EventQuit())

    def print_information(self):
        player0_score = self.font.render(f"Score:{self.players[0].score}", True, (255, 255, 255))
        player1_score = self.font.render(f"Score:{self.players[1].score}", True, (255, 255, 255))
        player2_score = self.font.render(f"Score:{self.players[2].score}", True, (255, 255, 255))
        player3_score = self.font.render(f"Score:{self.players[3].score}", True, (255, 255, 255))
        player0_lifespan = self.font.render(f"Lifespan:{1+self.players[0].respawn_count}", True, (255, 255, 255))
        player1_lifespan = self.font.render(f"Lifespan:{1+self.players[1].respawn_count}", True, (255, 255, 255))
        player2_lifespan = self.font.render(f"Lifespan:{1+self.players[2].respawn_count}", True, (255, 255, 255))
        player3_lifespan = self.font.render(f"Lifespan:{1+self.players[3].respawn_count}", True, (255, 255, 255))
        countdown = self.font.render(f"{int(self.timer/Const.FPS)}", True, (255, 255, 255))
        self.screen.blit(player0_score, (10,30))
        self.screen.blit(player1_score, (Const.ARENA_SIZE[0]-110, 30))
        self.screen.blit(player2_score, (10, Const.ARENA_SIZE[0]-40))
        self.screen.blit(player3_score, (Const.ARENA_SIZE[0]-110, Const.ARENA_SIZE[0]-40))
        self.screen.blit(player0_lifespan, (10, 10))
        self.screen.blit(player1_lifespan, (Const.ARENA_SIZE[0]-110, 10))
        self.screen.blit(player2_lifespan, (10, Const.ARENA_SIZE[0]-60))
        self.screen.blit(player3_lifespan, (Const.ARENA_SIZE[0]-110, Const.ARENA_SIZE[0]-60))
        self.screen.blit(countdown, (Const.ARENA_SIZE[0]//2 - 20, 0))
        pg.display.flip()
        return
        

    def run(self):
        '''
        The main loop of the game is in this function.
        This function activates the GameEngine.
        '''
        self.running = True
        # Tell every one to start
        self.ev_manager.post(EventInitialize())
        self.timer = Const.GAME_LENGTH
        self.screen = pg.display.set_mode(Const.WINDOW_SIZE)
        self.font = pg.font.SysFont('Comic Sans MS', 20)
        while self.running:
            self.ev_manager.post(EventEveryTick())
            self.print_information()
            self.clock.tick(Const.FPS)           
            if self.death_cnt >= 3:
                self.state_machine.push(Const.STATE_ENDGAME)
                self.update_endgame()
                return


