"""
TODO:
- Make this an abstract class?
- API for drawing_vector with varying color and opacity?????

"""
        
# TODO: MOVE THIS TO UTILITY
def draw_vector(cx, cy, len, angle):
  pushMatrix()
  translate(cx, cy)
  rotate(angle)
  line(0,0,len, 0)
  popMatrix()

class Shape:

    def __init__(self, x, y, decay_rate, color):
        self.x = x
        self.y = y
        self.decay_rate = decay_rate
        self.color = color

    def update(self, angle_grid):
        pass


class FlowLineSegment:
    def __init__(self, x, y, length, angle, life_remaining):
        self.x = x
        self.y = y
        self.length = length
        self.angle = angle
        self.life_remaining = life_remaining

    def draw_next_step(self):
        self.life_remaining = self.life_remaining - 1

        # calc new color using opacity from life_remaining 
        # fill(new_color)
        draw_vector(self.x, self.y, self.length, self.angle)

    def is_dead(self):
        return self.life_remaining < 1


class FlowLine:
    def __init__(self, x, y, decay_rate, color, max_length):
        self.x = x
        self.y = y
        self.curr_length = 0
        self.segment_life_span = 2 * max_length
        self.color = color
        self.max_length = max_length
        self.vectors = [] * max_length
        self.alive = True

    def is_dead(self):
        return all([v.is_dead() for v in self.vectors])

    def draw_next_step(self, angle_grid, resolution, left_x, top_y):
        if (self.curr_length >= self.max_length):
            self.decompose()
        else:
            step_size = resolution

            fill(self.color)

            # Determine angle
            x_offset = self.x - left_x
            y_offset = self.y - top_y
            column_index = int(x_offset / resolution)
            row_index = int(y_offset / resolution)
            row_index = row_index if row_index < len(angle_grid) else len(angle_grid) - 1
            column_index = column_index if column_index < len(angle_grid[row_index]) else len(angle_grid[row_index]) - 1
            grid_angle = angle_grid[row_index][column_index]

            # New LineSegment
            line_segment = FlowLineSegment(self.x, self.y, step_size, grid_angle, self.segment_life_span)
            line_segment.draw_next_step()
            self.vectors.append(line_segment)

            # Iterate
            x_step = step_size * cos(grid_angle)
            y_step = step_size * sin(grid_angle)
            self.x = self.x + x_step
            self.y = self.y + y_step
            self.curr_length += 1

    def decompose(self):
        for vector in self.vectors:
            vector.draw_next_step()

