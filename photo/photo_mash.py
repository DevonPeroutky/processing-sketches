# importing sys
import sys
  
# sys.path.append('/Users/devonperoutky/Development/processing/utilities/color')
sys.path.append('/Users/devonperoutky/Development/processing/utilities')
print(sys.path)

from math import sqrt
from color.color_diff import calc_pixel_color_distance

image_names = ["../images/IMG_0903.jpeg", "../images/IMG_0645.jpeg", "../images/IMG_2200.jpeg", "../images/starry_night_full.jpeg", "../images/working-mount-tam.jpeg"]
images = None

def setup():
    global images
    size(1000, 1000)
    print(image_names)
    images = [loadImage(image) for image in image_names]
    for image in images:
        image.loadPixels()
    noLoop()

def draw():
    global images
    # 1. Initialize a grid of squares
    # 2. For initial square --> Chose random photo
    # 3. Set pixels of square to be the chosen photo
    # 4. for each nearby squre --> Set the square's pixels to be the pixels of the photo whose corresponding square is more similar in color
    reference_pixel = color(random(256), random(256), random(256))
    print("REFERENCE COLOR ({}, {}, {})".format(red(reference_pixel), green(reference_pixel), blue(reference_pixel)))
    border_thickness = 20

    loadPixels()
    for x in range(width):
        for y in range(height):
            index = y * width + x
            #r if x < border_thickness or y < border_thickness or x > width - border_thickness or y > height - border_thickness:
            #     pixels[index] = reference_pixel
            # else:
            selected_pixel = select_random_pixel(x, y)
            # selected_pixel = select_most_similar_pixel(x, y, reference_pixel)
            # reference_pixel = selected_pixel
            pixels[index] = selected_pixel
    updatePixels()
    print("DONE!")


def select_random_pixel(x, y):
    global images

    # Select Image
    rand = int(random(len(images)))
    # rand = 0
    random_image = images[rand]

    image_index = y * random_image.width + x
    return random_image.pixels[image_index]

def select_most_similar_pixel(x, y, reference_pixel):
    global images
    candidate_pixels = [select_pixel_from_image(img, x, y) for img in images]
    pixel_distances = [calc_pixel_color_distance(image_pixel, reference_pixel) for image_pixel in candidate_pixels]
    most_similar_pixel_index = pixel_distances.index(min(pixel_distances))
    return candidate_pixels[most_similar_pixel_index]

def select_pixel_from_image(image, x, y):
    image_index = y * image.width + x
    return image.pixels[image_index]

