import process_image as proc
import abstract_art as abst
import cv2 as cv


def main():

    file = 'spring.jpeg'

    k = 15  # number of colours to quantize image to
    dim = (3000, 3000, 3)  # shape of abstract image
    boarder = 0.075  # percent of image outer edge to be a boarder

    # load and process input image
    img = proc.load_image(file)
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
