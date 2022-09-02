import random
from particle import FlowParticle
  
emotional_palette = {
    "surprise": color(141, 170, 157),  # DONE: TEAL-ISH
    "happy": color(52, 98, 63),     # DONE: GREEN
    "neutral": color(242, 213, 248),   # DONE: GRAY
    "angry": color(246, 16, 103),     # DONE: RED
    "sad": color(51, 101, 138),       # DONE: BLUE
    "disgust": color(82, 43, 71),   # DONE: PURPLE
    "fear": color(244, 157, 110),      # DONE: ORANGE
}

class FlowParticleFactory:
    @staticmethod
    def determine_color_from_emotion(emotion):
        return emotional_palette.get(emotion) or emotional_palette.get("neutral")
    
    @staticmethod
    def generate_particles_from_emotion_payload(payload):
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

        particles_to_instantiate = [(emotion, int(round(value))) for emotion, value in emotion.items()]
        particles = []
        for (emotion, quantity) in particles_to_instantiate:
            print("Creating {} {} particles at ({}, {})".format(quantity, emotion, particle_x, particle_y))
            for _ in range(0, quantity):

                # Random distribute new particles in face box
                x_offset = random.randint(int(round(-face_width / 4)), int(round(face_width / 4)))
                y_offset = random.randint(int(round(-face_height / 4)), int(round(face_height / 4)))
                particle = FlowParticle(x=particle_x + x_offset, y=particle_y + y_offset, starting_velocity=starting_velocity, max_speed=max_speed, emotion=emotion, max_length=max_length)
                particles.append(particle)

        return particles
