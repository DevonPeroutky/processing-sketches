import traceback

FIFO = "/tmp/piperoni"
fifo = None
sup = 0

def setup():
    global sup
    global fifo
    frameRate(15)
    # print("Opening FIFO...")
    # if fifo is None:
    #     print("Need to initialize the the Pipe")
    #     try:
    #         with open(FIFO) as fifo:
    #             for line in fifo:
    #                 print("PRICING")
    #                 print(line)
    #                 sup = random(10)

    #     except Exception:
    #         print(traceback.format_exc())

def draw():
    global fifo
    global sup

    println("Frame: " + str(frameCount))
    if (frameCount % 30 == 0):
        thread("my_thread")

def my_thread():
    println("hi")
