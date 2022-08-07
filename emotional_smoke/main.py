import sys

sys.path.append('/Users/devonperoutky/Development/processing/utilities')
sys.path.append('/Users/devonperoutky/Development/processing/utilities/ds')

from color_space.color_space_builder import ColorSpaceBuilder
from color_space.color_space_explorer import ColorSpaceExplorer
from color_space.coordinate import Coordinate
import kdtree

# Constants
node_size = 1 # Don't change this
grid_height = 1120
grid_width = 1792

# Stats
total_pixels_colored = 0

# Initialize
# starting_coord = ColorSpaceExplorer.random_coordinate(grid_height, grid_width)
starting_coord = ColorSpaceExplorer.random_coordinate(grid_width, grid_height)
print(starting_coord)
print("Starting Coordinate {}".format(starting_coord))

# Instantiate globals
color_space = None
color_space_explorer = None



def setup():
    global color_space, color_space_explorer
    fullScreen()
    background(255, 255, 255)
    noStroke()
    frameRate(24)

    # Build Color Space from Image
    image = loadImage("../images/mount-tam-compressed.jpg")
    image.loadPixels()
    color_space = ColorSpaceBuilder.build_color_space_from_image(image.pixels)

    # Using the RGB Color Space
    # color_space = ColorSpaceBuilder.build_full_RGB_color_space(size=grid_height * grid_width)

    color_space.space.rebalance()
    print("COLOR SPACE has {} entries".format(len(list(color_space.space.inorder()))))
    color_space_explorer = ColorSpaceExplorer(color_space=color_space, height=grid_height, width=grid_width, starting_coord=starting_coord, node_size=node_size)


def draw():
    global color_space_explorer, total_pixels_colored, node_size
    nodes_to_color = color_space_explorer.BFS_iteration(25)
    total_pixels_colored += len(nodes_to_color)
    for node in nodes_to_color:
        draw_point(node=node, node_size=node_size)


def draw_point(node, node_size):
    fill(node.COLOR)
    square(node.X, node.Y, node_size)
