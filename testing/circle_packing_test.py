import cv2 as cv
import numpy as np
import sys
from image_abstraction import circle_packing

def test_random_point(num):

    # create white blank image
    img = np.zeros((1000, 1000, 3), dtype=np.uint8)
    img[:] = (255, 255, 255)

    radius = 500
    center = circle_packing.Point(500, 500)
    circle = circle_packing.Circle(center, radius)

    for i in range(num):
        point = circle_packing.random_point(circle)
        img[point.x, point.y] = (0, 0, 0)

    cv.imshow('Random Points in Circle', img)
    cv.waitKey(0)
    cv.destroyAllWindows()

