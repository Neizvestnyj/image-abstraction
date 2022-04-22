from image_abstraction import abstract_art as abst, process_image as proc
import cv2 as cv
import argparse

def main():

    # Initialize parser
    parser = argparse.ArgumentParser()

    # Adding optional argument
    parser.add_argument("-f", "--file", default='winter.jpeg', type=str, help="Name of image file in image directory")
    parser.add_argument("-k", "--kclusters", default=5, type=int, help="Number of clusters to quantize image pixel "
                                                                       "colours into")
    parser.add_argument("-o", "--outdim", default="1080x1080", type=str, help="Image dimensions of output image")
    parser.add_argument("-i", "--indim", default=1920, type=int, help="Maximum dimension which input image will be "
                                                                      "reduced to before processing")

    # Read arguments from command line
    args = parser.parse_args()

    # Variable initialization
    file = args.file
    k = args.kclusters  # number of colours to quantize image to
    max_dim = args.indim
    width, height = args.outdim.split('x')
    dim = (int(height), int(width), 3)  # shape of abstract image
    boarder = 0.075  # percent of image outer edge to be a boarder

    # load and colour quantize input image
    img = proc.load_image(file, max_dim)
    img = proc.quantize_img_colours(img, k)

    # show quantized image
    window = 'Quantized Image'
    cv.imshow(window, img)
    cv.waitKey(0)
    cv.destroyAllWindows()

    # generate count of pixels of each colour
    colours = proc.get_colour_counts(img)
    proc.plot_colour_hist(colours)

    abst_img = abst.create_blank_img(dim)
    abst_img = abst.draw_lines(abst_img, boarder, len(colours))

    # show abstract image
    window = 'Abstract Image'
    cv.imshow(window, abst_img)
    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
