from __future__ import annotations
from geomlib.point import Point
from geomlib.vector import Vector
from geomlib.constants import EPS
from geomlib.morph import Morph
import math

class Line:
    __slots__ = ['a', 'b', 'c']

    def __init__(self, p: Point, q: Point):
        if p == q:
            raise ValueError("Cannot define line from identical points")
        
        self.a = p.y - q.y
        self.b = q.x - p.x
        self.c = p.x * q.y - q.x * p.y

    def transform(self, morph: Morph) -> "Line":
        denom = self.a*self.a + self.b*self.b

        p = Point(
            -self.a * self.c / denom,
            -self.b * self.c / denom
        )

        v = self.get_direction_vector()

        p2 = morph.apply_point(p)
        v2 = morph.apply_vector(v)

        return Line.from_point_and_direction_vector(p2, v2)

    @staticmethod
    def from_coeff(a: float, b: float, c: float) -> "Line":
        line = Line.__new__(Line)
        line.a = a
        line.b = b
        line.c = c
        return line

    @staticmethod
    def from_point_and_normal_vector(p: Point, n: Vector) -> "Line":
        a = n.x
        b = n.y
        c = -(a * p.x + b * p.y)
        return Line.from_coeff(a, b, c)
    
    @staticmethod
    def from_point_and_direction_vector(p: Point, u: Vector) -> "Line":
        return Line.from_point_and_normal_vector(p, u.normal())
    
    def intersect(self, other: "Line") -> Point:
        """
        Compute the intersection point of two lines.

        :param other: The other line to intersect with.
        :type other: Line
        :return: The intersection point of the two lines, or None if the lines are parallel.
        :rtype: Point or None
        """
        det = self.a * other.b - other.a * self.b
        if abs(det) < EPS:
            return None  # Lines are parallel
        
        x = (self.b * other.c - other.b * self.c) / det
        y = (self.c * other.a - other.c * self.a) / det
        return Point(x, y)
    
    def distance_to_point(self, point: Point) -> float:
        """
        Compute the distance from a point to a line.

        :param point: The point to compute the distance to.
        :type point: Point
        :return: The distance from the point to the line.
        :rtype: float
        """
        return abs(self.a * point.x + self.b * point.y + self.c) / math.hypot(self.a, self.b)

    def get_normal_vector(self) -> Vector:
        """
        Return a vector perpendicular to the line.

        The returned vector is of the same magnitude as the line, but is perpendicular to it.

        :return: A vector perpendicular to the line.
        :rtype: Vector
        """
        return Vector(self.a, self.b)
    
    def get_direction_vector(self) -> Vector:
        """
        Return a vector parallel to the line.

        The returned vector is of the same magnitude as the line, but is parallel to it.

        :return: A vector parallel to the line.
        :rtype: Vector
        """
        return Vector(self.b, -self.a)
    
    def contains(self, point: Point) -> bool:
        """
        Check if a point lies on the line.

        :param point: The point to check.
        :type point: Point
        :return: True if the point lies on the line, False otherwise.
        :rtype: bool
        """
        return abs(self.a * point.x + self.b * point.y + self.c) / math.hypot(self.a, self.b) < EPS

    def find_reflection_point(self, point: Point) -> Point:
        """
        Find the reflection point of a point on the line.

        :param point: The point to find the reflection point of.
        :type point: Point
        :return: The reflection point of the point on the line.
        :rtype: Point
        """
        a, b, c = self.a, self.b, self.c
        d = (a * point.x + b * point.y + c) / (a*a + b*b)

        x = point.x - 2 * a * d
        y = point.y - 2 * b * d

        return Point(x, y)

    def __eq__(self, other):
        if not isinstance(other, Line):
            return NotImplemented

        return (
            abs(self.a * other.b - other.a * self.b) < EPS and
            abs(self.a * other.c - other.a * self.c) < EPS and
            abs(self.b * other.c - other.b * self.c) < EPS
        )
    
    def __ne__(self, other):
        if isinstance(other, Line):
            return not self.__eq__(other)
        return NotImplemented
    
    def __str__(self):
        return f"{self.a}x + {self.b}y + {self.c} = 0"

    def __repr__(self):
        return f"Line({self.a}, {self.b}, {self.c})"
    