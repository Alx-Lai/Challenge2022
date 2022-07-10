import csv
from Model.GameObject.obstacle import *
import Const

def map_gen(self, map_name: str) -> list:
    '''
    read <map_name>.csv and return a list of converted obstacles
    '''
    data = []
    obstacles = []
    with open(F"Map/CSV/{map_name}.csv") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        data = list(reader)

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
