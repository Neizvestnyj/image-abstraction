# circle-fractal-generator

Python program that creates a fractal of circles based on various inputs.

Currently only takes images as input. See [docs](./docs/dev.md) for features
under development.

Project created to explore computer generated art.

## Usage

1. Clone repository: `git clone https://github.com/lucas-escobar/circle-fractal-generator`
2. Change directory to root folder of project: `cd /path/to/circle-fractal-generator/`
3. Create virtual environment: `python -m venv /path/to/venv/`
4. Activate environment: `source /path/to/venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Run program: `python main.py`

To change parameters, alter `config.ini`.

Command line `python main.py --help` output:

```
usage: Circle Fractal Generator [-h] [-n NAME] [-k KCLUSTERS] [-o OUTDIM] [-i INDIM]

With image input, a fractal of circles filled with colors relating to the pixels in the image.

options:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Name of image file in the image directory specified in config.ini
  -k KCLUSTERS, --kclusters KCLUSTERS
                        Number of clusters to quantize image pixel colours into
  -o OUTDIM, --outdim OUTDIM
                        Image dimensions of output image
  -i INDIM, --indim INDIM
                        Maximum dimension which input image will be reduced to before processing
```

## Example output

The following is the output of the program with 8 layers of recursion and
input image quantized into 41 colours.

![example output](examples/neon-tokyo-out.png "Title")

The following image was used as input.

![example input](img/neon-tokyo.png)

## How it works

1. The input image is quantized using OpenCV's kmeans clustering algorithm.
2. The pixel counts of each colour is stored in a python dict.
3. A brute force circle packing algorithm is used to generate circle objects.
4. The circle packing function is recursively called on each child circle until
   the desired depth is achieved.
5. All circles are drawn with colour assigned randomly with weights
   proportional to the colour distribution in the input image.
