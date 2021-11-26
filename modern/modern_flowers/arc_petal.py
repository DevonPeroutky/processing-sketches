class ArcPetal():

    def __init__(self, x: float, y: float, target_radius: float, start_init: float, end_init: float, speed: float, color):
        self.x = x
        self.y = y
        self.current_radius = 0
        self.target_radius = random(target_radius + 50, target_radius + 200 - start_init * 100);
        self.speed = speed
        self.color = color
        self.start = start_init
        self.end = end_init

    def draw(self, speed: float, decay_rate: float):
        pass
