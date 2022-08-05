import math
import random
import cv2 as cv


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Circle:
    def __init__(self, center, radius, child_circles=None):
        self.center = center
        self.radius = radius
        if child_circles is None:
            child_circles = []
        self.child_circles = child_circles

    def draw_circle(self, image, parent_colour=(255, 255, 255),
                    child_colour=(0, 0, 0), child_fill=False):
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
            for c in self.child_circles:  # Draw child circles
                cv.circle(image, (c.center.y, c.center.x), int(c.radius),
                          child_colour, thickness=thickness,
                          lineType=cv.LINE_AA)
        return image


def select_random_colour(colours):
    """Selects random colour from dict containing 3 tuple bgr keys and
    integer count of pixels from image as values

    :param colours: dict of colour-count pairs
    :return: 3-tuple bgr value"""
    # Convert dict values (pixel count) to probability
    total_pixels = sum(colours.values())
    for key, value in colours.items():
        colours[key] = value / total_pixels
    colour = random.choices(
        list(colours.keys()), weights=colours.values(), k=1
    )[0]
    colour = (int(colour[0]), int(colour[1]), int(colour[2]))
    return colour


def random_point(circle):
    """Generates uniformly random point within a circle"""
    radius = circle.radius * math.sqrt(random.random())
    theta = random.random() * 2 * math.pi

    # Convert to cartesian coordinates
    x = circle.center.x + radius * math.cos(theta)
    y = circle.center.y + radius * math.sin(theta)
    return Point(int(x), int(y))


def has_intersection(a, b, epsilon, outside=True):
    """Checks if the parimeter of two circles intersect or touch.

    :param a: first circle object
    :param b: second circle object
    :param epsilon: gap between circles
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


def can_expand(new_circle, parent_circle, max_radius, gap=3):
    """Checks if a circle's radius can be increased by 1 without
    touching an edge of a pre-existing circle
    """
    is_not_max_size = new_circle.radius <= max_radius
    intersects_circle = False
    for circle in parent_circle.child_circles:
        intersects_circle = has_intersection(new_circle, circle, epsilon=gap)
        if intersects_circle:
            break
    intersects_parent_circle = has_intersection(
        new_circle, parent_circle, outside=False, epsilon=gap
    )
    intersection_occurs = intersects_circle or intersects_parent_circle
    return is_not_max_size and not intersection_occurs


def pack_circle(parent_circle, num_circles, max_radius, min_radius=3):
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
            parent_circle.child_circles.append(new_circle)
    return parent_circle


def draw_fractal(
        img, circle, num_circles, max_radius, parent_colour,
        child_colour, max_depth, curr_depth=0
):
    circle = pack_circle(circle, num_circles, circle.radius * max_radius)
    img = circle.draw_circle(img, parent_colour, child_colour, child_fill=True)
    curr_depth += 1
    if curr_depth < max_depth:
        for c in circle.child_circles:
            num_circles -= num_circles * (c.radius / circle.radius)
            draw_fractal(
                img, c, int(num_circles), c.radius * max_radius,
                parent_colour=child_colour, child_colour=parent_colour,
                max_depth=max_depth, curr_depth=curr_depth
            )
    return img


if __name__ == '__main__':  # Testing
    from image_abstraction.test import test_circle_packing as test

    # test.test_random_point(1000)
    # test.test_draw_circle()
    # test.test_pack_circle()
    # test.test_draw_fractal()
    test.test_draw_fractal_dict()
