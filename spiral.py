z = 0

def setup():
    size(1000, 1000)
    frameRate(12)
    noFill()
    rectMode(CENTER)

def draw():
    global z
    radius = 10
    startX = 0
    startY = 0

    # translate(width/2, height/2)
    # rotate(radians(z))
    # rect(50,50,50,50)
    # beginShape()
    # for angle in range(1440):
    #     radius += .5
    #     x = radius * cos(radians(angle))
    #     y = radius * sin(radians(angle))
    #     println("(" + str(x) + ", " + str(y) + ")")
    #     vertex(x + startX, y + startY)
    # endShape()

    rotateSquare(25, 25, width/2, height /2, z)
    z += 10

    # noLoop()

def rotateSquare(h, w, x, y, angle):
    translate(width/2, height/2)
    rotate(radians(angle))
    rect(h, w, x, y)
    
