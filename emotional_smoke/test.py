import sys

sys.path.append('/Users/devonperoutky/Development/processing/utilities')
sys.path.append('/Users/devonperoutky/Development/processing/utilities/ds')

from color_space.color_space_builder import ColorSpaceBuilder
from color_space.color_space_explorer import ColorSpaceExplorer
from color_space.coordinate import Coordinate

# Constants
node_size = 1 # The size of the point to draw
grid_height = 20
grid_width = 20

# Stats
total_pixels_colored = 0

# Initialize
starting_coord = Coordinate(0, 0, color(0,0, 0))
print("Starting Coordinate {}".format(starting_coord))
color_space = ColorSpaceBuilder.build_RGB_color_space(grid_height * grid_width)
color_space.space.rebalance()
print("COLOR SPACE has {} entries".format(len(list(color_space.space.inorder()))))
for node in color_space.space.inorder():
    print(node.data)

def setup():
    # size(grid_height, grid_width)
    fullScreen()
    background(255, 255, 255)
    noStroke()
    frameRate(12)
    noLoop()


def draw():
    row = range(grid_width)
    grid = [[x + (y*len(row)) for x in row] for y in range(grid_height)]
    for row_idx, row in enumerate(grid):
        for col_idx, cell  in enumerate(row):
            # print("EVALUATING ({}, {}) aka {}".format(row_idx, col_idx, cell))
            if (row_idx == 0 and col_idx == 0):
                grid[row_idx][row_idx] = starting_coord
                continue
            previous_coordinate = grid[row_idx - 1][grid_width-1] if col_idx == 0 else grid[row_idx][col_idx - 1]
            next_color = color_space.pop_most_similar_color([previous_coordinate])
            RED_VALUE = next_color >> 16 & 0xFF
            BLUE_VALUE = next_color & 0xFF
            GREEN_VALUE = next_color >> 8 & 0xFF
            print("NEXT COLOR ({}, {}, {})".format(RED_VALUE, GREEN_VALUE, BLUE_VALUE))
            new_coordinate = Coordinate(col_idx, row_idx, next_color)
            grid[row_idx][col_idx] = new_coordinate

        print("DRAWING {}".format(cell))
        # curr_coord = grid[grid_x][grid_y]
        draw_point(cell, 10)

def draw_point(node, node_size):
    fill(node.COLOR)
    square(node.X * node_size * 1.5, node.Y * node_size * 1.5, node_size)
