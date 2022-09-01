from particle import FlowParticle
  
emotional_palette = {
    "surprise": "#fad089",
    "happy": "#1A9348",
    "neutral": "#3b8183",
    "angry": "#ed303c",
    "sad": "#004444",
    "disgust": "#3FF000",
    "fear": "#f5634a",
}

class FlowParticleFactory:
    @staticmethod
    def determine_color_from_emotion(emotion):
        return emotional_palette.get(emotion, "#ff9c5b")
    
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
        print("Payload")
        print(payload)
        emotion = payload.get('emotion')
        face_location = payload.get('region')
        assert face_location
        assert emotion

        # TODO: CHANGE THIS
        max_length = 50

        face_center_x = face_location['x']
        face_center_y = face_location['y']

        # Mapping the position of the face in the webcam to the corresponding position in the canvas
        # TODO. Send this info via the pipe instead of hardcoding it.
        particle_x = int(round(map(face_center_x, 0, 1275, 0, 1000)))
        particle_y = int(round(map(face_center_y, 0, 720, 0, 1000)))

        particles_to_instantiate = [(FlowParticleFactory.determine_color_from_emotion(emotion), int(round(value))) for emotion, value in emotion.items()]
        particles = []
        for (color, quantity) in particles_to_instantiate:
            print("Creating {} {} particles at ({}, {})".format(quantity, color, particle_x, particle_y))
            for _ in range(0, quantity):
                particle = FlowParticle(x=particle_x, y=particle_y, max_speed=2, color=color, max_length=max_length)
                particles.append(particle)

        return particles
