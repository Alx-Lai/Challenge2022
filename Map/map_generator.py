import csv
import os
import sys
from Model.GameObject.obstacle import *
from random import choice
import Const

def map_gen(self, map_name: str) -> list:
    '''
    read <map_name>.csv and return a list of converted obstacles
    '''
    if map_name.lower() in ('random', 'r'):
        map_name = choice([fileName for fileName in os.listdir("./Map/CSV/") if fileName.endswith(".csv")])
    else:
        map_name += ".csv"

    data = []
    obstacles = []
    try:
        with open(F"./Map/CSV/{map_name}") as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            data = list(reader)
    except:
        print(F"ERROR: Cannot find map file {map_name} under ./Map/CSV")
        sys.exit(2)

    x, y = 0.5, 0.5
    for row in data:
        x = 0.5
        for val in row:
            if val == '1':
                obstacles.append(Obstacle(self, pg.Vector2(x, y), Const.OBSTACLE_RADIUS))
            if val == '2':
                obstacles.append(RE_Field(self, pg.Vector2(x, y), Const.RE_FIELD_RADIUS))
            x += 1
        y += 1
    return obstacles
