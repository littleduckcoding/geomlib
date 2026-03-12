from __future__ import annotations
from geomlib.morph.base import Morph
from geomlib.point import Point
from geomlib.vector import Vector

class CompositeMorph(Morph):

    def __init__(self, *morphs):
        self.morphs = morphs

    def apply_point(self, p: Point) -> Point:
        for m in self.morphs:
            p = m.apply_point(p)
        return p
    
    def apply_vector(self, v: Vector) -> Vector:
        for m in self.morphs:
            v = m.apply_vector(v)
        return v
