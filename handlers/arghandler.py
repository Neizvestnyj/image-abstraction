import argparse
from .confighandler import ConfigHandler 


class ArgHandler:
    """Creates argument parser and processes args"""

    def __init__(self):
        parser = get_parser()
        self.args = parser.parse_args()

    def get_dimensions(self):
        return 


def get_parser() -> argparse.ArgumentParser:
    """Create argparse instance, define arguments, return argparse instance"""
    parser = argparse.ArgumentParser(
        prog='Circle Fractal Generator',
        description="""With image input, a fractal of circles filled with colors
        relating to the pixels in the image."""
    )
    config = ConfigHandler()
    parser.add_argument(
        "-n", "--name", 
        default=config.file_name, 
        type=str,
        help="Name of image file in the image directory specified in config.ini"
    )
    parser.add_argument(
        "-k", "--kclusters", 
        default=config.kclusters, 
        type=int,
        help="Number of clusters to quantize image pixel colours into"
    )
    parser.add_argument(
        "-o", "--outdim", 
        default=config.output_shape, 
        type=str,
        help="Image dimensions of output image"
    )
    parser.add_argument(
        "-i", "--indim", 
        default=config.input_max_edge_length, 
        type=int,
        help="""Maximum dimension which input image will be reduced to before
            processing"""
    )
    return parser