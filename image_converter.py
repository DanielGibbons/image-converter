import os
import sys
import numpy
from PIL import Image
import argparse


def calculate_pixel_value(red, green, blue, output_colour_space):

    if output_colour_space == "RGB565":
        return (((red >> 3) & 0x1F) << 11) | (((green >> 2) & 0x3F) << 5) | ((blue >> 3) & 0x1F)
    elif output_colour_space == "RGB888":
        return red << 16 | green << 8 | blue


def convert_to_colour_space(image_buffer, colour_space):

    height = image_buffer.shape[0]
    width = image_buffer.shape[1]
    pixel_data = numpy.empty(width * height, dtype=int)
    pixel = 0

    for y in range(0, height):
        for x in range(0, width):
            pixel_data[pixel] = calculate_pixel_value(image_buffer[y][x][0], image_buffer[y][x][1], image_buffer[y][x][2], colour_space)
            pixel += 1
    return pixel_data


def write_data_to_file(filename, colour_space, data, image_width, image_height):

    filename_without_ext, ext = os.path.splitext(filename)
    file_path = "output/" + filename_without_ext + ".c"

    # delete file if it already exists
    if os.path.exists(file_path):
        os.remove(file_path)

    fp = open(file_path, "w+")

    # write file header
    fp. write("/*\r\n")
    fp.write(" *\r\n")
    fp.write(" * Filename: %s.c\r\n" % filename_without_ext)
    fp.write(" * Author: Daniel Gibbons\r\n")
    fp.write(" * Image Width: %d pixels\r\n" % image_width)
    fp.write(" * Image Height: %d pixels\r\n" % image_height)
    fp.write(" * Colour Space: %s\r\n" % colour_space)
    fp.write(" *\r\n")
    fp.write(" */\r\n\r\n")

    # write array declaration
    if colour_space == "RGB565":
        fp.write("const unsigned short[%d] = { \r\n\r\n" % data.size)
    elif colour_space == "RGB888":
        fp.write("const unsigned int[%d] = { \r\n\r\n" % data.size)

    # write data
    for i in range(0, data.size - 1):
        fp.write("%d, " % data[i])
        if i % 50 == 0 and i != 0:
            fp.write("\r\n")
    fp.write("%d \r\n\r\n};" % data[data.size - 1])
    fp.close()


def main(filename, colour_space):

    # check if input is bitmap
    if not filename.lower().endswith('.bmp'):
        sys.exit("Error: Input file not BMP")

    # check valid colour space
    if colour_space != "RGB565" and colour_space != "RGB888":
        sys.exit("Error: Invalid colour space")

    image = Image.open(filename)
    image_buffer = numpy.array(image)

    data = convert_to_colour_space(image_buffer, colour_space)

    write_data_to_file(filename, colour_space, data, image_buffer.shape[1], image_buffer.shape[0])

    print("Image conversion complete.")


if __name__ == "__main__":

    numpy.set_printoptions(threshold=numpy.inf)

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Converts a 24-Bit BMP to either RGB565 or RGB888 for use in embedded application')
    parser.add_argument('filename', help='The 24-Bit BMP file to be converted')
    parser.add_argument('colour_space', help='Desired output colour space - RGB565 or RGB888')
    args = parser.parse_args()

    # start conversion
    main(args.filename, args.colour_space)

