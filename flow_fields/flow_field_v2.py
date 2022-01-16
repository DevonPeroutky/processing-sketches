seed = 0
noise_step = .005
angle_grid = None

def setup():
    global angle_grid, resolution
    size(1000, 1000)
    noLoop()

    left_x = int(width * -0.5)
    right_x = int(width * 1.5)
    top_y = int(height * -0.5)
    bottom_y = int(height * 1.5)

    resolution = int(width  * .01) 
    num_columns = int((right_x - left_x) / resolution)
    num_rows = int((bottom_y - top_y) / resolution)
    angle_grid = [[0 for y in range(num_columns)] for x in range(num_rows)]

    for y in range(num_columns):
        for x in range(num_rows):
            angle = ((x) / float(num_rows) * PI)
            angle_grid[y][x] = angle

def draw():
    global angle_grid, resolution
    background(255)

    xOffset = seed
    for x in range(width):
        yOffset = seed
        for y in range(height):
            if (y == 0 and x % resolution == 0):
                length = int(noise(xOffset, yOffset) * 2000)
                print("(" + str(x) + "," + str(y) + ")  - Length: " + str(length))
                draw_curve(x, y, length)
                return
            yOffset += .005
        xOffset += .005
    

def draw_vector(cx, cy, len, angle):
    pushMatrix()
    translate(cx, cy)
    rotate(angle)
    line(0,0,len, 0)
    # line(len, 0, len - 3, -3)
    # line(len, 0, len - 3, 3)
    popMatrix()

def draw_curve(x, y, num_steps):
    global angle_grid, resolution
    left_x = int(width * -0.5)
    top_y = int(height * -0.5)
    step_size = 1

    beginShape()
    for n in range(num_steps):
        curveVertex(x, y)

        x_offset = x - left_x
        y_offset = y - top_y
        column_index = int(x_offset / resolution)
        row_index = int(y_offset / resolution)

        # NOTE: normally you want to check the bounds here
        column_index = column_index if column_index < len(angle_grid) else len(angle_grid) - 1
        row_index = row_index if row_index < len(angle_grid[column_index]) else len(angle_grid[column_index]) - 1
        grid_angle = angle_grid[column_index][row_index]

        x_step = step_size * cos(grid_angle)
        y_step = step_size * sin(grid_angle)
        x = x + x_step
        y = y + y_step
    endShape()


def calc_noisey_angle(x_offset, y_offset, z_offset):
    return noise(x_offset, y_offset, z_offset) * PI * 2
