emotional_palette = {
    "surprise": (141, 170, 157), # TEAL-ISH
    "happy": (52, 98, 63),       # GREEN
    "neutral": (242, 213, 248),  # GRAY
    "angry": (246, 16, 103),     # RED
    "sad": (51, 101, 138),       # BLUE
    "disgust": (82, 43, 71),     # PURPLE
    "fear": (244, 157, 110),     # ORANGE
}

class EmotionalColorPalette:
    @staticmethod
    def determine_color_from_emotion(emotion):
        return emotional_palette.get(emotion) or emotional_palette.get("neutral")
    
