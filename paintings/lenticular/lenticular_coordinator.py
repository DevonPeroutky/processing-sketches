
class LenticularCoordinator(object):
    def __init__(self, width, height):
        # self.images = images
        # (left_img, right_img) = self.images
        red = color(235, 64, 52)
        blue = color(29, 61, 222)

        self.width = width
        self.height = height
        self.fov_threshold = 45
        self.pixel_matrix = [color(255, 255, 255)] * (self.height * self.width)

        # Load matrix with pixels from both images
        for i in range(self.width * self.height):
            col = i % self.width
            self.pixel_matrix[i] = red if (col % 2 == 0) else blue


    def render_image_pixels(self, x_pos):
        """
        Given the distance_from_camera and angle_from_camera, return the breakdown of pixels via a 2D-array

        """
        print("X POS: %s" % x_pos)
        red = color(235, 64, 52)
        blue = color(29, 61, 222)
        for i in range(self.width * self.height):
            col = i % self.width

            # If in FOV
            if abs(x_pos - col) <= self.fov_threshold:
                self.pixel_matrix[i] = red if (col % 2 == 0) else blue

            # If outside right
            elif x_pos > col:
                self.pixel_matrix[i] = red

            # If outside left
            elif x_pos < col:
                self.pixel_matrix[i] = blue

        return self.pixel_matrix
