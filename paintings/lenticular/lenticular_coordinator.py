
class LenticularCoordinator(object):
    def __init__(self, width, height, images):
        self.images = images
        (left_img, right_img) = [loadImage(img) for img in self.images]
        left_img.loadPixels()
        right_img.loadPixels()

        self.left_img_pixels = left_img.pixels
        self.right_img_pixels = right_img.pixels
        # self.left_img_pixels = [color(66, 135, 245)] * (width * height)
        # self.right_img_pixels = [color(245, 69, 66)] * (width * height)

        self.width = width
        self.height = height
        self.fov_threshold = 30


    def calc_pixel_diffs(self, x_pos, last_x_pos):
        """
        Determine indexes of pixels that need to be re-evaluated.

        """
        min_x_pos = max(min(x_pos, last_x_pos) - self.fov_threshold, 0)
        max_x_pos = min(max(x_pos, last_x_pos) + self.fov_threshold, self.width)
        return [x+ (self.width * y) for y in range(self.height) for x in range(min_x_pos, max_x_pos)]


    def update_img_pixels(self, img, new_pixels, x_pos):
        """
        Given the distance_from_camera and angle_from_camera, return the breakdown of pixels via a 2D-array

        """
        print("UPDATING FOR x_pos %s" % x_pos)
        for i in new_pixels:
            col = i % self.width

            # If in FOV
            if abs(x_pos - col) <= self.fov_threshold:
                img.pixels[i] = self.left_img_pixels[i] if (col % 2 == 0) else self.right_img_pixels[i]

            # If outside right
            elif x_pos > col:
                img.pixels[i] = self.right_img_pixels[i]

            # If outside left
            elif x_pos < col:
                img.pixels[i] = self.left_img_pixels[i]

        return img

    # def render_image_pixels(self, x_pos):
    #     """
    #     Given the distance_from_camera and angle_from_camera, return the breakdown of pixels via a 2D-array

    #     """
    #     for i in range(self.width * self.height):
    #         col = i % self.width

    #         # If in FOV
    #         if abs(x_pos - col) <= self.fov_threshold:
    #             self.pixel_matrix[i] = self.left_img.pixels[i] if (col % 2 == 0) else self.right_img.pixels[i]

    #         # If outside right
    #         elif x_pos > col:
    #             self.pixel_matrix[i] = self.left_img.pixels[i]

    #         # If outside left
    #         elif x_pos < col:
    #             self.pixel_matrix[i] = self.right_img.pixels[i]

    #     return self.pixel_matrix
