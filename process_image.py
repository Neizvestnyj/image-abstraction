import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import glob
import logging
from time import perf_counter

logging.basicConfig(level=logging.INFO)


def load_image(file):
    img = cv.imread(f'images/{file}')
    logging.info(f'Image loaded with shape {img.shape}')
    return img

# Uses kmeans algorithm to reduce image to 'k' number of colours
def quantize_img_colours(img, k):

    start = perf_counter()
    logging.info(f'Starting image quantization with {k} clusters')

    i = np.float32(img).reshape(-1, 3)
    condition = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    ret, label, center = cv.kmeans(i, k, None, condition, 10, cv.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    final_img = center[label.flatten()]
    final_img = final_img.reshape(img.shape)

    end = perf_counter()
    logging.info(f'Image quantized in {end-start} seconds')

    return final_img

# returns pixel count of each colour within an image
def get_colour_counts(img):

    start = perf_counter()
    logging.info('Getting pixel colour counts')

    h, w, _ = img.shape
    colours = {}

    for row in range(h):
        for col in range(w):

            colour = tuple(img[row, col])

            if colour in colours:
                colours[colour] += 1

            else:
                colours[colour] = 1

    end = perf_counter()
    logging.info(f'Image pixels counted in {end-start} seconds')

    return colours

# plots histogram of pixel colour distribution of an image.
def plot_colour_hist(colours):

    c = [bgr_to_hex(key) for key in colours]
    plt.bar(range(len(colours)), colours.values(), color=c)
    plt.show()


# returns 4-tuple in RGB hex format
# input 3-tuple in BGR format (int)
def bgr_to_hex(bgr):
    b, g, r = bgr
    return '#%02x%02x%02x%02x' % (r, g, b, 255)