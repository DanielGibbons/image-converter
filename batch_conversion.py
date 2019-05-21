import image_converter
import glob
import argparse


if __name__ == "__main__":

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Converts all images in images/ to either RGB565 or RGB888 for use in an embedded application')
    parser.add_argument('colour_space', help='Desired output colour space - RGB565 or RGB888')
    args = parser.parse_args()

    for filename in glob.glob("images/*"):
        image_converter.main(filename, args.colour_space)
