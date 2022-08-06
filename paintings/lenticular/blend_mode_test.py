# Constants
render_width = 1058
render_height = 1586

def setup():
    global render_height, render_width
    size(render_width, render_height)
    young_img_src = "../../images/devon_young.jpg"
    background(loadImage(young_img_src))
    noLoop()
    blendMode(DIFFERENCE)


def draw():
    global render_height, render_width
    old_img_src = "../../images/devon_old.jpg"
    old_img = loadImage(old_img_src)
    image(old_img, 0, 0)
