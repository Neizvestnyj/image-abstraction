import numpy as np
import cv2 as cv
import os
import logging
import time
from .confighandler import ConfigHandler


logging.basicConfig(level=logging.INFO)


class ImageHandler:
    """Load cv2.Mat image, apply algorithms, and get statistics."""

    def __init__(self):
        config = ConfigHandler()
        self.image = load_image(config.file_name, config.input_max_edge_length)

    def get_quantized_image(self, k: int) -> cv.Mat:
        return quantize_img_colours(self.image, k)

    def show_quantized_image(image: cv.Mat, k: int) -> None:
        cv.imshow(winname='Quantized', 
                mat=image.get_quantized_image(k=k)
                )
        cv.waitKey(0)
        cv.destroyAllWindows()

    def get_colours(self, image: cv.Mat=None) -> dict:
        if image is None:
            colors = create_colours_dict(self.image)
        else:
            colors = create_colours_dict(image)
        return colors
        


def load_image(file_name: str, dimension_limit: int) -> cv.Mat:
    """Load image from a file. 
    
    Resizes image if an edge length exceeds the specified limit.
    """
    image_path = os.getcwd() + '/img/' + file_name
    image = cv.imread(image_path)
    logging.info(f'Image loaded with dimensions: {image.shape}')
    if max(image.shape) > dimension_limit:
        image = scale_down(image, dimension_limit)
        logging.info(f'Image resized to dimensions: {image.shape}')
    return image


def scale_down(image: cv.Mat, dimension_constraint: int) -> cv.Mat:
    """Scale image to specified dimension constraint.
    
    Returns scaled down image with the maximum edge length of dimension_limit.

    FIXME: 
        Desired output: Matrix with max edge length equal to long_edge_length
                        with aspect ratio maintained
        Current output: Matrix with max edge length scaled down by 
                        factor based on dimension_constraint
    """
    height, width, *_ = image.shape
    long_edge_length = max(height, width)
    scale = (long_edge_length - dimension_constraint) / long_edge_length 
    target_dimensions = (int(width * scale), int(height * scale))
    return cv.resize(image, target_dimensions)


def quantize_img_colours(img: cv.Mat, k: int) -> cv.Mat:
    """Reduce number of colors in an image using kmeans."""
    start = time.perf_counter()
    logging.info(f'Starting image quantization with {k} clusters')
    i = np.float32(img).reshape(-1, 3)
    condition = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    *_, label, center = cv.kmeans(data=i, 
                                  K=k,
                                  bestLabels=None, 
                                  criteria=condition, 
                                  attempts=10,
                                  flags=cv.KMEANS_RANDOM_CENTERS
    )
    center = np.uint8(center)
    final_img = center[label.flatten()]
    final_img = final_img.reshape(img.shape)
    end = time.perf_counter()
    logging.info(f'Image quantized in {end - start} seconds')
    return final_img


def create_colours_dict(img: cv.Mat) -> dict:
    """Calculate count of each unique color in an image.
    
    Returns dict {"color": tuple, "count": int}
    """
    start = time.perf_counter()
    logging.info('Getting pixel colour counts')
    if len(img.shape) != 3:
        raise ValueError(f'Incorrect image shape, should be [height, width, channels].\
            Shape provided is {img.shape}')
    height, width, _ = img.shape
    colours = {}
    for row in range(height):
        for col in range(width):
            colour = tuple(img[row, col])
            if colour in colours:
                colours[colour] += 1
            else:
                colours[colour] = 1
    end = time.perf_counter()
    logging.info(f'Image pixels counted in {end - start} seconds')
    return colours
