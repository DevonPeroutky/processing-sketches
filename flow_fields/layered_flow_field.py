import sys
sys.path.append('/Users/devonperoutky/Development/processing/utilities')
sys.path.append('/Users/devonperoutky/Development/processing/utilities/unix_pipes')

from flow_particle_factory import FlowParticleFactory
from utils import visualize_flow_field
from reader import UnixPipeReader

noise_step = .01
z_noise_step = .07
angle_grid = [[]]
num_rows = 0
num_cols = 0
z_noise_offset = 0
grid_scale_factor = .2
lines_per_render = 10
left_x, right_x, top_y, bottom_y = [0]*4
starting_num_lines = 100
line_length = 500
max_lines_number = 100000
lines = {}
resolution_factor = .01
particle_manager = FlowParticleFactory(max_lines=max_lines_number)

def setup():
    global angle_grid, resolution, num_cols, num_rows, grid_scale_factor, left_x, right_x, top_y, bottom_y, line_length, particle_manager, starting_num_lines
    size(1000, 1000)
    background(255)
    smooth()

    # thread("grab_emotional_parameters")

    left_x = int(width * (0-grid_scale_factor))
    right_x = int(width * (1 + grid_scale_factor))
    top_y = int(height * (0-grid_scale_factor))
    bottom_y = int(height * (1+ grid_scale_factor))

    resolution = int((right_x - left_x)  * resolution_factor)
    num_cols = int((right_x - left_x) / resolution)
    num_rows = int((bottom_y - top_y) / resolution)
    angle_grid = [[0 for x in range(num_cols)] for y in range(num_rows)]

    # Calculate Angle Grid
    build_angle_grid(angle_grid, num_rows, num_cols, noise_step, z_noise_offset)

    # Visualize FlowField
    # visualize_flow_field(angle_grid, num_rows, num_cols, resolution)

def build_angle_grid(angle_grid, num_rows, num_cols, noise_step, z_noise_offset):
    print("Building the next angle grid with {} & {}" .format(noise_step, z_noise_offset))
    y_noise_offset = 0
    for row in range(0, num_rows):
        x_noise_offset = 0
        for col in range(0, num_cols):
            angle = noise(x_noise_offset, y_noise_offset, z_noise_offset) * PI * 2
            angle_grid[row][col] = angle
            x_noise_offset += noise_step
        y_noise_offset += noise_step


def draw():
    global resolution, num_rows, num_cols, angle_grid, z_noise_offset, noise_step, grid_scale_factor, left_x, right_x, top_y, bottom_y, lines_per_render, line_length, max_lines_number, particle_manager
    """
    Draw the flow field in layers.
        1. Generate the particles for this layer
        2. Completely draw the layer's particles to completion
        3. Re calculate angle grid 
    """
    if frameCount <= 5:
        print(frameCount)

        # 1. Generate the particles for this layer
        particle_manager.spawn_new_reed_groups(reed_width=200, reed_quantity= 2000, left_x=left_x, top_y=top_y, line_length=line_length, emotion="neutral")

        # 2. Completely draw the particles
        while particle_manager.particles:
            particle_manager.iterate(angle_grid, resolution, left_x, top_y)

        # 3. Build the Angle Grid for the next layer
        z_noise_offset += z_noise_step
        build_angle_grid(angle_grid, num_rows, num_cols, noise_step, z_noise_offset)
