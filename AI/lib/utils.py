import numpy as np
import pygame as pg 
import Const
from AI.lib.Const import *

# General
def MinIndex(inputList: list) -> int:
    minValue = min(inputList)
    return inputList.index(minValue)

def MaxIndex(inputList: list) -> int:
    maxValue = max(inputList)
    return inputList.index(maxValue)

def Clamp(tar: int, smallest: int, largest: int) -> int:
    try:
        return max(smallest, min(tar, largest))
    except:
        print("Clamp ERROR: ", tar, smallest, largest)


# Geometry
def UnitVector(vector):
    return vector / np.linalg.norm(vector)

def Orientation(v1, v2):
    v1_u = UnitVector(np.array(v1))
    v2_u = UnitVector(np.array(v2))
    cross = np.cross(v1_u, v2_u) 
    if cross > 0:
        return 1
    else:
        return -1
    
def AngleBetween(v1, v2):
    ori = Orientation(v1, v2)
    v1_u = UnitVector(np.array(v1))
    v2_u = UnitVector(np.array(v2))
    return ori * np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def InSegment(l1: pg.Vector2, l2: pg.Vector2, p: pg.Vector2):
    """Check if point p is in segment (l1, l2)."""
    return Orientation(l2-l1, p-l1) == 0 and (p - l1).dot(p - l2) <= 0

def Banana(a1: pg.Vector2, a2: pg.Vector2, b1: pg.Vector2, b2: pg.Vector2):
    """Check if segment (a1, a2) intersects with segment (b1, b2)."""
    if InSegment(a1, a2, b1) or InSegment(a1, a2, b2) or InSegment(b1, b2, a1) or InSegment(b1, b2, a2):
        return True
    return  Orientation(a2-a1, b1-a1) * Orientation(a2-a1, b2-a1) < 0 and \
            Orientation(b2-b1, a1-b1) * Orientation(b2-b1, a2-b1) < 0


# Graph
def InGraph(vec: pg.Vector2) -> bool:
    try:
        return 0 <= min(vec.x, vec.y) and max(vec.x, vec.y) < Const.ARENA_GRID_COUNT
    except:
        print("InGraph ERROR: ", vec)

def Index(vec: pg.Vector2) -> int:
    if not InGraph(vec):
        return 0
    try:
        x = round(vec.x * SCALE)
        y = round(vec.y * SCALE)
        return Clamp(y + x * LENGTH, 0, LENGTH ** 2-1)
    except:
        print("Index ERROR: ", vec, x, y)

def Normalize(vec: pg.Vector2) -> pg.Vector2:
    nx = round(vec.x * SCALE) / SCALE
    ny = round(vec.y * SCALE) / SCALE
    return pg.Vector2(nx, ny)