# Image Converter

### Description

Scripts to create .h and .c for embedded graphics applications from Bitmaps, PNGs and JPEGs without alpha channels

Source files can be generated to use the RGB565 or RGB888 colour spaces and when generated are located in the "output / filename_wihout_extension + "_current_time" /" directory


### Using the scripts

#### image_converter.py

Run " python image_converter.py "filename" "colour_space" " where filename is the relative path to the image and the "colour_space" is either "RGB565" or "RGB888".

#### batch_conversion.py

Run " python batch_conversion.py "colour_space" " where "colour_space" is either "RGB565" or "RGB888". This will generate .h and .c files in  output/ for all images in images/ directory.
