import sys
sys.path.append('/Users/devonperoutky/Development/processing/utilities')
sys.path.append('/Users/devonperoutky/Development/processing/utilities/unix_pipes')

from random import randint
from utilities.emotional_color_palette import EmotionalColorPalette
from utilities.flow_particle_factory import FlowParticleFactory
from utilities.angle_grid import AngleGrid
from reader import UnixPipeReader

angle_grid = None
emotional_particle_manager = None
ambient_particle_manager = None
background_particle_manager = None
background_color = (0, 0, 100)
noise_step = .03
z_noise_offset = 0

def setup():
    global emotional_particle_manager, ambient_particle_manager, angle_grid, background_color, background_particle_manager, noise_step, z_noise_offset

    colorMode(HSB, 360, 100, 100)
    size(1792, 1120)

    # Read emotion_payload from pipe
    thread("grab_emotional_parameters")

    # Constants
    max_lines_number = 400
    grid_scale_factor = .2
    resolution_factor = .01

    # Set background_color
    background(*background_color)

    # Build AngleGrid
    angle_grid = AngleGrid(width=width, height=height, grid_scale_factor=grid_scale_factor, resolution_factor=resolution_factor, z_noise_offset=z_noise_offset, noise_step=noise_step)

    # Visualize FlowField
    # angle_grid.visualize_flow_field()

    # Build ParticleManage
    emotional_particle_manager = FlowParticleFactory(max_lines=max_lines_number, left_x=angle_grid.left_x, right_x=angle_grid.right_x, top_y=angle_grid.top_y, bottom_y=angle_grid.bottom_y)
    ambient_particle_manager = FlowParticleFactory(max_lines=max_lines_number, left_x=angle_grid.left_x, right_x=angle_grid.right_x, top_y=angle_grid.top_y, bottom_y=angle_grid.bottom_y)
    background_particle_manager = FlowParticleFactory(max_lines=max_lines_number/4, left_x=angle_grid.left_x, right_x=angle_grid.right_x, top_y=angle_grid.top_y, bottom_y=angle_grid.bottom_y)


def draw():
    global emotional_particle_manager, ambient_particle_manager, background_particle_manager, angle_grid, face_center_y, face_center_x, face_width, background_color, noise_step, z_noise_offset

    # Macro constants
    iterations_per_draw = 2
    max_additional_lines_per_draw = 50
    
    # Particle Constants
    ambient_emotion = "neutral"
    line_length = 50
    stroke_weight = 40
    opacity = 60
    max_speed = 3
    starting_velocity = randint(1, 3)

    for _ in range(0, iterations_per_draw):
        ambient_particle_manager.iterate(angle_grid)
        emotional_particle_manager.iterate(angle_grid)
        background_particle_manager.iterate(angle_grid)

    # Add in ambient particles
    # background_particle_manager.build_layer_of_particles(
    #     quantity=max_additional_lines_per_draw,
    #     line_length =line_length*2,
    #     emotion=ambient_emotion,
    #     stroke_weight=stroke_weight,
    #     opacity=opacity,
    #     max_speed=max_speed,
    #     starting_velocity=starting_velocity,
    #     color=background_color,
    # )
    ambient_particle_manager.build_layer_of_particles(
        quantity=max_additional_lines_per_draw,
        line_length=line_length,
        emotion=ambient_emotion,
        stroke_weight=stroke_weight,
        opacity=opacity,
        max_speed=max_speed,
        starting_velocity=starting_velocity,
        color=(209, randint(50, 90), 64)
    )
    

    # Slightly change the angle_grid overtime
    if (frameCount % (24 * 1) == 0):
        z_noise_offset += .005
        angle_grid.build_angle_grid(z_noise_offset, noise_step)
    
    print("{}-{}".format(len(emotional_particle_manager.particles.keys()), frameRate))


def grab_emotional_parameters():
    FIFO = "/tmp/EMOTIONAL_PIPE"
    UnixPipeReader().open_json_pipe(FIFO, update_configuration_from_emotions)

def update_configuration_from_emotions(emotions):
    global emotional_particle_manager, face_center_x, face_center_y, face_width

    if emotional_particle_manager:
        for emotion in emotions:
            # particle_manager.generate_layer_from_emotion_payload(emotion)
            emotional_particle_manager.generate_particles_from_emotion_payload(emotion)
