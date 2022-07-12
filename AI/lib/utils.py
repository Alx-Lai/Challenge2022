import numpy as np
import pygame as pg 
import math

def unit_vector(vector):
    return vector / np.linalg.norm(vector)

def orientation(v1, v2):
    v1_u = unit_vector(np.array(v1))
    v2_u = unit_vector(np.array(v2))
    cross = np.cross(v1_u, v2_u) 
    if cross > 0:
        return 1
    else:
        return -1
    
def angle_between(v1, v2):
    ori = orientation(v1, v2)
    v1_u = unit_vector(np.array(v1))
    v2_u = unit_vector(np.array(v2))
    return ori * np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def toVector2(vector) -> pg.Vector2:
    return pg.Vector2(vector[0], vector[1])