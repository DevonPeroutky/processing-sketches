import os
import traceback
import time
import select
import json

FIFO = "/tmp/piperoni"
fifo = None
distance_from_camera = 0
angle_from_camera = 0

def setup():
    global fifo
    frameRate(1)
    thread("grab_emotional_parameters")
    size(500, 500)

def draw():
    global fifo
    global emotion
    background(255, 255, 255)

    textSize(32)
    fill(0, 102, 153)

def grab_emotional_parameters():
    global distance_from_camera, angle_from_camera

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
                    except ValueError as e:
                        print("Unable to parse Json")
