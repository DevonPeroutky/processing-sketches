from random import randint
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
left_x, right_x, top_y, bottom_y = [0]*4
starting_num_lines = 0
max_lines_number = 100000
lines = {}
resolution_factor = .01
particle_manager = None

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
    # angle_grid.visualize_flow_field()

    # Build ParticleManager
    particle_manager = FlowParticleFactory(max_lines=max_lines_number, left_x=angle_grid.left_x, right_x=angle_grid.right_x, top_y=angle_grid.top_y, bottom_y=angle_grid.bottom_y)

    # Create Initial Layer
    [
        particle_manager.build_layer_of_particles(
            quantity=500,
            line_length=500,
            emotion=EmotionalColorPalette.get_random_emotion(),
            stroke_weight=randint(20, 40),
            opacity=1,
            max_speed=randint(2, 10),
            starting_velocity=randint(2, 10)
        )
        for _ in range(0, 10)
    ]
    # return particle_manager.build_layer_of_particles(
    #     quantity=1000,
    #     line_length=1500,
    #     emotion="neutral",
    #     stroke_weight=randint(20, 40),
    #     opacity=10,
    #     max_speed=randint(2, 10),
    #     starting_velocity=randint(2, 5)
    # )

def draw():
    global angle_grid, particle_manager

    # Constants
    line_length = 5000
    lines_per_layer = 200
    iterations_per_draw = 3

    if frameCount % (24 * 1) == 0:

        # 0. Generate parameters for this layer
        stroke_weight = 30
        opacity = 2
        max_speed = randint(1, 10)
        starting_velocity = randint(2, 8)
        emotion = EmotionalColorPalette.get_random_emotion()
        print("CREATING {} lyaer".format(emotion))
        # return particle_manager.build_layer_of_particles(
        #     quantity=lines_per_layer,
        #     line_length =line_length,
        #     emotion=emotion,
        #     stroke_weight=stroke_weight,
        #     opacity=opacity,
        #     max_speed=max_speed,
        #     starting_velocity=starting_velocity
        # )

    # 2. Completely draw the particles of the layer
    # while particle_manager.particles:
    #     particle_manager.iterate(angle_grid)
    for _ in range(0, iterations_per_draw):
        particle_manager.iterate(angle_grid)

    print("{}-{}".format(len(particle_manager.particles.keys()), frameRate))
