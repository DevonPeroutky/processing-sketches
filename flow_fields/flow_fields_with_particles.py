"""
Simple permanent FlowField implementation.
"""

import sys

sys.path.append('/Users/devonperoutky/Development/processing/utilities')
sys.path.append(
    '/Users/devonperoutky/Development/processing/utilities/unix_pipes')

from utilities.angle_grid import AngleGrid
from reader import UnixPipeReader
from utilities.utils import visualize_flow_field
from utilities.flow_particle_factory import FlowParticleFactory
from random import randint

noise_step = .03
z_noise_step = 0
angle_grid = None
num_rows = 0
num_cols = 0
z_noise_offset = 0
grid_scale_factor = .2
lines_per_render = 100
left_x, right_x, top_y, bottom_y = [0] * 4
starting_num_lines = 10000
line_length = 500
max_lines_number = 20000
lines = {}
resolution_factor = .01
particle_manager = None


def setup():
    global angle_grid, resolution, num_cols, num_rows, grid_scale_factor, left_x, right_x, top_y, bottom_y, line_length, particle_manager, starting_num_lines
    size(1000, 1000)
    background(255)
    smooth()

    # thread("grab_emotional_parameters")

    left_x = int(width * (0 - grid_scale_factor))
    right_x = int(width * (1 + grid_scale_factor))
    top_y = int(height * (0 - grid_scale_factor))
    bottom_y = int(height * (1 + grid_scale_factor))

    resolution = int((right_x - left_x) * resolution_factor)
    num_cols = int((right_x - left_x) / resolution)
    num_rows = int((bottom_y - top_y) / resolution)

    angle_grid = AngleGrid(width=width,
                           height=height,
                           grid_scale_factor=.1,
                           resolution_factor=resolution_factor,
                           z_noise_offset=z_noise_offset,
                           noise_step=noise_step)

    particle_manager = FlowParticleFactory(max_lines=max_lines_number,
                                           left_x=left_x,
                                           right_x=right_x,
                                           top_y=top_y,
                                           bottom_y=bottom_y)
    particle_manager.build_layer_of_particles(quantity=500,
                                              line_length=500,
                                              emotion="neutral",
                                              stroke_weight=randint(20, 40),
                                              opacity=1,
                                              max_speed=randint(2, 10),
                                              starting_velocity=randint(2, 10))

    print("LEFT X: {}".format(left_x))
    print("RIGHT X: {}".format(right_x))
    print("TOP Y: {}".format(top_y))
    print("BOTTOM Y: {}".format(bottom_y))
    print("COLS: {}".format(num_cols))
    print("ROWS: {}".format(num_rows))
    print("TOTAL DIMENSIONS: {} x {}".format(num_cols * resolution,
                                             num_rows * resolution))
    print("RESOLUTION: {}".format(resolution))
    print("NUMBER OF LINES: {}".format(max_lines_number))


def draw():
    global resolution, num_rows, num_cols, angle_grid, z_noise_offset, noise_step, grid_scale_factor, left_x, right_x, top_y, bottom_y, lines_per_render, line_length, max_lines_number, particle_manager

    # Particle Lifecyle Management
    particle_manager.iterate(angle_grid, reset=True)

    # For a dynamic Flow Field
    # z_noise_offset += z_noise_step

    print("{} - {}".format(frameRate, len(particle_manager.particles.keys())))


def grab_emotional_parameters():
    FIFO = "/tmp/EMOTIONAL_PIPE"
    UnixPipeReader().open_json_pipe(FIFO, update_configuration_from_emotions)


def update_configuration_from_emotions(emotions):
    global angle_grid, resolution, num_cols, num_rows, grid_scale_factor, left_x, right_x, top_y, bottom_y, line_length, particle_manager

    for emotion in emotions:
        particle_manager.generate_particles_from_emotion_payload(emotion)
