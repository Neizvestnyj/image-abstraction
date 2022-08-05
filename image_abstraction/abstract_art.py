import numpy as np
import cv2 as cv
from random import randint, random
import math

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND_COLOUR = (137, 142, 140)  # #898E8C - Neutral Gray


def create_blank_img(dim):
    img = np.zeros(dim, dtype=np.uint8)
    img[:] = BACKGROUND_COLOUR
    return img


# assumes square image
def draw_lines(img, boarder, num_colours):
    min_space = 30
    thickness = 3
    h, w, _ = img.shape
    boarder_width = int(h * boarder)  # convert boarder % to pixels

    # create rectangle boarder
    top_left = (boarder_width, boarder_width)
    bottom_right = (w - boarder_width, h - boarder_width)
    cv.rectangle(img, pt1=top_left, pt2=bottom_right, color=WHITE, thickness=thickness)

    for i in range(num_colours):
        left_edge = boarder_width + min_space
        right_edge = h - boarder_width - min_space
        random_col = randint(left_edge, right_edge)

        start_pt = (random_col, boarder_width)
        end_pt = (random_col, h - boarder_width)
        cv.line(img, start_pt, end_pt, color=WHITE, thickness=thickness)

    return img


def draw_circles(img, colours):
    h, w = img.shape[0:2]
    center = (h / 2, w / 2)
    min_dim = min(h, w)
    outer_size = 0.8  # percent of total image dimension to be occupied by outer circle
    inner_size = 0.8  # percent of outer circle to fill with small circles
    outer_radius = outer_size * min_dim
    inner_radius = outer_radius * 0.8
    min_space = 5  # minimum space in pixels between circles

    circles = []

    return_img = cv.circle(img, center=center, radius=outer_radius, color=WHITE, thickness=3)

    for colour, count in colours.items():
        colour_coverage = count / img.size  # percent of total pixels with specified colour

        # random angle from center of image
        alpha = 2 * math.pi * random()

        # random radius from center of image
        r = inner_radius * math.sqrt(random.random())

        # calculating subcircle center
        x = r * math.cos(alpha) + center[0]
        y = r * math.sin(alpha) + center[1]

        # subcircle radius
        sub_r = 3

        return_img = cv.circle(return_img, (x, y), sub_r, color=colour, thickness=-1)

    return return_img
