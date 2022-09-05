from utilities.angle_grid import AngleGrid
from utilities.particle import FlowParticle

noise_step = .03
z_noise_step = 0
angle_grid = None
num_rows = 0
num_cols = 0
z_noise_offset = 0
grid_scale_factor = .2
lines_per_layer = 200
left_x, right_x, top_y, bottom_y = [0]*4
starting_num_lines = 0
line_length = 500
max_lines_number = 100000
lines = {}
resolution_factor = .01
particle_manager = None

def setup():
    global angle_grid, resolution, num_cols, num_rows, grid_scale_factor, left_x, right_x, top_y, bottom_y, line_length, particle_manager, resolution, particle

    colorMode(HSB, 360, 100, 100)
    size(1200, 1200)
    background(0, 0, 100)

    # Build AngleGrid
    angle_grid = AngleGrid(width=width, height=height, grid_scale_factor=.1, resolution_factor=resolution_factor, z_noise_offset=z_noise_offset, noise_step=noise_step)

    # Visualize FlowField
    angle_grid.visualize_flow_field()
    particle = FlowParticle(
        x=500,
        y=500,
        sensitivity=10,
        starting_velocity=1,
        max_speed=1,
        emotion="surprise",
        max_length=500,
        stroke_weight=3,
        opacity=25
    )
    

def draw():
    global angle_grid, resolution, num_cols, num_rows, grid_scale_factor, left_x, right_x, top_y, bottom_y, line_length, particle_manager, resolution, partcle

    # Periodically spawn new particles (Every second? Based on capacity?)

    if frameCount < 50:
        particle.iterate(angle_grid)
