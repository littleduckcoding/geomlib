from typing import TYPE_CHECKING
import math
from geomlib.constants import EPS

# avoid circular import
if TYPE_CHECKING:
    from geomlib.vector import Vector

class Point:
    __slots__ = ["x", "y"]

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def distance_to(self, other: 'Point') -> float:
        """
        Calculate the Euclidean distance between two points self and other.

        :param other: The other point to calculate the distance to.
        :type other: Point
        :return: The Euclidean distance between self and other.
        :rtype: float
        :raises TypeError: If other is not a Point instance.
        """
        if isinstance(other, Point):
            return math.hypot(self.x - other.x, self.y - other.y)
        raise TypeError("Distance can only be calculated between two Point instances")
    
    def cross3(self, A: 'Point', B: 'Point') -> float:
        """
        Calculate the cross product of the vectors self->A and self->B.
        
        The cross product is positive if B is to the left of A (counter-clockwise direction),
        negative if B is to the right of A (clockwise direction), and zero if A, B and self are collinear.
        
        :return: The cross product of the vectors self->A and self->B.
        :rtype: float
        """
        return (A.x - self.x) * (B.y - self.y) - (A.y - self.y) * (B.x - self.x)

    def cross(self, other: 'Point') -> float:
        """
        Return the 2D cross product of vectors from the origin to self and other.
        Equivalent to determinant |self other|.

        :return: The cross product of the vectors self->other.
        :rtype: float
        """
        if isinstance(other, Point):
            return self.x * other.y - self.y * other.x
        return NotImplemented
    
    def midpoint(self, other):
        """
        Calculate the midpoint between two points self and other.

        :param other: The other point to calculate the midpoint with.
        :type other: Point
        :return: The midpoint between self and other.
        :rtype: Point
        """
        return (self + other) / 2
    
    def norm(self):
        """
        Calculate the Euclidean norm of the point self.

        :return: The Euclidean norm of the point self.
        :rtype: float
        """
        return math.hypot(self.x, self.y)
    
    def rotate(self, angle: float, in_radian: bool = False) -> 'Point':
        """
        Rotate the point self by an angle in either degrees or radians.

        :param angle: The angle to rotate the point by.
        :type angle: float
        :param in_radian: If the angle is given in radians (True) or degrees (False).
        :type in_radian: bool
        :return: The rotated point.
        :rtype: Point
        :raises TypeError: If angle is not a float instance.
        """
        if not in_radian:
            angle = math.radians(angle)
        return Point(self.x * math.cos(angle) - self.y * math.sin(angle), self.x * math.sin(angle) + self.y * math.cos(angle))

    def __add__(self, other):
        if isinstance(other, Vector):
            return Point(self.x + other.x, self.y + other.y)
        return NotImplemented
    
    def __sub__(self, other):
        if isinstance(other, Point):
            return Vector(self.x - other.x, self.y - other.y)
        if isinstance(other, Vector):
            return Point(self.x - other.x, self.y - other.y)
        return NotImplemented
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Point(self.x * other, self.y * other)
        return NotImplemented
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            return Point(self.x / other, self.y / other)
        return NotImplemented
    
    def __eq__(self, other):
        if isinstance(other, Point):
            return abs(self.x - other.x) < EPS and abs(self.y - other.y) < EPS
        return NotImplemented
    
    def __ne__(self, other):
        if isinstance(other, Point):
            return not self.__eq__(other)
        return NotImplemented

    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"
    
    def __lt__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return (self.x, self.y) < (other.x, other.y)