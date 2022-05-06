import cv2 as cv
import numpy as np
import sys
from image_abstraction.circle_packing import Point, Circle, random_point, \
    pack_circle, draw_fractal


def test_random_point(num):
    # create white blank image
    img = np.zeros((1000, 1000, 3), dtype=np.uint8)
    img[:] = (255, 255, 255)
    radius = 500
    center = Point(500, 500)
    circle = Circle(center, radius)
    for i in range(num):
        point = random_point(circle)
        img[point.x, point.y] = (0, 0, 0)
    cv.imshow('Random Points in Circle', img)
    cv.waitKey(0)
    cv.destroyAllWindows()

def test_draw_circle():
    img = np.zeros((1000, 800, 3), dtype=np.uint8)
    img[:] = (255, 255, 255)
    w, h, _ = img.shape
    center = Point(x=int(w / 2), y=int(h / 2))
    radius = int(w / 4)
    circle = Circle(center, radius)
    img = circle.draw_circle(img)
    cv.imshow('Draw circles test', img)
    cv.waitKey(0)
    cv.destroyAllWindows()

def test_pack_circle():
    img = np.zeros((1000, 1000, 3), dtype=np.uint8)
    img[:] = (0, 0, 0)
    w, h, _ = img.shape
    center = Point(x=int(w / 2), y=int(h / 2))
    radius = int(w / 3)
    circle = Circle(center, radius)
    circle = pack_circle(circle, num_circles=5000, max_radius=radius*0.80)
    img = circle.draw_circle(img, child_colour=(0, 0, 0), child_fill=True)
    for c in circle.child_circles:
        c = pack_circle(c, num_circles=1000, max_radius=radius*0.5)
        img = c.draw_circle(
            img, parent_colour=(0,0,0), child_colour=(255,255,255),
            child_fill=True
        )
    cv.imshow('Circle packing test', img)
    cv.waitKey(0)
    cv.destroyAllWindows()

def test_draw_fractal():
    img = np.zeros((1080, 1080, 3), dtype=np.uint8)
    img[:] = (0, 0, 0)
    w, h, _ = img.shape
    center = Point(x=int(w / 2), y=int(h / 2))
    radius = int(w / 2.5)
    circle = Circle(center, radius)
    img = draw_fractal(
        img, circle, num_circles=20, max_radius=0.75,
        parent_colour=(237,220,35),
        child_colour=(35,133,237),
        max_depth=2
    )
    cv.imshow('Circle fractal test', img)
    cv.waitKey(0)
    cv.destroyAllWindows()
    cv.imwrite("circle-fractal.png", img)
