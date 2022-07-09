import os
from lenticular_coordinator import LenticularCoordinator
import traceback
import time
import select
import json

# Named Pipe for reading from video_face_tracker
FIFO = "/tmp/piperoni"
fifo = None

# Variables set by external video_face_tracker
distance_from_camera = 0
angle_from_camera = 0

# TODO: Change x_pos received to be a percentage?!?!?!
# The most up-to-date x_pox (being updated very fast)
curr_x_pos = 0

# Lock the x_pos in.
x_pos = 0

# The previously "locked-in" x_pos
last_x_pos = 0
distance_from_center = 0

# Constants
render_width = 1058
render_height = 1586

# Variables
lenticular_img = None
coordinator = None

def setup():
    global fifo, lenticular_img, coordinator
    frameRate(24)
    thread("grab_emotional_parameters")
    size(render_width, render_height)
    coordinator = LenticularCoordinator(render_width, render_height, ["../../images/devon_young.jpg", "../../images/devon_old.jpg"])
    lenticular_img = createImage(render_width, render_height, RGB)
    lenticular_img.loadPixels()
    print("Created image with %s pixels" % len(lenticular_img.pixels))

    # INITIAL RENDER
    new_pixels = coordinator.calc_pixel_diffs(x_pos=render_width, last_x_pos=0)
    coordinator.update_img_pixels(img=lenticular_img, new_pixels=new_pixels, x_pos=x_pos)
    lenticular_img.updatePixels()
    image(lenticular_img, 0, 0)

def draw():
    global fifo, emotion, x_pos, last_x_pos, curr_x_pos, lenticular_img, coordinator
    last_x_pos = x_pos
    x_pos = curr_x_pos
    println(frameRate);

    # Determine Pixel Array
    # rendered_pixel_array = coordinator.render_image_pixels(x_pos=x_pos)

    # Determine which pixels need to be reevaluated
    new_pixels = coordinator.calc_pixel_diffs(x_pos=x_pos, last_x_pos=last_x_pos)

    # Update the image's pixels
    coordinator.update_img_pixels(img=lenticular_img, new_pixels=new_pixels, x_pos=x_pos)
    
    # Update image on the screen
    lenticular_img.updatePixels()

    # Render Image
    image(lenticular_img, 0, 0)

def set_x_pos(received_x_pos):
    global render_width, curr_x_pos
    """
    OpenCV is right-to-left because its from perspective of the camera. Processing is left to right
    """
    curr_x_pos = render_width - received_x_pos



def grab_emotional_parameters():
    global distance_from_camera, angle_from_camera, curr_x_pos

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
                        distance_from_camera = location_data.get('distance_in_inches', '50')
                        angle_from_camera = location_data.get('angle_from_camera', '0')
                        set_x_pos(int(location_data.get('x_pos', '0')))
                        distance_from_center = location_data.get('distance_from_center', '0')
                    except ValueError as e:
                        print("Unable to parse Json")
