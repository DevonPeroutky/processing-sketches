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
    def __init__(self, x, y, length, angle, life):
        self.x = x
        self.y = y
        self.length = length
        self.angle = angle
        self.life = life
        self.life_remaining = life

    def draw(self):
        # calc new color using opacity from life_remaining 
        opacity = max(round(float(self.life_remaining) / self.life, 1), 0)

        opacity_to_hexidecimal = {
            0: 0x00FFFFFF,
            .1: 0x1A000000,
            .2: 0x33000000,
            .3: 0x4D000000,
            .4: 0x66000000,
            .5: 0x80000000,
            .6: 0x99000000,
            .7: 0xB3000000,
            .8: 0xCC000000,
            .9: 0xE6000000,
            1: 0xFF000000
        }
        hex_opacity = opacity_to_hexidecimal.get(opacity, opacity_to_hexidecimal[1])
        hexidecimal_color = "0x{}000000".format(hex_opacity)

        # stroke(hex_opacity)
        stroke(opacity_to_hexidecimal.get(1))
        strokeWeight(.6)
        draw_vector(self.x, self.y, self.length, self.angle)

    def decay(self, decay_rate):
        self.life_remaining = max(self.life_remaining - decay_rate, 0)

    def is_dead(self):
        return self.life_remaining < 1

class FlowLine:

    def __init__(self, x, y, color, max_length):
        self.x = x
        self.y = y
        self.curr_length = 0
        self.color = color
        self.max_length = max_length
        self.life = max_length
        self.vectors = [] * max_length

    def is_dead(self):
        return all([v.is_dead() for v in self.vectors])

    def _spawn_new_segment(self, angle_grid, resolution, left_x, top_y):
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

        # New LineSegment
        life_span = self.max_length
        line_segment = FlowLineSegment(self.x, self.y, step_size, grid_angle, life_span)
        line_segment.draw()
        self.vectors.append(line_segment)

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
        self.curr_length += 1

    def _rerender(self):
        return [vector.draw() for vector in self.vectors if not vector.is_dead()]

    def _decay_segments(self):
        decay_amount = min(self.max_length - self.life + 1, self.max_length)
        for i in range(0, decay_amount):
            self.vectors[i].decay(decay_rate=1)

    def iterate(self, angle_grid, resolution, left_x, top_y):
        if (self.curr_length < self.max_length):
            self._spawn_new_segment(angle_grid, resolution, left_x, top_y)
        else:
            self._decay_segments()
        
        # print([v.life_remaining for v in self.vectors])
        self.life = self.life - 1
        self._rerender()
