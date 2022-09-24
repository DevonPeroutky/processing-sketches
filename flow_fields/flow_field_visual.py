"""
Simple visualization of a FlowField.
"""

step_size = 20
seed = 0
zOffset = 0


def setup():
    size(500, 500)
    frameRate(24)


def draw():
    global zOffset

    background(255)
    xOffset = seed
    for x in range(width):
        yOffset = seed
        for y in range(height):
            if (y % step_size == 0 and x % step_size == 0):
                # println("(" + str(x) + ", " + str(y) + ")")
                angle = noise(xOffset, yOffset, zOffset) * PI * 2
                drawVector(x, y, step_size / 2, angle)
            yOffset += .005
        xOffset += .005
    zOffset += .05


def drawVector(cx, cy, len, angle):
    pushMatrix()
    translate(cx, cy)
    rotate(angle)
    line(0, 0, len, 0)
    # line(len, 0, len - 3, -3)
    # line(len, 0, len - 3, 3)
    popMatrix()
