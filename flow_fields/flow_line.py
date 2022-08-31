import random

class FlowCurveVertex:
    def __init__(self, x, y, color, life):
        self.x = x
        self.y = y
        self.color = color
        self.life = life
        self.life_remaining = life
        
    

class FlowCurve:

    def __init__(self, x, y, color, max_length, angle_grid, resolution, left_x, top_y):
        # https://py.processing.org/reference/curveVertex.html
        self.min_length = 5
        assert(max_length > self.min_length)

        self.color = color
        self.x = x
        self.y = y
        self.vertexes = []
        self.max_length = max_length


        for i in range(0, self.min_length):
            self.iterate(angle_grid=angle_grid, resolution=resolution, left_x=left_x, top_y=top_y)


    def add_new_vertex(self, x, y, color, life):
        new_vertex = FlowCurveVertex(x, y, color, life)
        self.vertexes.append(new_vertex)

    def iterate(self, angle_grid, resolution, left_x, top_y):
        if len(self.vertexes) < self.max_length:
            step_size = resolution

            fill(self.color)

            # Determine angle
            x_offset = self.x - left_x
            y_offset = self.y - top_y
            column_index = int(x_offset / resolution)
            row_index = int(y_offset / resolution)
            row_index = max(0, row_index) if row_index < len(angle_grid) else len(angle_grid) - 1
            column_index = max(0, column_index) if column_index < len(angle_grid[row_index]) else len(angle_grid[row_index]) - 1
            grid_angle = angle_grid[row_index][column_index]

            # Iterate
            x_step = step_size * cos(grid_angle)
            y_step = step_size * sin(grid_angle)

            # Debug
            # print("X: {}".format(self.x))
            # print("Y: {}".format(self.y))
            # print("GRID ANGLE: {} --> {}".format(grid_angle, degrees(grid_angle)))
            # print("({}, {}) + ({}, {})".format(self.x, self.y, x_step, y_step))

            self.x = self.x + x_step
            self.y = self.y + y_step
            self.add_new_vertex(self.x, self.y, self.color, self.max_length)
            self.draw()

    def draw(self):
        noFill()
        strokeWeight(.5)
        beginShape()
        for vertex in self.vertexes:
            curveVertex(vertex.x, vertex.y)
        endShape()

