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
                self.players[i].score += Const.ALIVE_SCORE
        scoreboard = pg.display.set_mode(Const.WINDOW_SIZE)
        scoreboard.fill((0,0,0))
        font = pg.font.SysFont('Comic Sans MS', 20)
        player0_score = font.render(f"Score:{self.players[0].score}", True, (255, 255, 255))
        player0_score_text = (10,30)
        player1_score = font.render(f"Score:{self.players[1].score}", True, (255, 255, 255))
        player1_score_text = (Const.ARENA_SIZE[0]-110,30)
        player2_score = font.render(f"Score:{self.players[2].score}", True, (255, 255, 255))
        player2_score_text = (10,Const.ARENA_SIZE[0]-40)
        player3_score = font.render(f"Score:{self.players[3].score}", True, (255, 255, 255))
        player3_score_text = (Const.ARENA_SIZE[0]-110,Const.ARENA_SIZE[0]-40)
        scoreboard.blit(player0_score, player0_score_text)
        scoreboard.blit(player1_score, player1_score_text)
        scoreboard.blit(player2_score, player2_score_text)
        scoreboard.blit(player3_score, player3_score_text)
        pg.display.flip() 
        time.sleep(10)
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
        screen = pg.display.set_mode(Const.WINDOW_SIZE)
        font = pg.font.SysFont('Comic Sans MS', 20)
        while self.running:
            player0_score = font.render(f"Score:{self.players[0].score}", True, (255, 255, 255))
            player0_score_text = (10,30)
            player1_score = font.render(f"Score:{self.players[1].score}", True, (255, 255, 255))
            player1_score_text = (Const.ARENA_SIZE[0]-110,30)
            player2_score = font.render(f"Score:{self.players[2].score}", True, (255, 255, 255))
            player2_score_text = (10,Const.ARENA_SIZE[0]-40)
            player3_score = font.render(f"Score:{self.players[3].score}", True, (255, 255, 255))
            player3_score_text = (Const.ARENA_SIZE[0]-110,Const.ARENA_SIZE[0]-40)
            player0_lifespan = font.render(f"Lifespan:{1+self.players[0].respawn_count}", True, (255, 255, 255))
            player0_lifespan_text = (10,10)
            player1_lifespan = font.render(f"Lifespan:{1+self.players[1].respawn_count}", True, (255, 255, 255))
            player1_lifespan_text = (Const.ARENA_SIZE[0]-110,10)
            player2_lifespan = font.render(f"Lifespan:{1+self.players[2].respawn_count}", True, (255, 255, 255))
            player2_lifespan_text = (10,Const.ARENA_SIZE[0]-60)
            player3_lifespan = font.render(f"Lifespan:{1+self.players[3].respawn_count}", True, (255, 255, 255))
            player3_lifespan_text = (Const.ARENA_SIZE[0]-110,Const.ARENA_SIZE[0]-60)
            countdown = font.render(f"{int(self.timer/Const.FPS)}", True, (255, 255, 255))
            countdown_text = (Const.ARENA_SIZE[0] // 2 - 20,0)
            self.ev_manager.post(EventEveryTick())
            screen.blit(player0_score, player0_score_text)
            screen.blit(player1_score, player1_score_text)
            screen.blit(player2_score, player2_score_text)
            screen.blit(player3_score, player3_score_text)
            screen.blit(player0_lifespan, player0_lifespan_text)
            screen.blit(player1_lifespan, player1_lifespan_text)
            screen.blit(player2_lifespan, player2_lifespan_text)
            screen.blit(player3_lifespan, player3_lifespan_text)
            screen.blit(countdown, countdown_text)
            pg.display.flip() 
            self.clock.tick(Const.FPS)           
            if Const.ALIVE_PLAYER_NUMBER <= 1:
                self.state_machine.push(Const.STATE_ENDGAME)
                self.update_endgame()
                return


