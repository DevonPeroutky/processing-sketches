
class FlowParticle:
    def __init__(self, x, y, max_speed, color, max_length):
        self.max_length = max_length
        self.pos = PVector(x, y)
        self.velocity = PVector(0, 0)
        self.acc = PVector(0, 0)
        self.color = color
        self.max_speed = max_speed
        self.length = 0

        self.prev_pos = self.pos.copy()


    def iterate(self, angle_grid, resolution, left_x, top_y):

        # Determine angle
        x_offset = self.pos.x - left_x
        y_offset = self.pos.y - top_y
        column_index = int(x_offset / resolution)
        row_index = int(y_offset / resolution)
        row_index = max(0, row_index) if row_index < len(angle_grid) else len(angle_grid) - 1
        column_index = max(0, column_index) if column_index < len(angle_grid[row_index]) else len(angle_grid[row_index]) - 1
        grid_angle = angle_grid[row_index][column_index]

        # Apply Force
        flow_field_force = PVector.fromAngle(grid_angle)
        self.acc.add(flow_field_force)

        # Apply Accelaration
        self.velocity.add(self.acc)
        self.velocity.limit(self.max_speed)
        self.pos.add(self.velocity)

        # Reset Acceleration
        self.acc.mult(0)

        # Draw
        # stroke(self.color)
        stroke(199, 13, 58, 80);
        strokeWeight(.3)
        line(self.pos.x, self.pos.y, self.prev_pos.x, self.prev_pos.y)

        # Update
        self.prev_pos.x = self.pos.x
        self.prev_pos.y = self.pos.y
        self.length += self.velocity.mag()

    def is_finished(self, left_x, top_y):
        return self.is_out_of_bounds(left_x=left_x, top_y=top_y) or self.length > self.max_length
        

    def is_out_of_bounds(self, left_x, top_y):
        x_pos = self.pos.x - left_x
        y_pos = self.pos.y - top_y
        return x_pos < left_x or x_pos > width - left_x or y_pos < top_y or y_pos > height - top_y


