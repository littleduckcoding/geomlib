from geomlib.point import Point
from geomlib.line import Line
from geomlib.constants import EPS
import math

class Circle:
    __slots__ = ['center', 'radius']
    
    def __init__(self, center: Point, radius: float):
        if radius < 0:
            raise ValueError("Radius must be non-negative")
        self.center = center
        self.radius = radius

    @staticmethod
    def from_points(p1: Point, p2: Point, p3: Point) -> 'Circle':
        """
        Returns a Circle object that passes through three points p1, p2, and p3.
        """
        A = 2 * (p1.x * (p2.y - p3.y) + p2.x * (p3.y - p1.y) + p3.x * (p1.y - p2.y))
        if abs(A) < EPS:
            raise ValueError("The three points are collinear.")
        
        B = (p1.x ** 2 + p1.y ** 2) * (p2.y - p3.y) + (p2.x ** 2 + p2.y ** 2) * (p3.y - p1.y) + (p3.x ** 2 + p3.y ** 2) * (p1.y - p2.y)
        C = (p1.x ** 2 + p1.y ** 2) * (p3.x - p2.x) + (p2.x ** 2 + p2.y ** 2) * (p1.x - p3.x) + (p3.x ** 2 + p3.y ** 2) * (p2.x - p1.x)
        
        center_x = -B / A
        center_y = -C / A
        center = Point(center_x, center_y)
        radius = center.distance_to(p1)
        return Circle(center, radius)
    
    def diameter(self) -> float:
        """
        Returns the diameter of the circle.
        """
        return 2 * self.radius
    
    def point_at_angle(self, angle: float) -> Point:
        """
        Returns the point on the circle at the given angle (in radians).

        Parameters
        ----------
        angle : float
            The angle (in radians) at which to find the point.

        Returns
        -------
        Point
            The point on the circle at the given angle.
        """
        return Point(
            self.center.x + self.radius * math.cos(angle),
            self.center.y + self.radius * math.sin(angle)
        )
    
    def arc_length(self, angle: float) -> float:
        """
        Parameters
        ----------
        angle : float
            The angle (in radians) of the arc.

        Returns
        -------
        float
            The length of the arc.
        """
        return self.radius * angle

    def get_intersection(self, other: 'Circle') -> list[Point]:
        """
        Find the intersections of two circles.

        Parameters
        ----------
        other : Circle
            The other circle to find the intersections with.

        Returns
        -------
        list[Point]
            A list of up to two points that are the intersections of the two circles.
        """
        
        d = self.center.distance_to(other.center)
        if d > self.radius + other.radius + EPS:
            return []  # No intersection
        if d < abs(self.radius - other.radius) - EPS:
            return []  # One circle is inside the other
        if d < EPS:
            return []
        
        a = (self.radius ** 2 - other.radius ** 2 + d ** 2) / (2 * d)
        h = math.sqrt(max(0, self.radius ** 2 - a ** 2))
        x = self.center.x + a * (other.center.x - self.center.x) / d
        y = self.center.y + a * (other.center.y - self.center.y) / d
        intersection1 = Point(x + h * (other.center.y - self.center.y) / d, y - h * (other.center.x - self.center.x) / d)
        intersection2 = Point(x - h * (other.center.y - self.center.y) / d, y + h * (other.center.x - self.center.x) / d)
        
        if h < EPS:
            return [intersection1]  # One intersection (tangent)
        
        return [intersection1, intersection2]

    def get_intersection_with_line(self, line: Line) -> list[Point]:
        d = line.distance_to_point(self.center)

        if d > self.radius + EPS:
            return []

        # projection of center onto line
        denom = line.a * line.a + line.b * line.b
        t = -(line.a*self.center.x + line.b*self.center.y + line.c) / denom

        foot = Point(
            self.center.x + line.a*t,
            self.center.y + line.b*t
        )

        if abs(d - self.radius) < EPS:
            return [foot]

        offset = math.sqrt(self.radius**2 - d**2)

        direction = line.get_direction_vector().normalize()

        p1 = foot + direction * offset
        p2 = foot - direction * offset

        return [p1, p2]

    def contains(self, point: Point) -> bool:
        """
        Check if a point is contained within the circle.

        Parameters
        ----------
        point : Point
            The point to check.

        Returns
        -------
        bool
            True if the point is contained within the circle, False otherwise.
        """
        return self.center.distance_to(point) <= self.radius + EPS
    
    def intersects(self, other: 'Circle') -> bool:
        """
        Check if two circles intersect.

        Parameters
        ----------
        other : Circle
            The other circle to check intersection with.

        Returns
        -------
        bool
            True if the two circles intersect, False otherwise.
        """
        return self.center.distance_to(other.center) <= self.radius + other.radius + EPS
    
    def area(self) -> float:
        """
        Calculate the area of the circle.

        Returns
        -------
        float
            The area of the circle.
        """
        return math.pi * self.radius ** 2
    
    def perimeter(self) -> float:
        """
        Calculate the perimeter of the circle.

        Returns
        -------
        float
            The perimeter of the circle.
        """
        return 2 * math.pi * self.radius
    
    def __str__(self) -> str:
        return f"Circle(center={self.center}, radius={self.radius})"
    
    def __repr__(self):
        return f"Circle({self.center!r}, {self.radius})"
    
    def __eq__(self, other) -> bool:
        return self.center == other.center and abs(self.radius - other.radius) < EPS
    
    def __ne__(self, other) -> bool:
        return not self == other
    