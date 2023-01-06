from __future__ import annotations
import configparser
import os


class ConfigHandler:
    """Accesses and manages data from config.ini"""

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        print(os.getcwd())
        self.file_name = config['ArgDefaults']['file_name']
        self.kclusters = int(config['ArgDefaults']['kclusters'])
        self.output_image_dimensions = split_wxh_string(config['ArgDefaults']['output_image_dimensions'])
        self.input_max_edge_length = int(config['ArgDefaults']['input_max_edge_length'])
        self.image_path = config['Paths']['image_path']
        self.num_circles = int(config['FractalParameters']['num_circles'])
        self.max_radius = float(config['FractalParameters']['max_radius'])
        self.min_radius = int(config['FractalParameters']['min_radius'])
        self.max_depth = int(config['FractalParameters']['max_depth'])
        self.gap = int(config['FractalParameters']['gap'])


def split_wxh_string(string: str) -> tuple:
    width, height = string.split('x')
    return (int(width), int(height))