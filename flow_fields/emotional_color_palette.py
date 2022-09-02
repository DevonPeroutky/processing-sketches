import random

emotional_palette = {
    "surprise": (141, 170, 157), # TEAL-ISH
    "happy": (52, 98, 63),       # GREEN
    "neutral": (0, 0, 0),        # GRAY
    # "neutral": (242, 213, 248),# GRAY
    "angry": (246, 16, 103),     # RED
    "sad": (51, 101, 138),       # BLUE
    "disgust": (82, 43, 71),     # PURPLE
    "fear": (244, 157, 110),     # ORANGE
}

class EmotionalColorPalette:
    @staticmethod
    def determine_color_from_emotion(emotion):
        return emotional_palette.get(emotion) or emotional_palette.get("neutral")


    @staticmethod
    def determine_color_from_position(x, y):
        rando = random.randint(0, y)
        index = int(round(map(rando, 0, height, 0, 6)))
        if index == 0:
            return emotional_palette.get("surprise")
        if index == 1:
            return emotional_palette.get("happy")
        if index == 2:
            return emotional_palette.get("neutral")
        if index == 3:
            return emotional_palette.get("angry")
        if index == 4:
            return emotional_palette.get("sad")
        if index == 5:
            return emotional_palette.get("disgust")
        if index >= 6:
            return emotional_palette.get("fear")
