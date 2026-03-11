from geomlib.point import Point
from geomlib.vector import Vector
from geomlib.constants import EPS

class Segment:
    __slots__ = ['start', 'end']

    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    def on_segment(self, p: Point) -> bool:
        """
        Check if a point p is on the segment.

        :param p: The point to check.
        :type p: Point
        :return: True if the point is on the segment, False otherwise.
        :rtype: bool
        """
        if abs(self.start.cross3(self.end, p)) > EPS:
            return False

        return (min(self.start.x, self.end.x) - EPS <= p.x <= max(self.start.x, self.end.x) + EPS and
                min(self.start.y, self.end.y) - EPS <= p.y <= max(self.start.y, self.end.y) + EPS)
    
    def length(self):
        """
        Calculate the length of the segment.

        :return: The length of the segment.
        :rtype: float
        """
        return self.start.distance_to(self.end)
    
    def midpoint(self):
        """
        Calculate the midpoint of the segment.

        :return: The midpoint of the segment.
        :rtype: Point
        """
        return (self.start + self.end) / 2
    
    def vector(self):
        return Vector.from_points(self.start, self.end)
    
    def intersect(self, other: "Segment") -> bool:
        """
        Check if two segments intersect.

        :param other: The other segment to check intersection with.
        :type other: Segment
        :return: True if the segments intersect, False otherwise.
        :rtype: bool
        """
        A, B = self.start, self.end
        C, D = other.start, other.end

        o1 = A.cross3(B, C)
        o2 = A.cross3(B, D)
        o3 = C.cross3(D, A)
        o4 = C.cross3(D, B)

        # General case
        if o1 * o2 < 0 and o3 * o4 < 0:
            return True

        # Collinear cases
        if abs(o1) < EPS and self.on_segment(C): return True
        if abs(o2) < EPS and self.on_segment(D): return True
        if abs(o3) < EPS and other.on_segment(A): return True
        if abs(o4) < EPS and other.on_segment(B): return True

        return False

    def __eq__(self, other):
        if isinstance(other, Segment):
            return self.start == other.start and self.end == other.end
        return NotImplemented
    
    def __ne__(self, other):
        if isinstance(other, Segment):
            return not self.__eq__(other)
        return NotImplemented

    def __str__(self):
        return f"Segment({self.start}, {self.end})"
    
    def __repr__(self):
        return f"Segment({self.start!r}, {self.end!r})"