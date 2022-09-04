"""
Todos
    - Experiment with line lengths?
    - We need a color palette. 
    - Lines need to dye gracefully
    - We need it to be dynamic

Variables
    - Colors of lines/shapes    <-- Emotion
    - Length of lines/shapes    <-- The degree of cohesiveness of the emotion? Constant?
    - Lifespan of the lines     <-- Magnitude of the emotion. Tie into Length? Constant?
    - Spawn point               <-- Face location
    - Flow field angles         <-- ???
    - Opacity of lines          <-- Decay over Time

Algo
    1. Read lastest payload from pipe
    2. Create FlowParticle for each Emotion:
        # Lifespan? Line Length? 
        FlowParticle(x=face_center_x, y=face_center_y, max_speed=2, color=color_palette.get(emotion))



"""
import sys
sys.path.append('/Users/devonperoutky/Development/processing/utilities')
sys.path.append('/Users/devonperoutky/Development/processing/utilities/unix_pipes')

from utilities.flow_particle_factory import FlowParticleFactory
from utilities.utils import visualize_flow_field
from reader import UnixPipeReader

noise_step = .03
z_noise_step = 0
angle_grid = [[]]
num_rows = 0
num_cols = 0
z_noise_offset = 0
grid_scale_factor = .2
lines_per_render = 100
left_x, right_x, top_y, bottom_y = [0]*4
starting_num_lines = 10000
line_length = 500
max_lines_number = 20000
lines = {}
resolution_factor = .01
particle_manager = FlowParticleFactory(max_lines=max_lines_number)

def setup():
    global angle_grid, resolution, num_cols, num_rows, grid_scale_factor, left_x, right_x, top_y, bottom_y, line_length, particle_manager, starting_num_lines
    size(1000, 1000)
    background(255)
    smooth()

    # thread("grab_emotional_parameters")

    left_x = int(width * (0-grid_scale_factor))
    right_x = int(width * (1 + grid_scale_factor))
    top_y = int(height * (0-grid_scale_factor))
    bottom_y = int(height * (1+ grid_scale_factor))

    resolution = int((right_x - left_x)  * resolution_factor)
    num_cols = int((right_x - left_x) / resolution)
    num_rows = int((bottom_y - top_y) / resolution)
    angle_grid = [[0 for x in range(num_cols)] for y in range(num_rows)]

    particle_manager.spawn_new_particles(quantity=starting_num_lines, left_x=left_x, right_x=right_x, top_y=top_y, bottom_y=bottom_y, line_length=line_length, emotion="neutral")

    print("LEFT X: {}".format(left_x))
    print("RIGHT X: {}".format(right_x))
    print("TOP Y: {}".format(top_y))
    print("BOTTOM Y: {}".format(bottom_y))
    print("COLS: {}".format(num_cols))
    print("ROWS: {}".format(num_rows))
    print("TOTAL DIMENSIONS: {} x {}".format(num_cols * resolution, num_rows * resolution))
    print("RESOLUTION: {}".format(resolution))
    print("NUMBER OF LINES: {}".format(max_lines_number))

    # Calculate Angle Grid
    y_noise_offset = 0
    for row in range(0, num_rows):
        x_noise_offset = 0
        for col in range(0, num_cols):
            angle = noise(x_noise_offset, y_noise_offset, z_noise_offset) * PI * 2
            angle_grid[row][col] = angle
            x_noise_offset += noise_step
        y_noise_offset += noise_step


def draw():
    global resolution, num_rows, num_cols, angle_grid, z_noise_offset, noise_step, grid_scale_factor, left_x, right_x, top_y, bottom_y, lines_per_render, line_length, max_lines_number, particle_manager

    # Visualize FlowField
    # visualize_flow_field(angle_grid, num_rows, num_cols, resolution)

    # Spawn ambient background lines
    # particle_manager.spawn_new_particles(quantity=lines_per_render, left_x=left_x, right_x=right_x, top_y=top_y, bottom_y=bottom_y, line_length=line_length, emotion="neutral")

    # Particle Lifecyle Management
    particle_manager.iterate(angle_grid, resolution, left_x, top_y) 

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
