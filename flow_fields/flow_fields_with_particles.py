"""
Betterments:
    - Is there a way to do any smoothing?
    - WTF is drawCurve? Is there a configuration we need to set, to just get a line and not a shape?
    - IS draw line correct? Feel like the angle of the line is off (relatvie to the grid). Possible the degrees -> radians are wrong

Todos
    - We need a color palette. 
    - Lines need to dy gracefully
    - We need it to be dynamic

Variables
    - Colors of lines/shapes    <-- Emotion
    - Length of lines/shapes    <-- ???
    - Lifespan of the lines     <-- Magnitude of the emotion. Tie into Length?
    - Spawn point               <-- Face location
    - Flow field angles         <-- ???
    - Opacity of lines          <-- Time
"""

from shape import FlowLine
import random

noise_step = .02
z_noise_step = .005
angle_grid = [[]]
num_rows = 0
num_cols = 0
z_noise_offset = 0
grid_scale_factor = .1
lines_per_render = 10
left_x, right_x, top_y, bottom_y = [0]*4
starting_num_lines = 0
line_length = 100
max_lines_number = 100
lines = {}

def setup():
    global angle_grid, resolution, num_cols, num_rows, grid_scale_factor, left_x, right_x, top_y, bottom_y, lines, line_length
    size(1000, 1000)
    background(255)
    # noLoop()
    # frameRate(1)
    # print(frameRate)

    left_x = int(width * (0-grid_scale_factor))
    right_x = int(width * (1 + grid_scale_factor))
    top_y = int(height * (0-grid_scale_factor))
    bottom_y = int(height * (1+ grid_scale_factor))

    resolution = int(width  * .01) 
    num_cols = int((right_x - left_x) / resolution)
    num_rows = int((bottom_y - top_y) / resolution)
    angle_grid = [[0 for x in range(num_cols)] for y in range(num_rows)]

    lines = { idx: FlowLine(x=random.randint(left_x, right_x), y=random.randint(top_y, bottom_y), color=0, max_length=line_length) for idx in range(starting_num_lines)}

    print("COLS: {}".format(num_cols))
    print("ROWS: {}".format(num_rows))
    print("TOTAL DIMENSIONS: {} x {}".format(num_cols * resolution, num_rows * resolution))
    print("RESOLUTION: {}".format(resolution))

def draw():
    global resolution, num_rows, num_cols, angle_grid, z_noise_offset, noise_step, grid_scale_factor, left_x, right_x, top_y, bottom_y, lines, lines_per_render, line_length, max_lines_number
    # background(255)

    # Calculate Angle Grid
    y_noise_offset = 0
    for row in range(0, num_rows):
        x_noise_offset = 0
        for col in range(0, num_cols):
            angle = noise(x_noise_offset, y_noise_offset, z_noise_offset) * PI * 2
            angle_grid[row][col] = angle
            x_noise_offset += noise_step
        y_noise_offset += noise_step

    # Visualize FlowField
    # for row in range(0, num_rows):
    #     for col in range(0, num_cols):
    #         x = col * resolution
    #         y = row * resolution
    #         strokeWeight(.7)
    #         draw_vector(x, y, resolution, angle_grid[row][col])
            # textSize(10)
            # text(degrees(angle_grid[row][col]), x, y)

    # Spawn new lines
    for i in range(1, lines_per_render+1):
        if (len(lines.keys()) < max_lines_number):
            line_key = (frameCount * i) + i
            # print("Adding line with key {}".format(line_key))
            lines[line_key] = FlowLine(x=random.randint(left_x, right_x), y=random.randint(top_y, bottom_y), color=0, max_length=line_length)

    # FlowLine Management
    for (key, line) in lines.items():
        line.draw_next_step(angle_grid, resolution, left_x, top_y)
        if line.is_dead():
            # print("Removing {}".format(key))
            lines.pop(key)

    print(len(lines.keys()))
    # z_noise_offset += z_noise_step


def draw_vector(cx, cy, len, angle):
  pushMatrix()
  translate(cx, cy)
  rotate(angle)
  line(0,0,len, 0)
  popMatrix()