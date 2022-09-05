import random

# HSB
emotional_palette = {
    "neutral": (0, 0, 87),# GRAY
    "angry": (338, 95, 76),     # RED
    "sad": (209, 100, 64),       # BLUE
    "happy": (134, 100, 38),       # GREEN
    "surprise": (153, 100, 67), # TEAL-ISH
    "disgust": (317, 100, 32),     # PURPLE
    "fear": (21, 100, 96),     # ORANGE
    # "black": (0, 0, 0),
    # "white": (0, 0, 100),
}

class EmotionalColorPalette:
    @staticmethod
    def determine_color_from_emotion(emotion):
        color = emotional_palette.get(emotion)
        assert color
        return color

    @staticmethod
    def get_random_emotion():
        random_emotion = "neutral"
        while random_emotion == "neutral":
            keys = emotional_palette.keys()
            index = random.randint(0, len(keys)-1)
            random_emotion = keys[index]
        return random_emotion


    @staticmethod
    def determine_color_from_position(x, y):
        index = int(round(map(y, 0, height, 0, 5)))
        if index <= 0:
            return emotional_palette.get("surprise")
        if index == 1:
            return emotional_palette.get("happy")
        if index == 2:
            return emotional_palette.get("angry")
        if index == 3:
            return emotional_palette.get("sad")
        if index == 4:
            return emotional_palette.get("disgust")
        if index >= 5:
            return emotional_palette.get("fear")

    @staticmethod
    def determine_color_from_gradient(x, y):
        visible_y = min(max(0, y), height)
        r = random.randint(visible_y, visible_y+100)

        noise_injection = .1

        colorA = emotional_palette.get("fear")
        colorB = emotional_palette.get("happy")
        colorC = emotional_palette.get("surprise")
        
        probA = map(visible_y, 0, 1000, 1, .5)
        probB = 1 - probA
        print("{} -> {}".format(y, probA))
        return EmotionalColorPalette.choices([colorA, colorB], [probA, probB])

        # index = map(r, 0, height, 0, 6)
        # if index <= 1:
        #     return emotional_palette.get("surprise")
        # if index <= 2:
        #     return emotional_palette.get("happy")
        # if index <= 3:
        #     return emotional_palette.get("angry")
        # if index <= 4:
        #     return emotional_palette.get("sad")
        # if index <= 5:
        #     return emotional_palette.get("disgust")
        # if index <= 6:
        #     return emotional_palette.get("fear")
        # return emotional_palette.get("neutral")

    @staticmethod
    def choices(population, weights):
        """
        Randomly selects an element from the population given the probability distributions specified by the weights.

        Ex. [.2, .7, .1]
        
        0 - 0.2
        0.2 - 0.9
        0.9 - 1

        """
        assert(sum(weights)) == 1
        assert(len(weights) == len(population))
        r = random.random()

        curr_propability = 0
        for i, probability in enumerate(weights):
            curr_propability = curr_propability + probability

            if r <= curr_propability:
                return population[i]
        assert(False)
