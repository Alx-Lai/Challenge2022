import pygame as pg
import sys
import getopt

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
    map_name = "random"
    try:
        opts, args = getopt.getopt(argv[1:], "ntm:")
    except:
        print ("Usage: main.py -m <map_name> <AI_1> <AI_2> ...")
        sys.exit(2)
    for opt, arg in opts:
        if opt.lower() in ('-n', '--nodebug'):
            special_modes.append('NODEBUG')
        elif opt.lower() in ('-t', '--timeout'):
            special_modes.append('TIMEOUT')
        elif opt.lower() in ('-m', '--map'):
            map_name = arg
    for arg in args:
        AIs.append(arg)
    assert len(AIs) <= Const.PLAYER_NUMBER, "too many AIs!"

    ev_manager = EventManager()
    model      = GameEngine(ev_manager, map_name, AIs)
    controller = Controller(ev_manager, model)
    view       = GraphicalView(ev_manager, model)
    sound      = Audio(ev_manager, model)
    interface  = Interface(ev_manager, model, special_modes)

    # Main loop
    model.run()


if __name__ == "__main__":
    main(sys.argv)
