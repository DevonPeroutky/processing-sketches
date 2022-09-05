from utilities.emotional_color_palette import EmotionalColorPalette
from utilities.flow_particle_factory import FlowParticleFactory
from utilities.angle_grid import AngleGrid

noise_step = .03
z_noise_step = 0
angle_grid = None
num_rows = 0
num_cols = 0
z_noise_offset = 0
grid_scale_factor = .2
lines_per_layer = 100
left_x, right_x, top_y, bottom_y = [0]*4
starting_num_lines = 0
line_length = 500
max_lines_number = 100000
lines = {}
resolution_factor = .01
particle_manager = None

def calculate_layer_parameters(frameCount, lines_per_layer, emotion, line_length):
    # stroke_weight = int(max(50 - (frameCount), 2))
    stroke_weight = 40
    opacity = int(min((frameCount/3) + 1, 10))
    opacity = 5
    max_speed = 3
    starting_velocity = 1
    emotion = EmotionalColorPalette.get_random_emotion()
    return (lines_per_layer, line_length, emotion, stroke_weight, opacity, max_speed, starting_velocity)

def setup():
    global angle_grid, num_cols, num_rows, grid_scale_factor, left_x, right_x, top_y, bottom_y, line_length, particle_manager
    colorMode(HSB, 360, 100, 100)
    size(1700, 1100)
    frameRate(24)

    # Set background_color
    background(0, 0, 100)

    # Build AngleGrid
    angle_grid = AngleGrid(width=width, height=height, grid_scale_factor=.1, resolution_factor=resolution_factor, z_noise_offset=z_noise_offset, noise_step=noise_step)

    # Visualize FlowField
    angle_grid.visualize_flow_field()

    # Build ParticleManager
    particle_manager = FlowParticleFactory(max_lines=max_lines_number, left_x=angle_grid.left_x, right_x=angle_grid.right_x, top_y=angle_grid.top_y, bottom_y=angle_grid.bottom_y)


def draw():
    global num_rows, num_cols, angle_grid, z_noise_offset, noise_step, grid_scale_factor, left_x, right_x, top_y, bottom_y, lines_per_layer, line_length, max_lines_number, particle_manager

    # Constants
    iterations_per_draw = 3

    if frameCount % (24 * 1) == 0:
        print("GOING")

        # 0. Generate parameters for this layer
        parameters = calculate_layer_parameters(frameCount=frameCount, lines_per_layer=lines_per_layer, emotion="surprise", line_length=line_length)

        # 1. Generate the particles for this layer
        particle_manager.build_layer_of_particles(*parameters)

    # 2. Completely draw the particles of the layer
    for _ in range(0, iterations_per_draw):
        particle_manager.iterate(angle_grid)

    print("{}-{}".format(len(particle_manager.particles.keys()), frameRate))
