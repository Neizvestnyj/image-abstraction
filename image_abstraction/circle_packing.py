import math
import random

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Circle:
    def __init__(self, center, radius, subcircles=None):
        self.center = center
        self.radius = radius
        if subcircles is None:
            subcircles = []
        self.subcircles = subcircles


def random_point(circle):
    """Generates uniformly random point within a circle"""
    r = circle.radius * math.sqrt(random.random())
    theta = random.random() * 2 * math.pi

    # Convert to cartesian coordinates
    x = circle.center.x + r * math.cos(theta)
    y = circle.center.y + r * math.sin(theta)
    return Point(int(x), int(y))


def has_intersection(a, b, outside=True):
    """Checks if the parimeter of two circles intersect or touch.

    Args:
        a: first circle object
        b: second circle object
        outside: boolean to indicate that circle a is inside of b
    """
    distance = math.dist(a.center, b.center)
    if outside:
        intersection_occurs = a.radius + b.radius >= distance
    else: # a inside b
        intersection_occurs = b.radius - a.radius <= distance
    return intersection_occurs


# Returns true if the radius of an inner circle can expand without intersecting
# any existing circle or reaching the max radius allowed by user
def can_expand(new_circle, outer_circle, max_radius):
    """

    :param new_circle:
    :param outer_circle:
    :param max_radius:
    :return:
    """
    is_not_max_size = new_circle.radius <= max_radius
    for circle in outer_circle.subcircles:
        intersects_circle = has_intersection(new_circle, circle)
        if intersects_circle:
            break
    intersects_outer_circle = has_intersection(new_circle, outer_circle,
                                                 outside=False)
    return is_not_max_size or intersects_circle or intersects_outer_circle


# Packs circle with specified radius and center with smaller random circles
def pack_circle(outer_circle, num_circles, max_radius):
    for _ in range(num_circles):
        while True:
            center = random_point(outer_circle)
            new_circle = Circle(center, radius=1)
            keep_expanding = can_expand(new_circle, outer_circle, max_radius)
            if keep_expanding:
                break
        while keep_expanding:
            new_circle.radius += 1
            keep_expanding = can_expand(new_circle, outer_circle, max_radius)
        outer_circle.subcircles.append(new_circle)
