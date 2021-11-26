# ???
zOffset = 0
noiseMax = 1
ox = 0
oy = 0 

# colorA = color("#0CCBCFAA")
color1 = color(12, 203, 207, 0.7)

# colorB = color("#FE68B5AA")
color2 = color(254, 104, 181)

def setup():
    size(1000, 1000)
    # frameRate(1)

    ox = width / 2
    oy = height

    MAX = width if width > height else height


    noFill();
    background("#E7ECF2")

def draw():
    global zOffset

    value = abs(sin(radians(zOffset * 100)))
    strokeColor = lerpColor(color1, color2, value)
    stroke(strokeColor)
    # push()
    translate(ox, oy)
    beginShape()

    for degree in range(360):
        angle = radians(degree)
        xOffset = map(cos(angle), -1, 1, 0, noiseMax)
        yOffset = map(sin(angle), -1, 1, 0, noiseMax)

        n = noise(xOffset, yOffset, zOffset)

        radius = map(n, 0, 1, 0, height * 1.5)
        x = radius * cos(angle)
        y = radius * sin(angle)
        vertex(x,y)

    endShape(CLOSE)
    zOffset += 0.005
    # pop()
