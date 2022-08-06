
rubberduck = None

def setup():
    global rubberduck
    noLoop()
    colorMode(RGB, 1)

    size(960,480)
    background('#004477')
    noStroke()
    fill('#FF0000')
    rect(0,0,width,80)
    fill('#FF9900')
    rect(0,80,width,80)
    fill('#FFFF00')
    rect(0,160,width,80)
    fill('#00FF00')
    rect(0,240,width,80)
    fill('#0099FF')
    rect(0,320,width,80)
    fill('#6633FF')
    rect(0,400,width,80)

    rubberduck = loadImage('../../images/rubber_duck.jpg')

    image(rubberduck, 0,0)



    halfwidth = width / 2
    x = 0
    y = 0

    for i in range(halfwidth * height):

        if i % halfwidth == 0 and i != 0:
            y += 1
            x = 0
        x += 1

        layer1 = get(x, y)
        layer0 = get(x+halfwidth, y)

        r = red(layer1) * red(layer0)
        g = green(layer1) * green(layer0)
        b = blue(layer1) * blue(layer0)
        layer2 = color(r, g, b)
        set( x+halfwidth, y, layer2 )


def draw():
    print("Hi")

    
