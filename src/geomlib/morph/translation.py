from __future__ import annotations
from geomlib.morph.base import Morph
from geomlib.point import Point
from geomlib.vector import Vector

class Translation(Morph):

    def __init__(self, dx: float, dy: float):
        self.dx = dx
        self.dy = dy

    def apply_point(self, p: Point) -> Point:
        return Point(p.x + self.dx, p.y + self.dy)
    
    def apply_vector(self, v: Vector) -> Vector:
        return v
    