import sys
sys.path.append('/Users/devonperoutky/Development/processing/utilities')
sys.path.append('/Users/devonperoutky/Development/processing/utilities/unix_pipes')

from utilities.emotional_color_palette import EmotionalColorPalette
from utilities.flow_particle_factory import FlowParticleFactory
from utilities.angle_grid import AngleGrid
from reader import UnixPipeReader

angle_grid = None
particle_manager = None
lines_per_layer = 200
line_length = 500

# REMOVE
face_center_x = 0
face_center_y = 0
face_width = 0

def setup():
    global particle_manager, angle_grid

    colorMode(HSB, 360, 100, 100)
    size(1000, 1000)

    # Read emotion_payload from pipe
    thread("grab_emotional_parameters")

    # Constants
    max_lines_number = 100000
    grid_scale_factor = .2
    resolution_factor = .01
    noise_step = .03
    z_noise_offset = 0

    # Set background_color
    background(0, 0, 100)

    # Build AngleGrid
    angle_grid = AngleGrid(width=width, height=height, grid_scale_factor=grid_scale_factor, resolution_factor=resolution_factor, z_noise_offset=z_noise_offset, noise_step=noise_step)

    # Visualize FlowField
    # angle_grid.visualize_flow_field()

    # Build ParticleManager
    particle_manager = FlowParticleFactory(max_lines=max_lines_number, left_x=angle_grid.left_x, right_x=angle_grid.right_x, top_y=angle_grid.top_y, bottom_y=angle_grid.bottom_y)


def draw():
    global particle_manager, angle_grid, face_center_y, face_center_x, face_width

    # Constants
    iterations_per_draw = 100

    # DELETE ME
    # f_x = int(round(map(face_center_x, 1280, 0, 0, 1000)))
    # f_y = int(round(map(face_center_y, 0, 720, 0, 1000)))
    # background(0, 0, 100)
    # stroke(0,0,0, 100)
    # noFill()
    # circle(f_x, f_y, face_width)
    # fill(0, 0, 0)
    # text("{}, {}".format(f_x, f_y), f_x + face_width /2, f_y + face_width/2)

    # z_noise_step = 0.005
    for _ in range(0, iterations_per_draw):
        particle_manager.iterate(angle_grid)

    
    print("{}-{}".format(len(particle_manager.particles.keys()), frameRate))


def grab_emotional_parameters():
    FIFO = "/tmp/EMOTIONAL_PIPE"
    UnixPipeReader().open_json_pipe(FIFO, update_configuration_from_emotions)

def update_configuration_from_emotions(emotions):
    global particle_manager, face_center_x, face_center_y, face_width

    if particle_manager:
        for emotion in emotions:
            # particle_manager.generate_layer_from_emotion_payload(emotion)
            particle_manager.generate_particles_from_emotion_payload(emotion)

            
            face_location = emotion.get('region')
            face_width = int(round(face_location['w']))
            face_height = int(round(face_location['h']))
            face_center_x = face_location['x']
            face_center_y = face_location['y']
