import numpy as np
import cv2 as cv
import logging
from time import perf_counter

logging.basicConfig(level=logging.INFO)


def load_image(file, max_dim):
    """Loads and resizes image from file"""
    img = cv.imread(f'img/{file}')
    logging.info(f'Image loaded with dimensions: {img.shape}')
    is_too_large = max(img.shape) > max_dim
    if is_too_large:
        h, w, _ = img.shape

        # scale image down to be within dimension constraint
        scale = (max(img.shape)-max_dim) / max(img.shape)
        dim = (int(w * scale), int(h * scale))
        img = cv.resize(img, dim)
        logging.info(f'Image resized to dimensions: {img.shape}')
    return img


def quantize_img_colours(img, k):
    """Uses kmeans algorithm to reduce image to 'k' number of
    colours
    """
    start = perf_counter()
    logging.info(f'Starting image quantization with {k} clusters')

    i = np.float32(img).reshape(-1, 3)
    condition = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, label, center = cv.kmeans(i, k, None, condition, 10,
                                   cv.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    final_img = center[label.flatten()]
    final_img = final_img.reshape(img.shape)
    end = perf_counter()
    logging.info(f'Image quantized in {end-start} seconds')
    return final_img


def get_colour_counts(img):
    """Calculates pixel count of each colour in an image, returns
    dict containing colour-count pairs
    """
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


def plot_colour_hist(colours):
    """Plots histogram of pixel colour distribution of an image"""
    c = [bgr_to_hex(key) for key in colours]
    plt.bar(range(len(colours)), colours.values(), color=c)
    plt.show()


def bgr_to_hex(bgr):
    """Converts BGR 3-tuple to RGBA 4-tuple"""
    b, g, r = bgr
    return '#%02x%02x%02x%02x' % (r, g, b, 255)
