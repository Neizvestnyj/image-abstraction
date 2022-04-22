from image_abstraction import circle_packing
import cv2 as cv
import numpy as np

def test_random_point():
    img = np.zeros(dim, dtype=np.uint8)
    img[:] = BACKGROUND_COLOUR