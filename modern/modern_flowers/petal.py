class Petal():

    def __init__(self, x: float, y: float, curr_radius: float, color):
        self.x = x
        self.y = y
        self.curr_radius = curr_radius
        self.target_radius = random(target_radius + 50, target_radius + 200);
        self.speed = speed
        self.color = color

    def draw(self, opacity: float) -> None:
        ellipse(self.x, self.y, )
