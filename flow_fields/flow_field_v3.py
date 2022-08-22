"""
Betterments:
    - Is there a way to do any smoothing?
    - WTF is drawCurve? Is there a configuration we need to set, to just get a line and not a shape?

Todos
    - We need a color palette. 
    - We need it to be dynamic

Variables
    - Colors of lines/shapes    <-- Emotion
    - Length of lines/shapes    <-- ???
    - Spawn point               <-- Face location
    - Flow field angles         <-- ???
    - Opacity of lines          <-- Time


"""


import random

noise_step = .003
z_noise_step = .005
angle_grid = [[]]
num_rows = 0
num_cols = 0
z_noise_offset = 0
grid_scale_factor = .25
num_lines = 10000
left_x, right_x, top_y, bottom_y = [0]*4

def setup():
    global angle_grid, resolution, num_cols, num_rows, grid_scale_factor, left_x, right_x, top_y, bottom_y
    size(1000, 1000)
    background(255)
    noLoop()
    # frameRate(1)

    left_x = int(width * (0-grid_scale_factor))
    right_x = int(width * (1 + grid_scale_factor))
    top_y = int(height * (0-grid_scale_factor))
    bottom_y = int(height * (1+ grid_scale_factor))

    resolution = int(width  * .001) 
    num_cols = int((right_x - left_x) / resolution)
    num_rows = int((bottom_y - top_y) / resolution)
    angle_grid = [[0 for x in range(num_cols)] for y in range(num_rows)]
    print("COLS: {}".format(num_cols))
    print("ROWS: {}".format(num_rows))
    print("TOTAL DIMENSIONS: {} x {}".format(num_cols * resolution, num_rows * resolution))
    print("RESOLUTION: {}".format(resolution))

def draw():
    global resolution, num_rows, num_cols, angle_grid, z_noise_offset, noise_step, num_lines, grid_scale_factor, left_x, right_x, top_y, bottom_y
    # background(255)
    print(frameRate)
    print(z_noise_step)

    # Calculate Angle Grid
    y_noise_offset = 0
    for row in range(0, num_rows):
        x_noise_offset = 0
        for col in range(0, num_cols):
            angle = noise(x_noise_offset, y_noise_offset, z_noise_offset) * PI * 2
            # angle = noise(x_noise_offset, y_noise_offset) * PI * 2
            angle_grid[row][col] = angle
            x_noise_offset += noise_step
        y_noise_offset += noise_step

    # Visualize FlowField
    # for row in range(0, num_rows):
    #     for col in range(0, num_cols):
    #         x = col * resolution
    #         y = row * resolution
    #         draw_vector(x, y, resolution, angle_grid[row][col])

    # draw_curve(x=100, y=250, num_steps=20, angle_grid=angle_grid, grid_scale_factor=grid_scale_factor)
    # plot_point(x=500, y=250, num_steps=50, angle_grid=angle_grid, grid_scale_factor=grid_scale_factor)
    for i in range(num_lines):
        x = random.randint(left_x, right_x)
        y = random.randint(top_y, bottom_y)
        plot_point(x=x, y=y, num_steps=100, angle_grid=angle_grid)

        # WTF is going on with this
        # draw_curve(x=x, y=y, num_steps=50, angle_grid=angle_grid)

        # PAY ATTENTION TO THIS
        z_noise_offset += z_noise_step

def draw_vector(cx, cy, len, angle):
  pushMatrix()
  translate(cx, cy)
  rotate(angle)
  line(0,0,len, 0)
  popMatrix()


def plot_point(x, y, num_steps, angle_grid):
    global resolution, left_x, top_y
    step_size = resolution

    fill(0)
    for n in range(num_steps):
        point(x, y)

        x_offset = x - left_x
        y_offset = y - top_y
        column_index = int(x_offset / resolution)
        row_index = int(y_offset / resolution)

        row_index = row_index if row_index < len(angle_grid) else len(angle_grid) - 1
        column_index = column_index if column_index < len(angle_grid[row_index]) else len(angle_grid[row_index]) - 1
        grid_angle = angle_grid[row_index][column_index]
        x_step = step_size * cos(grid_angle)
        y_step = step_size * sin(grid_angle)
        draw_vector(x, y, resolution, grid_angle)
        x = x + x_step
        y = y + y_step


def draw_curve(x, y, num_steps, angle_grid):
    global resolution, left_x, top_y
    step_size = resolution * 2
    # print("STEP SIZE: {}".format(step_size))

    beginShape()
    fill(0)
    for n in range(num_steps):
        curveVertex(x, y)

        # print("({}, {})".format(x, y))
        x_offset = x - left_x
        y_offset = y - top_y
        column_index = int(x_offset / resolution)
        row_index = int(y_offset / resolution)
        # print("Indexes: ({}, {})".format(column_index, row_index))

        row_index = row_index if row_index < len(angle_grid) else len(angle_grid) - 1
        column_index = column_index if column_index < len(angle_grid[row_index]) else len(angle_grid[row_index]) - 1
        # print("EDGED INDEXES: ({}, {})".format(column_index, row_index))
        grid_angle = angle_grid[row_index][column_index]
        # print("ANGLE: {}".format(grid_angle))

        x_step = step_size * cos(grid_angle)
        y_step = step_size * sin(grid_angle)
        # print("Step Sizes: {} & {}".format(x_step, y_step))
        x = x + x_step
        y = y + y_step
    endShape()
