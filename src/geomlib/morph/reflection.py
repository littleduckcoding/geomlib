from __future__ import annotations
from geomlib.morph.base import Morph
from geomlib.point import Point
from geomlib.vector import Vector
from geomlib.line import Line


class Reflection(Morph):

    def __init__(self, line: Line):
        self.line = line

    def apply_point(self, p: Point) -> Point:
        a, b, c = self.line.a, self.line.b, self.line.c

        d = (a * p.x + b * p.y + c) / (a * a + b * b)

        x = p.x - 2 * a * d
        y = p.y - 2 * b * d

        return Point(x, y)

    def apply_vector(self, v: Vector) -> Vector:
        a, b = self.line.a, self.line.b
        denom = a * a + b * b

        d = (a * v.x + b * v.y) / denom

        x = v.x - 2 * a * d
        y = v.y - 2 * b * d

        return Vector(x, y)
    