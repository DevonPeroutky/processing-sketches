import sys
sys.path.append('/Users/devonperoutky/Development/processing/utilities')
sys.path.append('/Users/devonperoutky/Development/processing/utilities/unix_pipes')

from utilities.emotional_color_palette import EmotionalColorPalette
from utilities.flow_particle_factory import FlowParticleFactory
from utilities.utils import visualize_flow_field
from reader import UnixPipeReader

noise_step = .03
z_noise_step = 0.001
angle_grid = [[]]
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

def calculate_layer_parameters(frameCount, lines_per_layer, emotion, line_length):
    stroke_weight = int(max(50 - (frameCount), 2))
    # stroke_weight = 40
    opacity = int(min((frameCount/3) + 1, 10))
    opacity = 5
    max_speed = 3
    starting_velocity = 1
    emotion = EmotionalColorPalette.get_random_emotion()
    return (lines_per_layer, line_length, emotion, stroke_weight, opacity, max_speed, starting_velocity)

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

def setup():
    global angle_grid, resolution, num_cols, num_rows, grid_scale_factor, left_x, right_x, top_y, bottom_y, line_length, particle_manager
    colorMode(HSB, 360, 100, 100)
    size(1000, 1000)

    thread("grab_emotional_parameters")

    # Set background_color
    background(0, 0, 100)

    # Set size of flow field to be bigger than the canvas for aesthetics
    left_x = int(width * (0-grid_scale_factor))
    right_x = int(width * (1 + grid_scale_factor))
    top_y = int(height * (0-grid_scale_factor))
    bottom_y = int(height * (1+ grid_scale_factor))

    # Calculate angle grid dimensions
    resolution = int((right_x - left_x)  * resolution_factor)
    num_cols = int((right_x - left_x) / resolution)
    num_rows = int((bottom_y - top_y) / resolution)
    angle_grid = [[0 for x in range(num_cols)] for y in range(num_rows)]

    # Calculate angle grid
    build_angle_grid(angle_grid, num_rows, num_cols, noise_step, z_noise_offset)

    # Visualize FlowField
    # visualize_flow_field(angle_grid, num_rows, num_cols, resolution)

    # Build ParticleManager
    particle_manager = FlowParticleFactory(max_lines=max_lines_number, left_x=left_x, right_x=right_x, top_y=top_y, bottom_y=bottom_y)


def draw():
    global resolution, num_rows, num_cols, angle_grid, z_noise_offset, noise_step, grid_scale_factor, left_x, right_x, top_y, bottom_y, lines_per_layer, line_length, max_lines_number, particle_manager
    
    # Particle Lifecyle Management
    particle_manager.iterate(angle_grid, resolution) 

    # 3. Build the Angle Grid for the next layer
    z_noise_offset += z_noise_step
    build_angle_grid(angle_grid, num_rows, num_cols, noise_step, z_noise_offset)

def grab_emotional_parameters():
    FIFO = "/tmp/EMOTIONAL_PIPE"
    UnixPipeReader().open_json_pipe(FIFO, update_configuration_from_emotions)

def update_configuration_from_emotions(emotions):
    global angle_grid, resolution, num_cols, num_rows, grid_scale_factor, left_x, right_x, top_y, bottom_y, line_length, particle_manager

    if particle_manager:
        for emotion in emotions:
            particle_manager.generate_particles_from_emotion_payload(emotion)
