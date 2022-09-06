import sys
sys.path.append('/Users/devonperoutky/Development/processing/utilities')
sys.path.append('/Users/devonperoutky/Development/processing/utilities/unix_pipes')

from random import randint
from utilities.particle import FlowParticle
from utilities.angle_grid import AngleGrid
from utilities.emotional_color_palette import EmotionalColorPalette

# Constants
angle_grid = None
particle_manager = None
noise_step = .03
z_noise_offset = 0
max_lines_number = 1000
grid_scale_factor = .2
resolution_factor = .01

def setup():
    global particles, angle_grids, noise_step, z_noise_offset, resolution_factor, grid_scale_factor, max_lines_number

    colorMode(HSB, 360, 100, 100)
    size(1720, 1120)

    # Set background_color
    background(0, 0, 100)

    # Build AngleGrid
    angle_grid = AngleGrid(width=width, height=height, grid_scale_factor=.1, resolution_factor=resolution_factor, z_noise_offset=z_noise_offset, noise_step=noise_step)

    # Visualize FlowField
    # angle_grid.visualize_flow_field()
    colors = [ 
        (338, 95, 100),     # RED
        (209, 100, 100),       # BLUE
        (134, 100, 100),       # GREEN
        (153, 100, 100), # TEAL-ISH
        (317, 100, 100),     # PURPLE
        (21, 100, 100),     # ORANGE
    ]

    particles_per_layer = 500
    particles = []
    print("{} -> {}".format(angle_grid.left_x, angle_grid.right_x))
    for l in range(0, len(colors)):
        color = colors[l] 
        layer = [
            FlowParticle(
                x=randint(angle_grid.left_x, angle_grid.right_x),
                y=randint(angle_grid.top_y, angle_grid.bottom_y),
                sensitivity=10,
                starting_angle=radians(randint(1, 360)),
                starting_velocity=randint(3, 5),
                max_speed=10,
                emotion=EmotionalColorPalette.get_random_emotion(),
                max_length=1000,
                stroke_weight=randint(30, 40),
                color=color,
                opacity=50
            ) for p in range(0, particles_per_layer)
        ]
        particles.append(layer)

    angle_grids = [
        AngleGrid(width=width, height=height, grid_scale_factor=.1, resolution_factor=resolution_factor, z_noise_offset=0, noise_step=noise_step)
        for z in range(0, len(colors))
    ]
    # Reverse for Fun
    # for idx, a in enumerate(angle_grids):
    #     if idx % 2 == 0:
    #         a.reverse_angle_grid()

    print("{} particles".format(len(particles)))


def draw():
    global particles, angle_grids, noise_step, z_noise_offset, resolution_factor, grid_scale_factor, max_lines_number

    for idx, layer in enumerate(particles):
        # print("LAYER {}".format(idx))
        angle_grid = angle_grids[idx]
        for particle in layer:
            if not particle.is_finished(angle_grid.left_x, angle_grid.top_y):
                particle.iterate(angle_grid)
            else:
                particle.reset(angle_grid.left_x, angle_grid.top_y, emotion=EmotionalColorPalette.get_random_emotion())
