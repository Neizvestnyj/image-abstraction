from matplotlib import pyplot as plt
from handlers import ImageHandler, ConfigHandler 
import numpy as np
import circle
import cv2 as cv


def display_fractal(imagehandler: ImageHandler) -> None:
    """Create root circle, calculate colors from quantized image,
    create fractal and display with cv.

    TODO: This function does too much, needs refactoring. Maybe move functions
    to ImageHandler.
    """
    config = ConfigHandler()
    base_image = create_base_image(config.output_image_dimensions)
    width, height, _ = base_image.shape
    c = circle.Circle(
        center=circle.Point(x=int(width / 2), y=int(height / 2)),
        radius=int(width / 2.5)
    )
    image_quantized = imagehandler.get_quantized_image(k=config.kclusters)
    colours = imagehandler.get_colours(image_quantized)
    image = circle.create_fractal(
        img=base_image, 
        circle=c, 
        num_circles=config.num_circles, 
        max_radius=config.max_radius,
        parent_colour=colours,
        child_colour=colours,
        max_depth=config.max_depth
    )
    cv.imshow('Circle Fractal', image)
    cv.waitKey(0)
    cv.destroyAllWindows()


def create_base_image(dimensions: tuple, color: tuple=(0,0,0)):
    """Create solid color image with specified dimensions and color (bgr)"""
    width, height = dimensions
    image = np.zeros((height, width, 3), dtype=np.uint8)
    image[:] = color
    return image 


def plot_colour_hist(colours: dict) -> None:
    """Plots histogram of pixel colour distribution of an image"""
    c = [bgr_to_hex(color) for color in colours]
    plt.bar(range(len(colours)), colours.values(), color=c)
    plt.show()


def bgr_to_hex(bgr: tuple) -> tuple:
    """Converts BGR 3-tuple to RGBA 4-tuple"""
    b, g, r = bgr
    return '#%02x%02x%02x%02x' % (r, g, b, 255)
