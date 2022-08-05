from image_abstraction import abstract_art as abst, process_image as proc
import cv2 as cv
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file", default='winter.jpeg', type=str,
        help="Name of image file in image directory"
    )
    parser.add_argument(
        "-k", "--kclusters", default=5, type=int,
        help="Number of clusters to quantize image pixel colours into"
    )
    parser.add_argument(
        "-o", "--outdim", default="1080x1080", type=str,
        help="Image dimensions of output image"
    )
    parser.add_argument(
        "-i", "--indim", default=1920, type=int,
        help="Maximum dimension which input image will be reduced to before "
             "processing"
    )
    args = parser.parse_args()
    width, height = args.outdim.split('x')
    dim = (int(height), int(width), 3)  # shape of abstract image

    # load and colour quantize input image
    img = proc.load_image(args.file, args.indim)
    img = proc.quantize_img_colours(img, args.kclusters)

    # show quantized image
    window = 'Quantized Image'
    cv.imshow(window, img)
    cv.waitKey(0)
    cv.destroyAllWindows()

    colours = proc.get_colour_counts(img)
    proc.plot_colour_hist(colours)

    window = 'Abstract Image'
    cv.imshow(window, abst_img)
    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
