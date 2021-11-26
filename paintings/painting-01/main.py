import math

# imgName = "./images/IMG_0903.jpeg"
imgName = "./images/IMG_0645.jpeg"
# imgName = "./images/IMG_2200.jpeg"
# imgName = "./images/starry_night_full.jpeg"
img = None
min_stroke_length = 5
max_stroke_length = 35
stroke_thickness = 20
noise_scale = 0.005
draw_iterations = 400
color_diff_threshold = 5
frame = 0

def setup():
    global img

    noiseSeed(int(random(1000)))
    background(255)
    img = loadImage(imgName)
    img.loadPixels()
    size(1968, 1476)

def draw():
    global img
    global frame
    global min_stroke_length
    global stroke_thickness

    if (frame > draw_iterations):
        return

    translate(width / 2 - img.width / 2, height / 2 - img.height / 2)

    # The smaller the stroke is the more the spawn count increases to capture more detail.
    count = map(frame, 0, draw_iterations, 10, 800)

    for i in range(0, int(count)):
    
        # Pick a random position on the image.
        x = int(random(img.width))
        y = int(random(img.height))
        
        # Image's pixels is one long list, so we much map our position to an index in order to access that specific pixel.
        index = (y * img.width + x);

        # Get the pixel's color
        pixel = img.pixels[index]

        thickness = map(frame, 0, draw_iterations, stroke_thickness, 0)
        draw_stroke(x, y, pixel, thickness)
    frame += 1


def draw_stroke(x, y, color, stroke_thickness):
    global noise_scale
    global min_stroke_length
    global max_stroke_length

    stroke(color)
    strokeWeight(stroke_thickness)

    push()
    # Translate to the stroke's position
    translate(x, y)

    # Rotate the stroke to a random angle
    n = noise(x * noise_scale, y * noise_scale)
    angle = radians(map(n, 0, 1, -180, 180))
    rotate(angle)

    lengthVariation = random(0.75, 1.25)
    stroke_length = calculate_stroke_length(x, y, angle, color, min_stroke_length, max_stroke_length)

    # Draw the stroke
    line(0, 0, stroke_length, 0)

    # Draw a highlight for more detail
    stroke(min(red(color) * 3, 255), min(green(color) * 3, 255), min(blue(color) * 3, 255), random(100))
    strokeWeight(stroke_thickness * 0.8)
    line(0, -stroke_thickness * 0.15, stroke_length * lengthVariation, -stroke_thickness * 0.15)
    pop()

def calculate_stroke_length(x, y, angle, color, min_stroke_length, max_stroke_length):
    stroke_length = min_stroke_length
    while(stroke_length < max_stroke_length):
        length_x = int(math.floor(stroke_length * cos(angle)))
        length_y = int(math.floor(stroke_length * sin(angle)))
        end_x = max(min(x + length_x, img.width), 0)
        end_y = max(min(y + length_y, img.width), 0)

        # Image's pixels is one long list, so we much map our position to an index in order to access that specific pixel.
        index = int(end_y * img.width + end_x)

        # Get the pixel's color
        pixel = img.pixels[index]

        # Calculate color simularity
        if not color_comparison(color, pixel):
            return stroke_length
        else:
            stroke_length += 1
    return stroke_length

def color_comparison(colorA, colorB):
    global color_diff_threshold
    color_values_a = [red(colorA), blue(colorA), green(colorA)]
    color_values_b = [red(colorB), blue(colorB), green(colorB)]

    return all([a - b < color_diff_threshold for a, b in zip(color_values_a, color_values_b)])
