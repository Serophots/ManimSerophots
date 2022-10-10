from __future__ import annotations

import math

from manim import *
from abc import ABC

class LineEquation:
    @staticmethod
    def staticFromX(x, m, c): return m * x + c;
    @staticmethod
    def staticFromY(y, m, c): return (-c+y)/m
    @staticmethod
    def staticCoordinateFromX(x, m, c): return [x, LineEquation.staticFromX(x, m, c), 0]
    @staticmethod
    def staticCoordinateFromY(y, m, c): return [LineEquation.staticFromY(y, m, c), y, 0]

    @staticmethod
    def calcGradient(p1,p2): return (p2[1]-p1[1])/(p2[0]-p1[0])
    @staticmethod
    def calcGradientFromLine(line: Line): return LineEquation.calcGradient(line.get_start(), line.get_end())

    @staticmethod
    def calcYIntercept(y,x,m): return -m*x+y

    #Constructors
    @staticmethod
    def fromPoints(p1,p2) -> LineEquation:
        m = LineEquation.calcGradient(p1,p2)
        return LineEquation(m, LineEquation.calcYIntercept(p1[1], p1[0], m))
    @staticmethod
    def perpendicularTo(line: Line) -> LineEquation: #Chain with .setIntercept or .setInterceptFromPoint
        return LineEquation(-1/LineEquation.calcGradientFromLine(line), 0)


    def __init__(self, m, c):
        self.m = m; self.c = c

    def setIntercept(self, c): self.c = c; return self
    def setInterceptFromPoint(self, x, y):
        self.c = -self.m*x + y
        return self

    def fromX(self,x): return self.m * x + self.c
    def fromY(self,y): return (-self.c+y)/self.m
    def coordinateFromX(self, x): return [x, self.fromX(x), 0]
    def coordinateFromY(self, y): return [self.fromY(y), y, 0]

def getPointOnLinePoints(relativePosition, p1, p2):
    return LineEquation.fromPoints(p1, p2).coordinateFromX((p2[0] - p1[0]) * relativePosition + p1[0])
def getPointOnLine(relativePosition, line: Line): #When relativePosition=0, point 1 of line is returned, when relativePosition=1, point2 is returned (All values inbetween + outbetween)
    return getPointOnLinePoints(relativePosition, line.get_start(), line.get_end())

class PerpendicularLine(Line, ABC):
    def __init__(self, line:Line, relativePosition: float =0.5, length: float=0.2, **kwargs):
        throughPoint = getPointOnLine(relativePosition, line) #Point to draw perpendicular line on
        lineEquation = LineEquation.perpendicularTo(line).setInterceptFromPoint(throughPoint[0], throughPoint[1]) #Line equation for perpendicular line, correctly positioned
        xbuffer = math.sqrt(((length/2)**2)/(1+lineEquation.m**2)) # Take x of throughpoint, plus/minus this buffer to retreive X points to create line of that length Explanation I made: https://www.desmos.com/calculator/4bsdspj5u7
        super().__init__(lineEquation.coordinateFromX(throughPoint[0] - xbuffer), lineEquation.coordinateFromX(throughPoint[0] + xbuffer), **kwargs)