seed = 0
noise_step = .005
angle_grid = None

def setup():
    global angle_grid, resolution
    size(1000, 1000)
    frameRate(24)

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
    global angle_grid

    background(255)
    for y in range(len(angle_grid)):
        for x in range(len(angle_grid[y])):
            draw_vector(x * resolution, y * resolution, resolution / 2, angle_grid[x][y])
    

def draw_vector(cx, cy, len, angle):
    pushMatrix()
    translate(cx, cy)
    rotate(angle)
    line(0,0,len, 0)
    # line(len, 0, len - 3, -3)
    # line(len, 0, len - 3, 3)
    popMatrix()

def calc_noisey_angle(x_offset, y_offset, z_offset):
    return noise(x_offset, y_offset, z_offset) * PI * 2
