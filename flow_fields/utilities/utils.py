def visualize_flow_field(angle_grid, num_rows, num_cols, resolution):
    for row in range(0, num_rows):
        for col in range(0, num_cols):
            x = col * resolution
            y = row * resolution
            strokeWeight(.7)
            draw_vector(x, y, resolution, angle_grid[row][col])


def draw_vector(cx, cy, len, angle):
    pushMatrix()
    translate(cx, cy)
    rotate(angle)
    line(0,0,len, 0)
    popMatrix()
