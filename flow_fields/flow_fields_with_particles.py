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

from flow_particle_factory import FlowParticleFactory
from utils import draw_vector, visualize_flow_field
from reader import UnixPipeReader
from shape import FlowLine
from particle import FlowParticle
from flow_line import FlowCurve
import random

noise_step = .03
z_noise_step = 0
angle_grid = [[]]
num_rows = 0
num_cols = 0
z_noise_offset = 0
grid_scale_factor = .2
lines_per_render = 100
left_x, right_x, top_y, bottom_y = [0]*4
starting_num_lines = 0
line_length = 50
max_lines_number = 100000
lines = {}
resolution_factor = .01

def setup():
    global angle_grid, resolution, num_cols, num_rows, grid_scale_factor, left_x, right_x, top_y, bottom_y, lines, line_length
    size(1000, 1000)
    background(255)
    smooth()

    thread("grab_emotional_parameters")

    left_x = int(width * (0-grid_scale_factor))
    right_x = int(width * (1 + grid_scale_factor))
    top_y = int(height * (0-grid_scale_factor))
    bottom_y = int(height * (1+ grid_scale_factor))

    resolution = int((right_x - left_x)  * resolution_factor)
    num_cols = int((right_x - left_x) / resolution)
    num_rows = int((bottom_y - top_y) / resolution)
    angle_grid = [[0 for x in range(num_cols)] for y in range(num_rows)]

    lines = { idx: FlowLine(x=random.randint(left_x, right_x), y=random.randint(top_y, bottom_y), color=0, max_length=line_length) for idx in range(starting_num_lines)}

    print("LEFT X: {}".format(left_x))
    print("RIGHT X: {}".format(right_x))
    print("TOP Y: {}".format(top_y))
    print("BOTTOM Y: {}".format(bottom_y))
    print("COLS: {}".format(num_cols))
    print("ROWS: {}".format(num_rows))
    print("TOTAL DIMENSIONS: {} x {}".format(num_cols * resolution, num_rows * resolution))
    print("RESOLUTION: {}".format(resolution))
    print("NUMBER OF LINES: {}".format(max_lines_number))


def draw():
    global resolution, num_rows, num_cols, angle_grid, z_noise_offset, noise_step, grid_scale_factor, left_x, right_x, top_y, bottom_y, lines, lines_per_render, line_length, max_lines_number

    # Calculate Angle Grid
    y_noise_offset = 0
    for row in range(0, num_rows):
        x_noise_offset = 0
        for col in range(0, num_cols):
            angle = noise(x_noise_offset, y_noise_offset, z_noise_offset) * PI * 2
            angle_grid[row][col] = angle
            x_noise_offset += noise_step
        y_noise_offset += noise_step

    # Visualize FlowField
    # visualize_flow_field(angle_grid, num_rows, num_cols, resolution)

    # Spawn new lines
    # for _ in range(1, lines_per_render+1):
    #     if (len(lines.keys()) < max_lines_number):
    #         line_key = random.randint(0, 999999999)
    #         lines[line_key] = FlowParticle(x=random.randint(left_x, right_x), y=random.randint(top_y, bottom_y), starting_velocity=1, max_speed=2, emotion="neutral", max_length=random.randint(0, line_length))

    # FlowLine Management
    for (key, line) in lines.items():
        if line.is_finished(left_x, top_y):
            lines.pop(key)
        else:
            line.iterate(angle_grid, resolution, left_x, top_y)

    z_noise_offset += z_noise_step

def grab_emotional_parameters():
    FIFO = "/tmp/EMOTIONAL_PIPE"
    UnixPipeReader().open_json_pipe(FIFO, update_configuration_from_emotions)

def update_configuration_from_emotions(emotions):
    global angle_grid, resolution, num_cols, num_rows, grid_scale_factor, left_x, right_x, top_y, bottom_y, lines, line_length

    for emotion in emotions:
        particles = FlowParticleFactory.generate_particles_from_emotion_payload(emotion)
        print("Adding {} new particles".format(len(particles)))
        for particle in particles:
            # CHANGE THIS
            line_key = random.randint(0, 999999999)
            lines[line_key] = particle
        
