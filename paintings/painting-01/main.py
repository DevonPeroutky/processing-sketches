# imgName = "./images/IMG_0903.jpeg"
imgName = "./images/IMG_0645.jpeg"
# imgName = "./images/IMG_2200.jpeg"
# imgName = "./images/starry_night_full.jpeg"
img = None
strokeLength = 35
strokeThickness = 20
noiseScale = 0.005
drawIterations = 250
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
    global strokeLength
    global strokeThickness

    if (frame > drawIterations):
        return

    translate(width / 2 - img.width / 2, height / 2 - img.height / 2)

    # The smaller the stroke is the more the spawn count increases to capture more detail.
    count = map(frame, 0, drawIterations, 10, 800)
    print(count)

    for i in range(0, int(count)):
    
        # Pick a random position on the image.
        x = int(random(img.width))
        y = int(random(img.height))
        
        # Image's pixels is one long list, so we much map our position to an index in order to access that specific pixel.
        index = (y * img.width + x);

        # Get the pixel's color
        pixel = img.pixels[index]

        thickness = map(frame, 0, drawIterations, strokeThickness, 0)
        # length = map(frame, 0, drawIterations, 10, strokeLength)
        length = strokeLength
        
        draw_stroke(x, y, pixel, thickness, length)
    frame += 1


def draw_stroke(x, y, color, strokeThickness, strokeLength):
    global noiseScale

    stroke(color);
    strokeWeight(strokeThickness);

    push()
    # Translate to the stroke's position
    translate(x, y)

    # Rotate the stroke to a random angle
    n = noise(x * noiseScale, y * noiseScale)
    rotate(radians(map(n, 0, 1, -180, 180)))

    lengthVariation = random(0.75, 1.25)

    # Draw the stroke
    line(0, 0, strokeLength * lengthVariation, 0)

    # Draw a highlight for more detail
    stroke(min(red(color) * 3, 255), min(green(color) * 3, 255), min(blue(color) * 3, 255), random(100))
    strokeWeight(strokeThickness * 0.8)
    line(0, -strokeThickness * 0.15, strokeLength * lengthVariation, -strokeThickness * 0.15)
    pop()
