from __future__ import annotations
import math
from geomlib.morph.base import Morph
from geomlib.point import Point
from geomlib.vector import Vector

class Rotation(Morph):

    def __init__(self, center: Point, angle: float):
        self.center = center
        self.angle = angle

    def apply_point(self, p: Point) -> Point:
        dx = p.x - self.center.x
        dy = p.y - self.center.y

        c = math.cos(self.angle)
        s = math.sin(self.angle)

        x = dx * c - dy * s
        y = dx * s + dy * c

        return Point(x + self.center.x, y + self.center.y)
    
    def apply_vector(self, v: Vector) -> Vector:
        return Vector(v.x * math.cos(self.angle) - v.y * math.sin(self.angle), v.x * math.sin(self.angle) + v.y * math.cos(self.angle))
    