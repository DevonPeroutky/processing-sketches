"""
Just playing around
"""

from utilities.angle_grid import AngleGrid, TestAngleGrid
from utilities.particle import FlowParticle, GradientFlowParticle

noise_step = .03
z_noise_step = 0
angle_grid = None
num_rows = 0
num_cols = 0
z_noise_offset = 0
grid_scale_factor = .2
lines_per_layer = 200
left_x, right_x, top_y, bottom_y = [0] * 4
starting_num_lines = 0
line_length = 500
max_lines_number = 100000
lines = {}
resolution_factor = .01
particle_manager = None
particles = []


def setup():
    global angle_grid, resolution, num_cols, num_rows, grid_scale_factor, left_x, right_x, top_y, bottom_y, line_length, particle_manager, resolution, particle, particles

    colorMode(HSB, 360, 100, 100)
    size(1200, 1200)
    background(0, 0, 100)
    frameRate(10)

    # Build AngleGrid
    angle_grid = TestAngleGrid(width=width,
                               height=height,
                               grid_scale_factor=.1,
                               resolution_factor=resolution_factor,
                               z_noise_offset=z_noise_offset,
                               noise_step=noise_step)

    # Visualize FlowField
    # angle_grid.visualize_flow_field()
    noise_offset = .005
    particles = []
    for i in range(0, 1000, 40):
        for j in range(0, 1000, 80):
            particles.append(
                GradientFlowParticle(x=100 + i,
                                     y=100 + j,
                                     sensitivity=10,
                                     starting_velocity=1,
                                     max_speed=10,
                                     emotion="surprise",
                                     max_length=200 *
                                     noise(i * noise_offset, j * noise_offset),
                                     stroke_weight=1,
                                     opacity=40))


def draw():
    global angle_grid, resolution, num_cols, num_rows, grid_scale_factor, left_x, right_x, top_y, bottom_y, line_length, particle_manager, resolution, partcles

    for particle in particles:
        if not particle.is_finished(left_x, top_y):
            particle.iterate(angle_grid)
