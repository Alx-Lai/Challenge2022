import numpy as np
import pygame as pg 
import Const
from AI.lib.Const import *

# General
def minIndex(inputList: list) -> int:
    minValue = min(inputList)
    return inputList.index(minValue)

def maxIndex(inputList: list) -> int:
    maxValue = max(inputList)
    return inputList.index(maxValue)

def clamp(tar, smallest, largest):
    return max(smallest, min(tar, largest))

# Geometry
def unitVector(vector):
    return vector / np.linalg.norm(vector)

def orientation(v1, v2):
    v1_u = unitVector(np.array(v1))
    v2_u = unitVector(np.array(v2))
    cross = np.cross(v1_u, v2_u) 
    if cross > 0:
        return 1
    else:
        return -1
    
def angleBetween(v1, v2):
    ori = orientation(v1, v2)
    v1_u = unitVector(np.array(v1))
    v2_u = unitVector(np.array(v2))
    return ori * np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def inSegment(l1: pg.Vector2, l2: pg.Vector2, p: pg.Vector2):
    """Check if point p is in segment (l1, l2)."""
    return orientation(l2-l1, p-l1) == 0 and (p - l1).dot(p - l2) <= 0

def banana(a1: pg.Vector2, a2: pg.Vector2, b1: pg.Vector2, b2: pg.Vector2):
    """Check if segment (a1, a2) intersects with segment (b1, b2)."""
    if inSegment(a1, a2, b1) or inSegment(a1, a2, b2) or inSegment(b1, b2, a1) or inSegment(b1, b2, a2):
        return True
    return  orientation(a2-a1, b1-a1) * orientation(a2-a1, b2-a1) < 0 and \
            orientation(b2-b1, a1-b1) * orientation(b2-b1, a2-b1) < 0

# Graph
def in_graph(x, y) -> bool:
        return 0 < min(x, y) and max(x, y) < Const.ARENA_GRID_COUNT

def index(px, py = -1) -> int:
    if py == -1:
        if not in_graph(px.x, px.y):
            return 0
        x = round(px.x * SCALE)
        y = round(px.y * SCALE)
    else:
        if not in_graph(px, py):
            return 0
        x = round(px * SCALE)
        y = round(py * SCALE)
    return clamp(y + x * LENGTH, 0, LENGTH ** 2-1)

def normalize(px, py = -1):
    if py == -1:
        nx = round(px.x * SCALE) / SCALE
        ny = round(px.y * SCALE) / SCALE
    else:
        nx = round(px * SCALE) / SCALE
        ny = round(py * SCALE) / SCALE
    return (nx, ny)