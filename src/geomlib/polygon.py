from geomlib.point import Point
import math

class Polygon:
    __slots__ = ['points']

    def __init__(self, points: list[Point]):
        self.points = points

    def convex_hull(self) -> 'Polygon':
        """
        Compute the convex hull of the polygon.

        The convex hull is the smallest convex polygon that contains all the points of the polygon.

        :return: A new polygon representing the convex hull of the original polygon.
        :rtype: Polygon
        """
        if len(self.points) < 3:
            return Polygon(self.points.copy())

        pts = sorted(self.points)

        lower: list[Point] = []
        for p in pts:
            while len(lower) >= 2 and lower[-2].cross3(lower[-1], p) <= 0:
                lower.pop()
            lower.append(p)

        upper: list[Point] = []
        for p in reversed(pts):
            while len(upper) >= 2 and upper[-2].cross3(upper[-1], p) <= 0:
                upper.pop()
            upper.append(p)

        return Polygon(lower[:-1] + upper[:-1])
    
    def diameter(self) -> tuple[Point, Point]:
        """
        Compute the diameter of the polygon.

        The diameter is the longest distance between any two points of the polygon.

        :return: A tuple containing the two points that are furthest apart.
        :rtype: tuple[Point, Point]
        """
        hull = self.convex_hull().points
        n = len(hull)

        if n == 0:
            return None
        if n == 1:
            return hull[0], hull[0]
        if n == 2:
            return hull[0], hull[1]

        j = 1
        best_dist = 0
        best_pair = (hull[0], hull[1])

        for i in range(n):
            ni = (i + 1) % n

            while abs((hull[ni] - hull[i]).cross(hull[(j + 1) % n] - hull[i])) > \
                abs((hull[ni] - hull[i]).cross(hull[j] - hull[i])):
                j = (j + 1) % n

            d = hull[i].distance_to(hull[j])
            if d > best_dist:
                best_dist = d
                best_pair = (hull[i], hull[j])

        return best_pair

    def point_in_convex_polygon(self, p: Point) -> bool:
        """
        Check if a point is inside a convex polygon.

        This function uses the Bary- Centric formula to check if a point is inside a convex polygon.
        A point is considered to be inside the polygon if it is on the border or to the left of an edge.

        :param p: The point to check.
        :type p: Point
        :return: True if the point is inside the polygon, False otherwise.
        :rtype: bool
        """
        
        hull = self.points
        n = len(hull)

        if n < 3:
            return False

        if hull[0].cross3(hull[1], p) < 0:
            return False
        if hull[0].cross3(hull[-1], p) > 0:
            return False

        l, r = 1, n - 1
        while r - l > 1:
            mid = (l + r) // 2
            if hull[0].cross3(hull[mid], p) >= 0:
                l = mid
            else:
                r = mid

        return hull[l].cross3(hull[l + 1], p) >= 0
    
    def minimum_bounding_rectangle(self) -> tuple[float, float, float, float, float] | None:
        """
        Compute the minimum bounding rectangle of a convex polygon.

        The minimum bounding rectangle is the rectangle with the smallest area that fully contains the polygon.
        The function returns a tuple of five floats representing the minimum bounding rectangle: the minimum x-coordinate, the maximum x-coordinate, the minimum y-coordinate, the maximum y-coordinate and the angle of rotation of the rectangle.

        :return: A tuple of five floats representing the minimum bounding rectangle, or None if the input polygon has less than three vertices.
        :rtype: tuple[float, float, float, float, float] | None
        """
        hull = self.convex_hull()
        n = len(hull)

        if n <= 2:
            return None

        best_area = float("inf")
        best_rect = None

        for i in range(n):
            p1 = hull[i]
            p2 = hull[(i + 1) % n]

            dx = p2.x - p1.x
            dy = p2.y - p1.y
            angle = -math.atan2(dy, dx)

            cos = math.cos(angle)
            sin = math.sin(angle)

            xs = []
            ys = []

            for p in hull:
                x = p.x * cos - p.y * sin
                y = p.x * sin + p.y * cos
                xs.append(x)
                ys.append(y)

            minx, maxx = min(xs), max(xs)
            miny, maxy = min(ys), max(ys)

            area = (maxx - minx) * (maxy - miny)

            if area < best_area:
                best_area = area
                best_rect = (minx, maxx, miny, maxy, angle)

        return best_rect

    def signed_area(self) -> float:
        """
        Compute the signed area of a polygon.

        The signed area of a polygon is positive if the vertices are ordered in a counterclockwise direction, and negative if the vertices are ordered in a clockwise direction.

        :return: The signed area of the polygon.
        :rtype: float
        """
        area = 0
        n = len(self.points)

        for i in range(n):
            j = (i + 1) % n
            p, q = self.points[i], self.points[j]
            area += p.x * q.y - q.x * p.y

        return area / 2
    
    def area(self) -> float:
        """
        Compute the area of a polygon.

        The area of a polygon is positive if the vertices are ordered in a counterclockwise direction, and negative if the vertices are ordered in a clockwise direction.

        :return: The area of the polygon.
        :rtype: float
        """
        return abs(self.signed_area())
    
    def append(self, point: Point):
        """
        Append a point to the polygon.

        :param point: The point to append.
        :type point: Point
        """
        self.points.append(point)

    def insert(self, index: int, point: Point):
        """
        Insert a point at the specified index in the polygon.

        :param index: The index to insert the point at.
        :type index: int
        :param point: The point to insert.
        :type point: Point
        """
        self.points.insert(index, point)
    
    def remove(self, point: Point):
        """
        Remove the first occurrence of a point in the polygon.

        :param point: The point to remove.
        :type point: Point
        """
        self.points.remove(point)

    def pop(self, index: int = -1):
        """
        Remove and return the point at the specified index in the polygon.

        If index is not provided, remove and return the last point in the polygon.

        :param index: The index of the point to remove.
        :type index: int
        :return: The point at the specified index.
        :rtype: Point
        """
        return self.points.pop(index)
    
    def clear(self):
        """
        Clear the polygon by removing all points.

        :return: None
        :rtype: NoneType
        """
        self.points.clear()

    def copy(self):
        """
        Return a shallow copy of the polygon.

        :return: A new Polygon object which is a shallow copy of the original polygon.
        :rtype: Polygon
        """
        return Polygon(self.points.copy())
    
    def count(self, point: Point):
        """
        Count the number of occurrences of a point in the polygon.

        :param point: The point to count.
        :type point: Point
        :return: The number of occurrences of the point in the polygon.
        :rtype: int
        """
        return self.points.count(point)
    
    def index(self, point: Point):
        """
        Return the index of the first occurrence of a point in the polygon.

        :param point: The point to find.
        :type point: Point
        :return: The index of the point in the polygon.
        :rtype: int
        :raises ValueError: If the point is not in the polygon.
        """
        return self.points.index(point)
    
    def reverse(self):
        """
        Reverse the order of the points in the polygon.

        :return: None
        :rtype: NoneType
        """
        self.points.reverse()

    def sort(self, key=None, reverse=False):
        """
        Sort the points in the polygon.

        :param key: A function of one argument that is used to extract a comparison key from each input element.
        :type key: callable
        :param reverse: If set to True, then the list elements are sorted as if each comparison were reversed.
        :type reverse: bool
        :return: None
        :rtype: NoneType
        """
        self.points.sort(key=key, reverse=reverse)

    def sort_ccw(self):
        """
        Sort the points in the polygon counterclockwise.

        The points are sorted based on the angle between the line connecting the point and the centroid of the polygon, and the x-axis.

        The centroid is calculated as the average of the x and y coordinates of all the points in the polygon.

        If the polygon has less than 3 points, the function does nothing.

        :return: None
        :rtype: NoneType
        """
        if len(self.points) < 3:
            return

        cx = sum(p.x for p in self.points) / len(self.points)
        cy = sum(p.y for p in self.points) / len(self.points)

        def angle(p: Point):
            return math.atan2(p.y - cy, p.x - cx)

        self.points.sort(key=angle)

    def __str__(self):
        return f"Polygon({self.points})"
    
    def __repr__(self):
        return f"Polygon({self.points})"
    
    def __eq__(self, other):
        return self.points == other.points
    
    def __ne__(self, other):
        return not self == other
    
    def __hash__(self):
        return hash(tuple(self.points))
    
    def __len__(self):
        return len(self.points)
    
    def __getitem__(self, index: int):
        return self.points[index]
    
    def __setitem__(self, index: int, value: Point):
        self.points[index] = value

    def __iter__(self):
        return iter(self.points)
    
    def __reversed__(self):
        return reversed(self.points)
    
    def __contains__(self, point: Point):
        return point in self.points
    