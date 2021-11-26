class Flower:

    #def __init__(self, x: float, y: float, curr_radius: float, curr_length: float, growth_rate: float, decay_rate: float, target_length: float, target_radius: float, life: float, color):
    def __init__(self, x, y, curr_radius, curr_length, curr_stem_radius, growth_rate, decay_rate, target_length, target_radius, target_stem_radius, life, color):
        self.x = x
        self.y = y

        self.growth_rate = growth_rate
        self.decay_rate = decay_rate

        self.curr_stem_radius = curr_stem_radius
        self.target_stem_radius = target_stem_radius

        self.curr_radius = curr_radius
        self.curr_length = curr_length

        self.target_radius = target_radius
        self.target_length = target_length

        self.life = life
        self.color = color

        self.stem_offset = self.target_radius / 12

    def is_full_grow(self):
        return self.target_radius == self.curr_radius and self.curr_length == self.target_length

    def is_dead(self):
        return self.life != 0

    def draw(self):
        up = -1 if self.y > height / 2 else 1

        # Draw the stemhead aka seed
        noStroke()
        fill(0, 0, 0, 255)
        ellipse(self.x, self.y + self.stem_offset, self.curr_stem_radius, self.curr_stem_radius)

        if (self.curr_stem_radius == self.target_stem_radius):
            # Draw the stem
            noFill()
            stroke(0, 0, 0)
            line(self.x, self.y + self.stem_offset, self.x, self.y + (self.curr_length * up))

            # Draw the petal
            noStroke()
            fill(420, 69, 18, self.life)
            ellipse(self.x, self.y, self.curr_radius, self.curr_radius)


    def __repr__(self):
        return "<Flower x:%s y:%s radius:%s length: %s life: %s>" % (self.x, self.y, self.curr_radius, self.curr_length, self.life)

    def __str__(self):
        opacity = map(self.life, 0, 100, 0, 1)
        return "Flower (%s, %s) [(%s, %s) --> (%s, %s)]: Life is %s --> %s" % (self.x, self.y, self.curr_radius, self.curr_length, self.target_radius, self.target_length, self.life, opacity)
