import math
import random
import collections
import numpy as np
import cv2 as cv

# generate uniformly random point (x,y) within circle
def random_point(radius, center):

    r = radius * math.sqrt(random.uniform(0, 1))
    theta = random.uniform(0, 1) * 2 * math.pi
    x = center[0] + r * math.cos(theta)
    y = center[1] + r * math.cos(theta)
    Point = collections.namedtuple('Point', ['x', 'y'])

    return Point(x,y)

if __name__ == '__main__':
    from testing import circle_packing_test
    test_random_point()