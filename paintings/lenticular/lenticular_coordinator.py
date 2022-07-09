
class LenticularCoordinator(object):
    def __init__(self, width, height, images):
        self.images = images
        (self.left_img, self.right_img) = [loadImage(img) for img in self.images]
        self.left_img.loadPixels()
        self.right_img.loadPixels()

        print("Loaded imags")
        print(len(self.left_img.pixels))
        print(len(self.right_img.pixels))

        self.width = width
        self.height = height
        self.fov_threshold = 45
        self.pixel_matrix = [color(255, 255, 255)] * (self.height * self.width)

        # Load matrix with pixels from both images
        for i in range(self.width * self.height):
            col = i % self.width
            self.pixel_matrix[i] = self.left_img.pixels[i] if (col % 2 == 0) else self.right_img.pixels[i]


    def render_image_pixels(self, x_pos):
        """
        Given the distance_from_camera and angle_from_camera, return the breakdown of pixels via a 2D-array

        """
        for i in range(self.width * self.height):
            col = i % self.width

            # If in FOV
            if abs(x_pos - col) <= self.fov_threshold:
                self.pixel_matrix[i] = self.left_img.pixels[i] if (col % 2 == 0) else self.right_img.pixels[i]

            # If outside right
            elif x_pos > col:
                self.pixel_matrix[i] = self.left_img.pixels[i]

            # If outside left
            elif x_pos < col:
                self.pixel_matrix[i] = self.right_img.pixels[i]

        return self.pixel_matrix
