import numpy as np
import pygame as pg 

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

def minIndex(inputList: list) -> int:
    minValue = min(inputList)
    return inputList.index(minValue)

def maxIndex(inputList: list) -> int:
    maxValue = max(inputList)
    return inputList.index(maxValue)

def in_segment(l1: pg.Vector2, l2: pg.Vector2, p: pg.Vector2):
    """Check if point p is in segment (l1, l2)."""
    return orientation(l2-l1, p-l1) == 0 and (p - l1).dot(p - l2) <= 0

def is_intersect(a1: pg.Vector2, a2: pg.Vector2, b1: pg.Vector2, b2: pg.Vector2):
    """Check if segment (a1, a2) intersects with segment (b1, b2)."""
    if in_segment(a1, a2, b1) or in_segment(a1, a2, b2) or in_segment(b1, b2, a1) or in_segment(b1, b2, a2):
        return True
    return  orientation(a1, a2, b1) * orientation(a1, a2, b2) < 0 and \
            orientation(b1, b2, a1) * orientation(b1, b2, a2) < 0