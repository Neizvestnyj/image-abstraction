from __future__ import annotations
import math
import random
import cv2 as cv
from handlers import ConfigHandler


config = ConfigHandler()


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Circle:

    def __init__(self, center: Point, radius: Point, 
                 children: list[Circle]=None
                ):
        self.center = center
        self.radius = radius
        if children is None: children = []
        self.children = children 


    def draw_circle(self, 
                    image: cv.Mat,
                    parent_colour: tuple=(255, 255, 255),
                    child_colour: tuple=(0, 0, 0),
                    child_fill: bool=False
                    ) -> cv.Mat:
        """Draws the circle passed as a parameter and all child circles
        associated with its class attribute.

        :param image: NumPy image on which the circles are to be drawn
        :param colour: RGB tuple representing the outline colour of the
            circles
        :return: NumPy image with circles drawn on it
        """
        # Draw parent circle
        if isinstance(parent_colour, dict):
            parent_colour = select_random_colour(parent_colour)
        cv.circle(image, (self.center.y, self.center.x), int(self.radius),
                  parent_colour, thickness=-1, lineType=cv.LINE_AA)
        if self.radius > 2:
            if isinstance(child_colour, dict):
                child_colour = select_random_colour(child_colour)
            thickness = -1 if child_fill else 1
            for c in self.children:  # Draw child circles
                cv.circle(image, (c.center.y, c.center.x), int(c.radius),
                          child_colour, thickness=thickness,
                          lineType=cv.LINE_AA)
        return image


def pack_circle(parent_circle: Circle,
                num_circles: Circle, 
                max_radius: int,
                min_radius: int=config.min_radius
                ) -> Circle:
    """Fills the child_circles attribute of the parent_circle with
    randomly placed circles.

    :param parent_circle: Circle to be filled
    :param num_circles: Number of randomly placed circles to fill the
        parent circle
    :param max_radius: The max radius a generated child circle can have
    :param min_radius: The min radius a generated child circle can have
    :return: Copy of parent_circle with filled child_circles attribute
    """
    max_attempts_reached = False
    max_attempts = int(num_circles * 0.75)
    for _ in range(num_circles):
        attempt_count = 0
        while True:
            center = random_point(parent_circle)
            new_circle = Circle(center, radius=min_radius)
            keep_expanding = can_expand(new_circle, parent_circle, max_radius)
            if keep_expanding or max_attempts_reached:
                break
            attempt_count += 1
            max_attempts_reached = attempt_count >= max_attempts
        while keep_expanding:
            new_circle.radius += 1
            keep_expanding = can_expand(new_circle, parent_circle, max_radius)
        if not max_attempts_reached:
            parent_circle.children.append(new_circle)
    return parent_circle


def select_random_colour(colours: dict) -> dict:
    """Selects random colour from dict containing 3 tuple bgr keys and
    integer count of pixels from image as values

    :param colours: dict {"color": 3-tuple, "count": int} 
    :return: 3-tuple (B, G, R) 
    """
    for color, count in colours.items():
        probability = count / sum(colours.values()) 
        colours[color] = probability
    colour = random.choices(
        population=list(colours.keys()), 
        weights=colours.values(), 
        k=1
    )[0]
    colour = (int(colour[0]), int(colour[1]), int(colour[2]))
    return colour


def random_point(circle: Circle) -> Point:
    """Generates uniformly random point within a circle as coordinates (x,y)"""
    radius = circle.radius * math.sqrt(random.random())
    theta = random.random() * 2 * math.pi
    x = circle.center.x + radius * math.cos(theta)
    y = circle.center.y + radius * math.sin(theta)
    return Point(int(x), int(y))


def has_intersection(a: Circle, b: Circle, epsilon: int, outside: bool=True):
    """Checks if the parimeter of two circles intersect or touch.

    :param a: first circle object
    :param b: second circle object
    :param epsilon: pixel gap between circles
    :param outside: boolean to indicate that circle a is inside of b
    :return: True if intersection occurs
    """
    distance = math.dist((a.center.x, a.center.y),
                         (b.center.x, b.center.y))
    if outside:
        intersection_occurs = a.radius + b.radius >= distance - epsilon
    else:  # a inside b
        intersection_occurs = b.radius - a.radius <= distance + epsilon
    return intersection_occurs


def can_expand(new_circle, parent_circle, max_radius, gap=config.gap):
    """Checks if a circle's radius can be increased by 1 without
    touching an edge of a pre-existing circle
    """
    is_not_max_size = new_circle.radius <= max_radius
    intersects_circle = False
    for circle in parent_circle.children:
        intersects_circle = has_intersection(new_circle, circle, epsilon=gap)
        if intersects_circle:
            break
    intersects_parent_circle = has_intersection(
        new_circle, parent_circle, outside=False, epsilon=gap
    )
    intersection_occurs = intersects_circle or intersects_parent_circle
    return is_not_max_size and not intersection_occurs


def create_fractal(
        img: cv.Mat, circle: Circle, num_circles: int, max_radius: int, 
        parent_colour: tuple, child_colour: tuple, max_depth: int, 
        curr_depth: int=0
) -> cv.Mat:
    """Recursively occupies the child_circles: list[Circle] attribute of a
    Circle
    """
    circle = pack_circle(circle, num_circles, circle.radius * max_radius)
    img = circle.draw_circle(img, parent_colour, child_colour, child_fill=True)
    curr_depth += 1
    if curr_depth < max_depth:
        for c in circle.children:
            num_circles -= num_circles * (c.radius / circle.radius)
            create_fractal(
                img, c, int(num_circles), c.radius * max_radius,
                parent_colour=child_colour, child_colour=parent_colour,
                max_depth=max_depth, curr_depth=curr_depth
            )
    return img
