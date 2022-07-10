import pygame as pg
import sys

from EventManager.EventManager import EventManager
from Model.Model import GameEngine
from Controller.Controller import Controller
from View.View import GraphicalView
from API.interface import Interface
import Const

def main(argv):
    # Initialization
    pg.init()
    
    # EventManager listen to events and notice model, controller, view
    AIs = []
    special_modes = []
    map_name = "random"
    skip_tag = False
    for idx in range(1, len(argv)):
        if skip_tag:
            skip_tag = False
            continue
        arg = argv[idx]
        if arg.lower() in ('--nodebug', '-nd'):
            special_modes.append('NODEBUG')
        elif arg.lower() in ('--timeout', '-t'):
            special_modes.append('TIMEOUT')
        elif arg.lower() in ('--map', '-m'):
            skip_tag = True
            map_name = argv[idx+1]
        else:
            AIs.append(arg)

    assert len(AIs) <= Const.PLAYER_NUMBER, "too many AIs!"

    ev_manager = EventManager()
    model      = GameEngine(ev_manager, map_name, AIs)
    controller = Controller(ev_manager, model)
    view       = GraphicalView(ev_manager, model)
    interface  = Interface(ev_manager, model, special_modes)

    # Main loop
    model.run()


if __name__ == "__main__":
    main(sys.argv)
