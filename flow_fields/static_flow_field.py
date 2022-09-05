import sys
sys.path.append('/Users/devonperoutky/Development/processing/utilities')
sys.path.append('/Users/devonperoutky/Development/processing/utilities/unix_pipes')

from random import randint
from utilities.particle import FlowParticle
from utilities.angle_grid import AngleGrid
from utilities.emotional_color_palette import EmotionalColorPalette

angle_grid = None
particle_manager = None

def setup():
    global particles, angle_grid

    colorMode(HSB, 360, 100, 100)
    size(1000, 1000)

    # Constants
    max_lines_number = 1000
    grid_scale_factor = .2
    resolution_factor = .01
    noise_step = .03
    z_noise_offset = 0

    # Set background_color
    background(0, 0, 100)

    # Build AngleGrid
    angle_grid = AngleGrid(width=width, height=height, grid_scale_factor=.1, resolution_factor=resolution_factor, z_noise_offset=z_noise_offset, noise_step=noise_step)

    # Visualize FlowField
    # angle_grid.visualize_flow_field()

    num_layers = 10
    particles_per_layer = 200
    particles = [
        FlowParticle(
            x=randint(angle_grid.left_x, angle_grid.right_x),
            y=randint(angle_grid.top_y, angle_grid.bottom_y),
            sensitivity=10,
            starting_velocity=randint(1, 5),
            max_speed=10,
            emotion=EmotionalColorPalette.get_random_emotion(),
            max_length=500,
            stroke_weight=randint(5, 40),
            opacity=5,
        )
        for _ in range(0, particles_per_layer) for l in range(0, num_layers)
    ]
    print("{} particles".format(len(particles)))


def draw():
    global particles, angle_grid, face_center_y, face_center_x, face_width

    for particle in particles:
        if particle.is_finished(angle_grid.left_x, angle_grid.top_y):
            particle.reset(angle_grid.left_x, angle_grid.top_y)
        else:
            particle.iterate(angle_grid)
