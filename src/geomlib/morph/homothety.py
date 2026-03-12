from __future__ import annotations
from geomlib.morph.base import Morph
from geomlib.point import Point
from geomlib.vector import Vector

class Homothety(Morph):

    def __init__(self, center: Point, k: float):
        self.center = center
        self.k = k

    def apply_point(self, p: Point) -> Point:
        x = self.center.x + self.k * (p.x - self.center.x)
        y = self.center.y + self.k * (p.y - self.center.y)
        return Point(x, y)

    def apply_vector(self, v: Vector) -> Vector:
        return Vector(v.x * self.k, v.y * self.k)
