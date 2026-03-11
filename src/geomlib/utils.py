from geomlib.vector import Vector
from geomlib.point import Point
import numpy as np

def cross_product(vo: Vector, va: Vector, vb: Vector) -> float:
    """
    Compute the cross product of two vectors (va, vb) with respect to the vector origin (vo).

    The cross product is positive if vb is to the left of va (counter-clockwise direction),
    negative if vb is to the right of va (clockwise direction), and zero if va and vb are collinear.

    :param vo: The origin vector.
    :type vo: Vector
    :param va: The first vector.
    :type va: Vector
    :param vb: The second vector.
    :type vb: Vector
    :return: The cross product of the vectors va and vb with respect to the vector origin vo.
    :rtype: float
    """
    return (va.x - vo.x) * (vb.y - vo.y) - (va.y - vo.y) * (vb.x - vo.x)

def is_collinear(p1: Point, p2: Point, p3: Point) -> bool:
    """
    Checks if three points are collinear.

    The points are collinear if the cross product of the vectors formed by the points is zero.

    :param p1: The first point.
    :type p1: Point
    :param p2: The second point.
    :type p2: Point
    :param p3: The third point.
    :type p3: Point
    :return: True if the points are collinear, False otherwise.
    :rtype: bool
    """
    v1 = Vector.from_points(p1, p2)
    v2 = Vector.from_points(p1, p3)
    return v1.cross(v2) == 0

def is_concyclic(p1: Point, p2: Point, p3: Point, p4: Point, return_det: bool = False) -> bool:
    """
    Checks if four points are concyclic.
    If return_det is True, the determinant of the matrix is returned instead.

    Parameters
    ----------
    p1 : Point
        The first point.
    p2 : Point
        The second point.
    p3 : Point
        The third point.
    p4 : Point
        The fourth point.
    return_det : bool, optional
        If True, the determinant of the matrix is returned instead of a boolean, by default False.

    Returns
    -------
    bool or float
        True if the points are concyclic, False otherwise. If return_det is True, the determinant of the matrix is returned instead.
    """
    matrix = [
        [p1.x, p1.y, p1.x ** 2 + p1.y ** 2, 1],
        [p2.x, p2.y, p2.x ** 2 + p2.y ** 2, 1],
        [p3.x, p3.y, p3.x ** 2 + p3.y ** 2, 1],
        [p4.x, p4.y, p4.x ** 2 + p4.y ** 2, 1]
    ]
    
    det = np.linalg.det(matrix)

    if return_det:
        return det
    
    return (
        det == 0 and 
        not is_collinear(p1, p2, p3) and
        not is_collinear(p1, p2, p4) and
        not is_collinear(p1, p3, p4) and
        not is_collinear(p2, p3, p4)
    )


def closest_pair(points: list[Point]):
    """
    Find the closest pair of points in a given list of points.

    The function uses a divide-and-conquer approach to find the closest pair of points in O(n log n) time complexity.

    Parameters
    ----------
    points : list[Point]
        The list of points to find the closest pair in.

    Returns
    -------
    float, tuple[Point, Point]
        A tuple containing the minimum distance between two points and the pair of points that are closest to each other.
    """
    pts = sorted(points, key=lambda p: (p.x, p.y))

    def solve(pts):
        n = len(pts)

        if n <= 3:
            best = float("inf")
            pair = None
            for i in range(n):
                for j in range(i + 1, n):
                    d = pts[i].distance_to(pts[j])
                    if d < best:
                        best = d
                        pair = (pts[i], pts[j])
            return best, pair

        mid = n // 2
        midx = pts[mid].x

        d1, p1 = solve(pts[:mid])
        d2, p2 = solve(pts[mid:])

        d = min(d1, d2)
        pair = p1 if d1 < d2 else p2

        strip = [p for p in pts if abs(p.x - midx) < d]
        strip.sort(key=lambda p: p.y)

        for i in range(len(strip)):
            for j in range(i + 1, min(i + 7, len(strip))):
                dist = strip[i].distance_to(strip[j])
                if dist < d:
                    d = dist
                    pair = (strip[i], strip[j])

        return d, pair

    return solve(pts)