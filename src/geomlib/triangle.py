from __future__ import annotations

import math

from geomlib.point import Point
from geomlib.circle import Circle
from geomlib.line import Line
from geomlib.constants import EPS

class Triangle:
    __slots__ = ['A', 'B', 'C']
    def __init__(self, A: Point, B: Point, C: Point):
        self.A = A
        self.B = B
        self.C = C

    def _check_degenerate(self):
        """
        Check if the triangle is degenerate.

        A triangle is degenerate if the three points are collinear. In this case, the area of the triangle is zero.

        :raises ValueError: If the triangle is degenerate.
        """
        if self.area() < EPS:
            raise ValueError("Degenerate triangle (points are collinear)")
    def area(self) -> float:
        """
        Compute the area of the triangle.

        The area is computed using the shoelace formula.

        :return: The area of the triangle.
        :rtype: float
        """
        return 0.5 * abs(
            self.A.x * (self.B.y - self.C.y) +
            self.B.x * (self.C.y - self.A.y) +
            self.C.x * (self.A.y - self.B.y)
        )

    def half_perimeter(self) -> float:
        """
        Compute the half perimeter of the triangle.

        The half perimeter is the sum of the lengths of all sides divided by 2.

        :return: The half perimeter of the triangle.
        :rtype: float
        """
        return self.perimeter() / 2
    def perimeter(self) -> float:
        """
        Compute the perimeter of the triangle.

        The perimeter is the sum of the lengths of all sides.

        :return: The perimeter of the triangle.
        :rtype: float
        """
        return (
            self.A.distance_to(self.B) +
            self.B.distance_to(self.C) +
            self.C.distance_to(self.A)
        )
    
    def incircle(self) -> Circle:
        """
        Compute the incircle of the triangle.

        The incircle is the circle that is inscribed in the triangle.

        :return: The incircle of the triangle.
        :rtype: Circle
        """
        return Circle(self.incenter(), self.inradius())
    
    def circumcircle(self) -> Circle:
        """
        Compute the circumcircle of the triangle.

        The circumcircle is the circle that passes through all three vertices of the triangle.

        :return: The circumcircle of the triangle.
        :rtype: Circle
        """
        return Circle(self.circumcenter(), self.circumradius())

    def inradius(self) -> float:
        """
        Compute the inradius of the triangle.

        The inradius is the radius of the incircle, which is the circle that is inscribed in the triangle.

        :return: The inradius of the triangle.
        :rtype: float
        """
        return self.area() / self.half_perimeter()
    
    def circumradius(self) -> float:
        """
        Compute the circumradius of the triangle.

        The circumradius is the radius of the circumcircle, which is the circle that passes through all three vertices of the triangle.

        :return: The circumradius of the triangle.
        :rtype: float
        :raises ValueError: If the triangle is degenerate.
        """
        self._check_degenerate()

        a = self.B.distance_to(self.C)
        b = self.C.distance_to(self.A)
        c = self.A.distance_to(self.B)
        area = self.area()

        if area < EPS:
            raise ValueError("Degenerate triangle")

        return a * b * c / (4 * area)
    
    def centroid(self) -> Point:
        """
        Compute the centroid of the triangle.

        The centroid is the average of the x and y coordinates of all three vertices.

        :return: The centroid of the triangle.
        :rtype: Point
        """
        return Point(
            (self.A.x + self.B.x + self.C.x) / 3,
            (self.A.y + self.B.y + self.C.y) / 3
        )
    
    def incenter(self) -> Point:
        """
        Compute the incenter of the triangle.

        The incenter is the point where all three angle bisectors of the triangle intersect.

        :return: The incenter of the triangle.
        :rtype: Point
        :raises ValueError: If the triangle is degenerate.
        """

        # use barycentric coordinate (a, b, c) to find incenter
        a = self.B.distance_to(self.C)
        b = self.C.distance_to(self.A)
        c = self.A.distance_to(self.B)
        A = self.A
        B = self.B
        C = self.C
        area = self.area()
        if area == 0:
            raise ValueError("The points are collinear, incenter is undefined.")
        
        x = (a * A.x + b * B.x + c * C.x) / (a + b + c)
        y = (a * A.y + b * B.y + c * C.y) / (a + b + c)
        return Point(x, y)

    def circumcenter(self) -> Point:
        """
        Compute the circumcenter of the triangle.

        The circumcenter is the point where all three perpendicular bisectors of the triangle intersect.

        :return: The circumcenter of the triangle.
        :rtype: Point
        :raises ValueError: If the triangle is degenerate.
        """
        self._check_degenerate()

        D = 2 * (self.A.x * (self.B.y - self.C.y) + self.B.x * (self.C.y - self.A.y) + self.C.x * (self.A.y - self.B.y))
        if abs(D) < EPS:
            raise ValueError("Degenerate triangle")
        
        Ux = ((self.A.x ** 2 + self.A.y ** 2) * (self.B.y - self.C.y) + (self.B.x ** 2 + self.B.y ** 2) * (self.C.y - self.A.y) + (self.C.x ** 2 + self.C.y ** 2) * (self.A.y - self.B.y)) / D
        Uy = ((self.A.x ** 2 + self.A.y ** 2) * (self.C.x - self.B.x) + (self.B.x ** 2 + self.B.y ** 2) * (self.A.x - self.C.x) + (self.C.x ** 2 + self.C.y ** 2) * (self.B.x - self.A.x)) / D
        return Point(Ux, Uy)
    
    def orthocenter(self) -> Point:
        """
        Compute the orthocenter of the triangle.

        The orthocenter is the point where all three altitudes of the triangle intersect.

        :return: The orthocenter of the triangle.
        :rtype: Point
        :raises ValueError: If the triangle is degenerate.
        """
        O = self.circumcenter()
        x = self.A.x + self.B.x + self.C.x - 2 * O.x
        y = self.A.y + self.B.y + self.C.y - 2 * O.y
        return Point(x, y)
    
    def toricelli_point(self) -> Point:
        """
        Compute the Toricelli point of the triangle.

        The Toricelli point is the point where all three angle bisectors of the triangle intersect.

        :return: The Toricelli point of the triangle.
        :rtype: Point
        :raises ValueError: If the triangle is degenerate.
        """
        self._check_degenerate()

        area = self.area()
        if area == 0:
            raise ValueError("The points are collinear, toricelli point is undefined.")

        A, B, C = self.A, self.B, self.C

        # Check for angle >= 120°
        if self.angle_A() >= 2 * math.pi / 3:
            return A
        if self.angle_B() >= 2 * math.pi / 3:
            return B
        if self.angle_C() >= 2 * math.pi / 3:
            return C

        cos60 = 0.5
        sin60 = math.sqrt(3) / 2

        # Rotate C around B by +60°
        x1 = B.x + (C.x - B.x) * cos60 - (C.y - B.y) * sin60
        y1 = B.y + (C.x - B.x) * sin60 + (C.y - B.y) * cos60
        Cp = Point(x1, y1)

        # Rotate C around A by -60°
        x2 = A.x + (C.x - A.x) * cos60 + (C.y - A.y) * sin60
        y2 = A.y - (C.x - A.x) * sin60 + (C.y - A.y) * cos60
        Cpp = Point(x2, y2)

        # Intersection of lines A-Cp and B-Cpp
        x1, y1 = A.x, A.y
        x2, y2 = Cp.x, Cp.y
        x3, y3 = B.x, B.y
        x4, y4 = Cpp.x, Cpp.y

        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(denom) < EPS:
            raise ValueError("Degenerate configuration")

        px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
        py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom

        return Point(px, py)
    
    def lemoine_point(self) -> Point:
        """
        Compute the Lemoine point of the triangle.

        The Lemoine point is the point where the three medians of the triangle intersect.

        :return: The Lemoine point of the triangle.
        :rtype: Point
        :raises ValueError: If the triangle is degenerate.
        """
        a = self.B.distance_to(self.C)
        b = self.C.distance_to(self.A)
        c = self.A.distance_to(self.B)

        A, B, C = self.A, self.B, self.C

        wA = a * a
        wB = b * b
        wC = c * c

        denom = wA + wB + wC

        x = (wA * A.x + wB * B.x + wC * C.x) / denom
        y = (wA * A.y + wB * B.y + wC * C.y) / denom

        return Point(x, y)
    
    def symmedian_from_A(self) -> Line:
        """
        Compute the symmedian from A.

        The symmedian from A is the line that runs from A to the Lemoine point of the triangle.

        :return: The symmedian from A.
        :rtype: Line
        """
        return Line(self.A, self.lemoine_point())

    def symmedian_from_B(self) -> Line:
        """
        Compute the symmedian from B.

        The symmedian from B is the line that runs from B to the Lemoine point of the triangle.

        :return: The symmedian from B.
        :rtype: Line
        """
        return Line(self.B, self.lemoine_point())

    def symmedian_from_C(self) -> Line:
        
        """
        Compute the symmedian from C.

        The symmedian from C is the line that runs from C to the Lemoine point of the triangle.

        :return: The symmedian from C.
        :rtype: Line
        """
        return Line(self.C, self.lemoine_point())
    
    def symmedian_foot_from_A(self) -> Point:
        """
        Compute the symmedian foot from A.

        The symmedian foot from A is the point where the symmedian from A intersects the side BC.

        :return: The symmedian foot from A.
        :rtype: Point
        """
        AB = self.A.distance_to(self.B)
        AC = self.A.distance_to(self.C)

        B, C = self.B, self.C

        wB = AB * AB
        wC = AC * AC

        x = (wB * C.x + wC * B.x) / (wB + wC)
        y = (wB * C.y + wC * B.y) / (wB + wC)

        return Point(x, y)
    
    def symmedian_foot_from_B(self) -> Point:
        """
        Compute the symmedian foot from B.

        The symmedian foot from B is the point where the symmedian from B intersects the side AC.

        :return: The symmedian foot from B.
        :rtype: Point
        """
        BC = self.B.distance_to(self.C)
        BA = self.B.distance_to(self.A)

        A, C = self.A, self.C

        wA = BA * BA
        wC = BC * BC

        x = (wA * C.x + wC * A.x) / (wA + wC)
        y = (wA * C.y + wC * A.y) / (wA + wC)

        return Point(x, y)
    
    def symmedian_foot_from_C(self) -> Point:
        """
        Compute the symmedian foot from C.

        The symmedian foot from C is the point where the symmedian from C intersects the side AB.

        :return: The symmedian foot from C.
        :rtype: Point
        """
        CA = self.C.distance_to(self.A)
        CB = self.C.distance_to(self.B)

        A, B = self.A, self.B

        wA = CA * CA
        wB = CB * CB

        x = (wA * B.x + wB * A.x) / (wA + wB)
        y = (wA * B.y + wB * A.y) / (wA + wB)

        return Point(x, y)
    
    def altitude_from_A(self) -> Line:
        """
        Compute the altitude from A.

        The altitude from A is the line that passes through point A and is perpendicular to side BC.

        :return: The altitude from A.
        :rtype: Line
        """
        return Line(self.A, self.orthocenter())

    def altitude_from_B(self) -> Line:
        """
        Compute the altitude from B.

        The altitude from B is the line that passes through point B and is perpendicular to side AC.

        :return: The altitude from B.
        :rtype: Line
        """
        return Line(self.B, self.orthocenter())

    def altitude_from_C(self) -> Line:
        """
        Compute the altitude from C.

        The altitude from C is the line that passes through point C and is perpendicular to side AB.

        :return: The altitude from C.
        :rtype: Line
        """
        return Line(self.C, self.orthocenter())
    
    def altitude_foot_from_A(self) -> Point:
        """
        Compute the altitude foot from A.

        The altitude foot from A is the point where the altitude from A intersects the side BC.

        :return: The altitude foot from A.
        :rtype: Point
        """
        B, C, A = self.B, self.C, self.A

        BCx = C.x - B.x
        BCy = C.y - B.y

        t = ((A.x - B.x) * BCx + (A.y - B.y) * BCy) / (BCx * BCx + BCy * BCy)

        return Point(
            B.x + t * BCx,
            B.y + t * BCy
        )
    
    def altitude_foot_from_B(self) -> Point:
        # projection of B onto line AC
        """
        Compute the altitude foot from B.

        The altitude foot from B is the point where the altitude from B intersects the side AC.

        :return: The altitude foot from B.
        :rtype: Point
        :raises ValueError: If points A and C are the same, altitude foot is undefined.
        """
        A, C, B = self.A, self.C, self.B

        ACx = C.x - A.x
        ACy = C.y - A.y
        AC_len2 = ACx * ACx + ACy * ACy

        if AC_len2 == 0:
            raise ValueError("Points A and C are the same, altitude foot is undefined.")

        t = ((B.x - A.x) * ACx + (B.y - A.y) * ACy) / AC_len2

        foot_x = A.x + t * ACx
        foot_y = A.y + t * ACy
        return Point(foot_x, foot_y)

    def altitude_foot_from_C(self) -> Point:
        # projection of C onto line AB
        """
        Compute the altitude foot from C.

        The altitude foot from C is the point where the altitude from C intersects the side AB.

        :return: The altitude foot from C.
        :rtype: Point
        :raises ValueError: If points A and B are the same, altitude foot is undefined.
        """
        A, B, C = self.A, self.B, self.C

        ABx = B.x - A.x
        ABy = B.y - A.y
        AB_len2 = ABx * ABx + ABy * ABy

        if AB_len2 == 0:
            raise ValueError("Points A and B are the same, altitude foot is undefined.")

        t = ((C.x - A.x) * ABx + (C.y - A.y) * ABy) / AB_len2

        foot_x = A.x + t * ABx
        foot_y = A.y + t * ABy
        return Point(foot_x, foot_y)
    
    def bisector_from_A(self) -> Line:
        """
        Compute the bisector from A.

        The bisector from A is the line that runs from A to the incenter of the triangle.

        :return: The bisector from A.
        :rtype: Line
        """
        return Line(self.A, self.incenter())

    def bisector_from_B(self) -> Line:
        """
        Compute the bisector from B.

        The bisector from B is the line that runs from B to the incenter of the triangle.

        :return: The bisector from B.
        :rtype: Line
        """
        return Line(self.B, self.incenter())

    def bisector_from_C(self) -> Line:
        """
        Compute the bisector from C.

        The bisector from C is the line that runs from C to the incenter of the triangle.

        :return: The bisector from C.
        :rtype: Line
        """
        return Line(self.C, self.incenter())

    def bisector_foot_from_A(self) -> Point:
        """
        Compute the bisector foot from A.

        The bisector foot from A is the point where the angle bisector from A intersects the side BC.

        :return: The bisector foot from A.
        :rtype: Point
        :raises ValueError: If points A, B, and C are the same, bisector foot is undefined.
        """
        AB = self.A.distance_to(self.B)
        AC = self.A.distance_to(self.C)
        if AB + AC == 0:
            raise ValueError("Points A, B, and C are the same, bisector foot is undefined.")
        
        foot_x = (AB * self.C.x + AC * self.B.x) / (AB + AC)
        foot_y = (AB * self.C.y + AC * self.B.y) / (AB + AC)
        return Point(foot_x, foot_y)

    def bisector_foot_from_B(self) -> Point:
        """
        Compute the bisector foot from B.

        The bisector foot from B is the point where the angle bisector from B intersects the side AC.

        :return: The bisector foot from B.
        :rtype: Point
        :raises ValueError: If points B, A, and C are the same, bisector foot is undefined.
        """
        BA = self.B.distance_to(self.A)
        BC = self.B.distance_to(self.C)
        if BA + BC == 0:
            raise ValueError("Points B, A, and C are the same, bisector foot is undefined.")
        
        foot_x = (BA * self.C.x + BC * self.A.x) / (BA + BC)
        foot_y = (BA * self.C.y + BC * self.A.y) / (BA + BC)
        return Point(foot_x, foot_y)

    def bisector_foot_from_C(self) -> Point:
        """
        Compute the bisector foot from C.

        The bisector foot from C is the point where the angle bisector from C intersects the side AB.

        :return: The bisector foot from C.
        :rtype: Point
        :raises ValueError: If points C, A, and B are the same, bisector foot is undefined.
        """
        CA = self.C.distance_to(self.A)
        CB = self.C.distance_to(self.B)
        if CA + CB == 0:
            raise ValueError("Points C, A, and B are the same, bisector foot is undefined.")
        
        foot_x = (CA * self.B.x + CB * self.A.x) / (CA + CB)
        foot_y = (CA * self.B.y + CB * self.A.y) / (CA + CB)
        return Point(foot_x, foot_y)
    
    def nine_point_center(self) -> Point:
        """
        Compute the nine-point center of the triangle.

        The nine-point center is the midpoint of the line segment connecting the circumcenter and the orthocenter.

        :return: The nine-point center of the triangle.
        :rtype: Point
        :raises ValueError: If points A, B, and C are the same, nine-point center is undefined.
        """
        O = self.circumcenter()
        H = self.orthocenter()
        return Point((O.x + H.x) / 2, (O.y + H.y) / 2)
    
    def nine_point_radius(self) -> Point:
        """
        Compute the radius of the nine-point circle.

        :return: The radius of the nine-point circle.
        :rtype: float
        """
        return self.circumradius() / 2
    
    def nine_point_circle(self) -> Circle:
        """
        Compute the nine-point circle of the triangle.

        :return: The nine-point circle of the triangle.
        :rtype: Circle
        """
        return Circle(self.nine_point_center(), self.nine_point_radius())
    
    def euler_line(self) -> Line:
        """
        Compute the Euler line of the triangle.

        The Euler line is the line through the circumcenter, the centroid, and the orthocenter.

        :return: The Euler line of the triangle.
        :rtype: Line
        """
        O = self.circumcenter()
        G = self.centroid()
        return Line(O, G)

    def excenter_A(self) -> Point:
        """
        Compute the excenter of triangle ABC relative to vertex A.

        The excenter of triangle ABC relative to vertex A is the point where the bisector of angle A intersects the circumcircle of triangle ABC.

        :return: The excenter of triangle ABC relative to vertex A.
        :rtype: Point
        :raises ValueError: If points A, B, and C are the same, excenter is undefined.
        """
        AB = self.A.distance_to(self.B)
        AC = self.A.distance_to(self.C)
        if AB + AC == 0:
            raise ValueError("Points A, B, and C are the same, excenter is undefined.")
        
        excenter_x = (AB * self.C.x - AC * self.B.x) / (AB - AC)
        excenter_y = (AB * self.C.y - AC * self.B.y) / (AB - AC)
        return Point(excenter_x, excenter_y)

    def excenter_B(self) -> Point:
        """
        Compute the excenter of triangle ABC relative to vertex B.

        The excenter of triangle ABC relative to vertex B is the point where the bisector of angle B intersects the circumcircle of triangle ABC.

        :return: The excenter of triangle ABC relative to vertex B.
        :rtype: Point
        :raises ValueError: If points B, A, and C are the same, excenter is undefined.
        """
        BA = self.B.distance_to(self.A)
        BC = self.B.distance_to(self.C)
        if BA + BC == 0:
            raise ValueError("Points B, A, and C are the same, excenter is undefined.")
        
        excenter_x = (BA * self.C.x - BC * self.A.x) / (BA - BC)
        excenter_y = (BA * self.C.y - BC * self.A.y) / (BA - BC)
        return Point(excenter_x, excenter_y)

    def excenter_C(self) -> Point:
        """
        Compute the excenter of triangle ABC relative to vertex C.

        The excenter of triangle ABC relative to vertex C is the point where the bisector of angle C intersects the circumcircle of triangle ABC.

        :return: The excenter of triangle ABC relative to vertex C.
        :rtype: Point
        :raises ValueError: If points C, A, and B are the same, excenter is undefined.
        """
        CA = self.C.distance_to(self.A)
        CB = self.C.distance_to(self.B)
        if CA + CB == 0:
            raise ValueError("Points C, A, and B are the same, excenter is undefined.")
        
        excenter_x = (CA * self.B.x - CB * self.A.x) / (CA - CB)
        excenter_y = (CA * self.B.y - CB * self.A.y) / (CA - CB)
        return Point(excenter_x, excenter_y)

    def angle_A(self) -> float:
        """
        Compute the angle A of the triangle.

        :return: The angle A of the triangle in radians.
        :rtype: float
        :raises ValueError: If the points are collinear, angle A is undefined.
        """
        self._check_degenerate()

        a = self.B.distance_to(self.C)
        b = self.C.distance_to(self.A)
        c = self.A.distance_to(self.B)
        cosA = (b * b + c * c - a * a) / (2 * b * c)
        cosA = max(-1.0, min(1.0, cosA))
        return math.acos(cosA)

    def angle_B(self) -> float:
        """
        Compute the angle B of the triangle.

        :return: The angle B of the triangle in radians.
        :rtype: float
        :raises ValueError: If the points are collinear, angle B is undefined.
        """
        self._check_degenerate()

        a = self.C.distance_to(self.A)
        b = self.A.distance_to(self.B)
        c = self.B.distance_to(self.C)
        cosB = (a * a + c * c - b * b) / (2 * a * c)
        cosB = max(-1.0, min(1.0, cosB))
        return math.acos(cosB)

    def angle_C(self) -> float:
        """
        Compute the angle C of the triangle.

        :return: The angle C of the triangle in radians.
        :rtype: float
        :raises ValueError: If the points are collinear, angle C is undefined.
        """
        self._check_degenerate()

        a = self.A.distance_to(self.B)
        b = self.B.distance_to(self.C)
        c = self.C.distance_to(self.A)
        cosC = (a * a + b * b - c * c) / (2 * a * b)
        cosC = max(-1.0, min(1.0, cosC))
        return math.acos(cosC)

    def is_equilateral(self) -> bool:
        """
        Check if the triangle is equilateral.

        :return: True if the triangle is equilateral, False otherwise.
        :rtype: bool
        """
        return abs(self.A.distance_to(self.B) - self.B.distance_to(self.C)) < EPS and abs(self.B.distance_to(self.C) - self.C.distance_to(self.A)) < EPS
    
    def is_isosceles(self) -> bool:
        """
        Check if the triangle is isosceles.

        :return: True if the triangle is isosceles, False otherwise.
        :rtype: bool
        """
        return (abs(self.A.distance_to(self.B) - self.B.distance_to(self.C)) < EPS or
                abs(self.B.distance_to(self.C) - self.C.distance_to(self.A)) < EPS or
                abs(self.C.distance_to(self.A) - self.A.distance_to(self.B)) < EPS)
    
    def is_scalene(self) -> bool:
        """
        Check if the triangle is scalene.

        A triangle is scalene if all sides have different lengths.

        :return: True if the triangle is scalene, False otherwise.
        :rtype: bool
        """
        return (abs(self.A.distance_to(self.B) - self.B.distance_to(self.C)) > EPS and
                abs(self.B.distance_to(self.C) - self.C.distance_to(self.A)) > EPS and
                abs(self.C.distance_to(self.A) - self.A.distance_to(self.B)) > EPS)
    
    def is_acute(self) -> bool:
        a2 = self.A.distance_to(self.B) ** 2
        """
        Check if the triangle is acute.

        A triangle is acute if all its angles are acute (i.e. less than 90 degrees).

        :return: True if the triangle is acute, False otherwise.
        :rtype: bool
        """
        b2 = self.B.distance_to(self.C) ** 2
        c2 = self.C.distance_to(self.A) ** 2
        return a2 < b2 + c2 - EPS and b2 < a2 + c2 - EPS and c2 < a2 + b2 - EPS
    
    def is_right(self) -> bool:
        """
        Check if the triangle is right.

        A triangle is right if one of its angles is 90 degrees.

        :return: True if the triangle is right, False otherwise.
        :rtype: bool
        """
        a2 = self.A.distance_to(self.B) ** 2
        b2 = self.B.distance_to(self.C) ** 2
        c2 = self.C.distance_to(self.A) ** 2
        return abs(a2 - b2 - c2) < EPS or abs(b2 - a2 - c2) < EPS or abs(c2 - a2 - b2) < EPS
    
    def is_obtuse(self) -> bool:
        """
        Check if the triangle is obtuse.

        A triangle is obtuse if one of its angles is obtuse (i.e. greater than 90 degrees).

        :return: True if the triangle is obtuse, False otherwise.
        :rtype: bool
        """
        a2 = self.A.distance_to(self.B) ** 2
        b2 = self.B.distance_to(self.C) ** 2
        c2 = self.C.distance_to(self.A) ** 2
        return a2 > b2 + c2 + EPS or b2 > a2 + c2 + EPS or c2 > a2 + b2 + EPS
    
    def __str__(self):
        return f"Triangle(A={self.A}, B={self.B}, C={self.C})"
    
    def __repr__(self):
        return f"Triangle(A={self.A}, B={self.B}, C={self.C})"
    
    def __eq__(self, other):
        if isinstance(other, Triangle):
            return set([self.A, self.B, self.C]) == set([self.A2, self.B2, self.C2])
        return NotImplemented
    
    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return NotImplemented
        return not result
