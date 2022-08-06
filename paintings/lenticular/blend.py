import json

# Named Pipe for reading from video_face_tracker
FIFO = "/tmp/piperoni"
fifo = None

# Lock the x_pos in.
x_pos = 0

# Constants
render_width = 1058
render_height = 1586

# Variables
young_img_src = "../../images/devon_young.jpg"
old_img_src = "../../images/devon_old.jpg"


def setup():
    global render_height, render_width, young_img_src, old_img_src
    size(render_width, render_height)
    # background(loadImage(young_img_src))
    blendMode(BLEND)

    thread("grab_emotional_parameters")

def draw():
    global render_height, render_width, x_pos, old_img_src, young_img_src
    background(loadImage(young_img_src))
    # print(frameRate)

    curr_x_pos = x_pos
    tint_value = map(curr_x_pos, 0, render_width, 0, 255)
    # print("Mapping: %s --> %s" % (curr_x_pos, tint_value))

    tint(255, tint_value)
    old_img = loadImage(old_img_src)
    image(old_img, 0, 0)


def grab_emotional_parameters():
    global distance_from_camera, angle_from_camera, x_pos

    PIPE_PATH = '/tmp/test'
    while True:
        with open(PIPE_PATH) as fifo:
            while True:
                line = fifo.readline()
                cleaned_line = line.strip()
                if len(cleaned_line) == 0:
                    break
                else:
                    try:
                        location_data = json.loads(line)
                        x_pos = int(location_data.get('x_pos', '0'))
                    except ValueError as e:
                        print("Unable to parse Json")
