class AngleGrid:
    def __init__(self, width, height, grid_scale_factor, resolution_factor, z_noise_offset, noise_step):
        # Set size of flow field to be bigger than the canvas for aesthetics
        self.left_x = int(width * (0-grid_scale_factor))
        self.right_x = int(width * (1 + grid_scale_factor))
        self.top_y = int(height * (0-grid_scale_factor))
        self.bottom_y = int(height * (1+ grid_scale_factor))

        self.resolution = int((self.right_x - self.left_x)  * resolution_factor)
        self.num_cols = int((self.right_x - self.left_x) / self.resolution)
        self.num_rows = int((self.bottom_y - self.top_y) / self.resolution)

        self.angle_grid = [[0 for x in range(self.num_cols)] for y in range(self.num_rows)]
        self._build_angle_grid(z_noise_offset=z_noise_offset, noise_step=noise_step)
        print(self)

    def __str__(self):
        return "Angle Grid ({} x {}) w/resolution: {}, and offsets are {}, {}".format(self.num_rows, self.num_cols, self.resolution, self.left_x, self.top_y)

    def visualize_flow_field(self):
        for row in range(0, self.num_rows):
            for col in range(0, self.num_cols):
                x = (col * self.resolution) + self.left_x
                y = (row * self.resolution) + self.top_y
                strokeWeight(.7)
                # textSize(16)
                fill(0, 0, 0)
                # text("({}, {})".format(row, col), x+(self.resolution/3), y + (self.resolution /3))
                # text(degrees(self.angle_grid[row][col]), x+(self.resolution/2), y+(self.resolution/2))
                noFill()
                # square(x, y, self.resolution)
                AngleGrid.draw_vector(x, y, self.resolution, self.angle_grid[row][col])


    @staticmethod
    def draw_vector(cx, cy, len, angle):
        # Push to the center for visibility
        offset = len/2

        pushMatrix()
        translate(cx + offset, cy + offset)
        rotate(angle)
        circle(0, 0, 2)
        line(0, 0, len / 2, 0)
        # line(len, 0, 0, 0)
        popMatrix()

    def fetch_angle_vector_from_position(self, x, y):
        x_offset = x - self.left_x
        y_offset = y - self.top_y
        column_index = int(x_offset / self.resolution)
        row_index = int(y_offset / self.resolution)
        row_index = max(0, row_index) if row_index < len(self.angle_grid) else len(self.angle_grid) - 1
        column_index = max(0, column_index) if column_index < len(self.angle_grid[row_index]) else len(self.angle_grid[row_index]) - 1
        grid_angle = self.angle_grid[row_index][column_index]
        flow_field_force = PVector.fromAngle(grid_angle)
        return flow_field_force
    
    def _build_angle_grid(self, z_noise_offset, noise_step):
        y_noise_offset = 0
        for row in range(0, self.num_rows):
            x_noise_offset = 0
            for col in range(0, self.num_cols):
                angle = noise(x_noise_offset, y_noise_offset, z_noise_offset) * PI * 2
                self.angle_grid[row][col] = angle
                x_noise_offset += noise_step
            y_noise_offset += noise_step

