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
x_pos = 0
distance_from_center = 0

# Constants
render_width = 1058
render_height = 1586

# Variables
lenticular_img = None
coordinator = LenticularCoordinator(render_width, render_height, ["../../images/devon_young.jpg", "../../images/devon_old.jpg"])

def setup():
    global fifo, lenticular_img
    frameRate(24)
    thread("grab_emotional_parameters")
    size(render_width, render_height)
    lenticular_img = createImage(render_width, render_height, RGB)
    lenticular_img.loadPixels()

def draw():
    global fifo, emotion, x_pos, lenticular_img
    background(255, 255, 255)
    println(frameRate);

    # Determine Pixel Array
    rendered_pixel_array = coordinator.render_image_pixels(x_pos=x_pos)
    
    # Update image on the screen
    # for i in range(len(lenticular_img.pixels)):
    #     lenticular_img.pixels[i] = rendered_pixel_array[i]
    # lenticular_img.updatePixels()

    # Render Image
    # image(lenticular_img, 0, 0)


def draw_new_image():
    pass


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
                        distance_from_camera = location_data.get('distance_in_inches', '50')
                        angle_from_camera = location_data.get('angle_from_camera', '0')
                        x_pos = location_data.get('x_pos', '0')
                        distance_from_center = location_data.get('distance_from_center', '0')
                    except ValueError as e:
                        print("Unable to parse Json")
