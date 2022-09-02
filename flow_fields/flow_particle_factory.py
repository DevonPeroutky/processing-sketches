import random
from particle import FlowParticle

class FlowParticleFactory:
    def __init__(self, max_lines):
        self.particles = {}
        self.max_lines = max_lines

    def iterate(self, angle_grid, resolution, left_x, top_y):
        strokeWeight(.6)
        for (key, particle) in self.particles.items():
            if particle.is_finished(left_x, top_y):
                self.particles.pop(key)
            else:
                particle.iterate(angle_grid, resolution, left_x, top_y)

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
        assert face_location
        assert emotion

        # TODO: CHANGE THIS
        max_length = 500

        face_center_x = face_location['x']
        face_center_y = face_location['y']
        face_width = int(round(face_location['w']))
        face_height = int(round(face_location['h']))

        # Mapping the position of the face in the webcam to the corresponding position in the canvas
        # TODO. Send this info via the pipe instead of hardcoding it.
        particle_x = int(round(map(face_center_x, 1275, 0, 0, 1000)))
        particle_y = int(round(map(face_center_y, 720, 0, 0, 1000)))
        print("Mapping ({}, {}) --> ({}, {})".format(face_center_x, face_center_y, particle_x, particle_y))

        # TODO: Make this better
        max_speed = random.randint(2, 4)
        starting_velocity = random.randint(1, 2)

        particles_to_instantiate = [(emotion, int(round(value))) for emotion, value in emotion.items() if value > .5]
        for (emotion, quantity) in particles_to_instantiate:
            print("Creating {} {} particles at ({}, {})".format(quantity, emotion, particle_x, particle_y))
            for _ in range(0, quantity):

                # Random distribute new particles in face box
                x_offset = random.randint(int(round(-face_width / 4)), int(round(face_width / 4)))
                y_offset = random.randint(int(round(-face_height / 4)), int(round(face_height / 4)))
                particle = FlowParticle(x=particle_x + x_offset, y=particle_y + y_offset, starting_velocity=starting_velocity, max_speed=max_speed, emotion=emotion, max_length=max_length)

                line_key = "{}-{}".format(frameCount, i)
                self.particles[line_key] = particle

    def spawn_new_particles(self, quantity, left_x, right_x, top_y, bottom_y, line_length, emotion):
        particles_to_create = max(0, self.max_lines - len(self.particles.keys()))
        frozenFrameCount = frameCount

        for i in range(0, min(quantity, particles_to_create)):
            line_key = "{}-{}".format(frozenFrameCount, i)
            self.particles[line_key] = FlowParticle(x=random.randint(left_x, right_x), y=random.randint(top_y, bottom_y), starting_velocity=2, max_speed=2, emotion=emotion, max_length=random.randint(0, line_length))
