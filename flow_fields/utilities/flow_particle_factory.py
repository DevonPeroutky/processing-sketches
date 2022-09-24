from emotional_color_palette import EmotionalColorPalette
import random
from particle import FlowParticle


class FlowParticleFactory:
    def __init__(self, max_lines, left_x, right_x, top_y, bottom_y):
        self.particles = {}
        self.max_lines = max_lines
        self.left_x = left_x
        self.right_x = right_x
        self.top_y = top_y
        self.bottom_y = bottom_y

    def iterate(self, angle_grid, reset=False):
        for (key, particle) in self.particles.items():
            if particle.is_finished(self.left_x, self.top_y):
                if reset:
                    particle.reset(angle_grid.left_x, angle_grid.top_y,
                                   EmotionalColorPalette.get_random_emotion())
                else:
                    self.particles.pop(key)
            else:
                particle.iterate(angle_grid)

    def generate_particles_from_emotion_payload(self, payload):
        """
        Example Payload:
        {
            'emotion': {
                'angry': 13.037654757499695,
                'disgust': 0.000244021202888689,
                'fear': 17.94908195734024,
                'happy': 1.0951195861252927e-05,
                'sad': 68.58017444610596,
                'surprise': 0.004346260902821086,
                'neutral': 0.4284909926354885
            },
            'dominant_emotion': 'sad',
            'region': {
                'x': 23,
                'y': 23,
                'w': 265,
                'h': 265
            }
        }
        """
        emotion = payload.get('emotion')
        face_location = payload.get('region')
        dominant_emotion = payload.get('dominant_emotion')
        assert face_location
        assert emotion
        assert dominant_emotion

        # Face Location
        face_width = int(round(face_location['w']))
        face_height = int(round(face_location['h']))
        face_center_x = face_location['x']
        face_center_y = face_location['y']

        # Mapping the position of the face in the webcam to the corresponding position in the canvas
        # TODO. Send the dimension via the pipe instead of hardcoding it.
        particle_x = int(round(map(face_center_x, 1280, 0, 0, 1000)))
        particle_y = int(round(map(face_center_y, 0, 720, 0, 1000)))

        # TODO: CHANGE/VARY THESE
        max_length = 1000
        max_speed = random.randint(5, 10)
        starting_velocity = random.randint(3, 5)
        creation_factor = .5
        opacity = 10

        particles_to_instantiate = [(emotion,
                                     int(round(value) * creation_factor))
                                    for emotion, value in emotion.items()
                                    if value > .5]
        buffer = max(0, self.max_lines - len(self.particles.keys()))
        for (emotion, quantity) in particles_to_instantiate:
            true_amount = min(quantity, buffer)
            print("Creating {} {} particles at ({}, {})".format(
                true_amount, emotion, particle_x, particle_y))
            for _ in range(0, true_amount):

                # Random distribute new particles in face box
                # x_offset = randomGaussian() * (face_width / 2)
                # y_offset = randomGaussian() * (face_height / 2)
                x = random.randint(self.left_x, self.right_x)
                y = random.randint(self.top_y, self.bottom_y)
                starting_angle = radians(random.randint(1, 360))
                particle = FlowParticle(
                    x=x,
                    y=y,
                    # x=particle_x + x_offset,
                    # y=particle_y + y_offset,
                    sensitivity=10,
                    starting_velocity=starting_velocity,
                    starting_angle=starting_angle,
                    max_speed=max_speed,
                    emotion=emotion,
                    max_length=max_length,
                    stroke_weight=40,
                    opacity=opacity)

                self.particles[id(particle)] = particle

    def build_layer_of_particles(self,
                                 quantity,
                                 line_length,
                                 emotion,
                                 stroke_weight,
                                 opacity,
                                 max_speed,
                                 starting_velocity,
                                 color=None):
        particles_to_create = min(
            quantity, max(0, self.max_lines - len(self.particles.keys())))

        # print("Creating {} particles".format(min(quantity, particles_to_create)))
        for _ in range(0, particles_to_create):
            particle = FlowParticle(
                x=random.randint(self.left_x, self.right_x),
                y=random.randint(self.top_y, self.bottom_y),
                sensitivity=10,
                starting_angle=radians(random.randint(1, 360)),
                starting_velocity=starting_velocity,
                max_speed=max_speed,
                emotion=emotion,
                max_length=line_length,
                stroke_weight=stroke_weight,
                opacity=opacity,
                color=color)
            self.particles[id(particle)] = particle

        return particles_to_create

    def spawn_new_reed_groups(self, reed_width, reed_quantity, left_x, top_y,
                              line_length, emotion):
        group_y = random.randint(top_y, height - top_y)
        group_x = random.randint(left_x, width - left_x)
        length = line_length
        for _ in range(0, reed_quantity):
            y = group_y + random.randint(0, reed_width)
            x = group_x + random.randint(0, reed_width)
            sensitivity = random.randint(1, 1000)
            particle = FlowParticle(x=x,
                                    y=y,
                                    sensitivity=sensitivity,
                                    starting_velocity=2,
                                    max_speed=5,
                                    emotion=emotion,
                                    max_length=length)
            self.particles[id(particle)] = particle
