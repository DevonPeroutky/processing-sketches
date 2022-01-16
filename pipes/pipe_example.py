import traceback
import time
import select
import json

FIFO = "/tmp/piperoni"
fifo = None
emotion = 'neutral'

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
    print("THE EMOTION" + emotion)
    text(emotion, 10, 30)


def grab_emotional_parameters():
    global emotion

    print("Setting up FIFO reader...")

    PIPE_PATH = '/Users/devonperoutky/Development/playground/python/opencv/playground/EMOTIONAL_PIPE'
    with open(PIPE_PATH) as fifo:
        while True:
            line = fifo.readline()
            if len(line) == 0:
                continue
            else:
                print(line)
                emotions = json.loads(line)
                dom_emotion = emotions.get('dominant_emotion', 'neutral')
                print(dom_emotion)
                time.sleep(1)
                emotion = dom_emotion

