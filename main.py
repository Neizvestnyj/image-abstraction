from handlers import ImageHandler
import display


def main():
    image = ImageHandler()
    display.display_fractal(image)


if __name__ == '__main__':
    main()
