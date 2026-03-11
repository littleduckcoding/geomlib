from __future__ import annotations
from typing import TYPE_CHECKING
import math
from geomlib.constants import EPS

if TYPE_CHECKING:
    from geomlib.point import Point

class Vector:
    __slots__ = ['x', 'y']

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    @staticmethod
    def from_point(point: Point) -> 'Vector':
        return Vector(point.x, point.y)

    @staticmethod
    def from_points(p1: Point, p2: Point) -> 'Vector':
        return Vector(p2.x - p1.x, p2.y - p1.y)
    
    def magnitude(self) -> float:
        """
        Calculate the magnitude (length) of the vector.

        :return: The magnitude of the vector.
        :rtype: float
        """
        return math.hypot(self.x, self.y)
    
    def magnitude2(self) -> float:
        """
        Calculate the squared magnitude of the vector.

        :return: The squared magnitude of the vector.
        :rtype: float
        """
        return self.x * self.x + self.y * self.y
    
    def project(self, other: 'Vector') -> 'Vector':
        """
        Project the vector onto another vector.

        The projected vector is the vector that is closest to the original vector
        and is parallel to the other vector.

        :param other: The vector to project onto.
        :type other: Vector
        :return: The projected vector.
        :rtype: Vector
        """
        return other * (self.dot(other) / other.magnitude2())

    def rotate(self, angle: float) -> 'Vector':
        """
        Rotate the vector by the given angle (in radians).

        The rotated vector is the vector that is closest to the original vector
        and is rotated by the given angle.

        :param angle: The angle (in radians) to rotate the vector by.
        :type angle: float
        :return: The rotated vector.
        :rtype: Vector
        """
        c = math.cos(angle)
        s = math.sin(angle)
        return Vector(
            self.x * c - self.y * s,
            self.x * s + self.y * c
        )

    def normalize(self) -> 'Vector':
        """
        Normalize the vector.

        :return: A vector with the same direction as self, but with a magnitude of 1.
        :rtype: Vector
        :raises ValueError: If self is a zero vector.
        """
        mag = self.magnitude()
        if mag == 0:
            raise ValueError("Cannot normalize a zero vector")
        return Vector(self.x / mag, self.y / mag)
    
    def normal(self) -> 'Vector':
        """
        Return a vector perpendicular to self.

        The returned vector is of the same magnitude as self, but is perpendicular to it.

        :return: A vector perpendicular to self.
        :rtype: Vector
        """
        return Vector(-self.y, self.x)

    def dot(self, other: 'Vector') -> float:
        """
        Calculate the dot product of the vectors self and other.

        The dot product is the sum of the products of corresponding corresponding components.
        It is a measure of how similar the two vectors are.

        :param other: The other vector to calculate the dot product with.
        :type other: Vector
        :return: The dot product of the vectors self and other.
        :rtype: float
        :raises TypeError: If other is not a Vector instance.
        """
        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y
        else:
            raise TypeError("Unsupported type for dot product")
        
    def cross(self, other: 'Vector') -> float:
        """
        Calculate the cross product of the vectors self and other.

        The cross product is positive if other is to the left of self (counter-clockwise direction),
        negative if other is to the right of self (clockwise direction), and zero if self and other are collinear.

        :param other: The other vector to calculate the cross product with.
        :type other: Vector
        :return: The cross product of the vectors self and other.
        :rtype: float
        :raises TypeError: If other is not a Vector instance.
        """
        if isinstance(other, Vector):
            return self.x * other.y - self.y * other.x
        else:
            raise TypeError("Unsupported type for cross product")
        
    def angle(self, other: 'Vector') -> float:
        """
        Calculate the angle between two vectors.

        The angle is in radians and is between 0 and pi (inclusive).

        :param other: The other vector to calculate the angle with.
        :type other: Vector
        :return: The angle between the two vectors.
        :rtype: float
        :raises ValueError: If either of the vectors is a zero vector.
        :raises TypeError: If other is not a Vector instance.
        """
        if isinstance(other, Vector):
            if self.magnitude() == 0 or other.magnitude() == 0:
                raise ValueError("Angle undefined for zero vector")
            cos_theta = self.dot(other) / (self.magnitude() * other.magnitude())
            cos_theta = max(-1.0, min(1.0, cos_theta))
            return math.acos(cos_theta)
        else:
            raise TypeError("Unsupported type for angle")
    
    def angle_degrees(self, other: 'Vector') -> float:
        """
        Calculate the angle between two vectors in degrees.

        The angle is in degrees and is between 0 and 180 (inclusive).

        :param other: The other vector to calculate the angle with.
        :type other: Vector
        :return: The angle between the two vectors in degrees.
        :rtype: float
        :raises ValueError: If either of the vectors is a zero vector.
        :raises TypeError: If other is not a Vector instance.
        """
        return math.degrees(self.angle(other))
    
    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return NotImplemented
        
    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        return NotImplemented
        
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other)
        return NotImplemented
        
    def __rmul__(self, other):
        return self.__mul__(other)
        
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            return Vector(self.x / other, self.y / other)
        return NotImplemented
    
    def __neg__(self):
        return Vector(-self.x, -self.y)
        
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
    
    def __str__(self):
        return f"Vector({self.x}, {self.y})"
    
    def __eq__(self, other):
        if isinstance(other, Vector):
            return abs(self.x - other.x) < EPS and abs(self.y - other.y) < EPS
        return NotImplemented
    
    def __ne__(self, other):
        if isinstance(other, Vector):
            return abs(self.x - other.x) > EPS or abs(self.y - other.y) > EPS
        return NotImplemented
    