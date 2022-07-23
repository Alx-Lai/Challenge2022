import pygame as pg
import sys
import argparse

from EventManager.EventManager import EventManager
from Model.Model import GameEngine
from Controller.Controller import Controller
from View.View import GraphicalView
from View.sound import Audio
from API.interface import Interface
import Const

def main(argv):
    # Initialization
    pg.init()
    
    # EventManager listen to events and notice model, controller, view
    AIs = []
    special_modes = []
    q_mode = False
    map_name = "random"
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='activate debug mode')
    parser.add_argument('-n', '--notimeout', action='store_true', help='deactivate timeout')
    parser.add_argument('-m', '--map', type=str, default='random', help='map type')
    parser.add_argument('-q', '--quiet', action='store_true', help='turn off sound')
    parser.add_argument('rest', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    
    if args.debug:
        special_modes.append('DEBUG')
    if args.notimeout:
        special_modes.append('NOTIMEOUT')
    q_mode = args.quiet
    map_name = args.map

    
    for AI in args.rest:
        AIs.append(AI)
    assert len(AIs) <= Const.PLAYER_NUMBER, "too many AIs!"

    ev_manager = EventManager()
    model      = GameEngine(ev_manager, map_name, AIs)
    controller = Controller(ev_manager, model)
    view       = GraphicalView(ev_manager, model)
    sound      = Audio(ev_manager, model, q_mode)
    interface  = Interface(ev_manager, model, special_modes)

    # Main loop
    model.run()


if __name__ == "__main__":
    main(sys.argv)
