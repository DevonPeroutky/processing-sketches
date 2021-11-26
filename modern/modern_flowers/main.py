# Based on https://openprocessing.org/sketch/617407

from flower import Flower
flowers = []
colorList = ["#9f928a", "#9f928a", "#fd682d", '#fd682d', '#f9ae17', '#f9ae17', '#f9ae17','#95cebd', '#95cebd', '#116f6f', '#116f6f', '#d7d7bd', '#ddc5ab', '#fc9946', '#454344']

def setup():
    global flowers

    size(800, 800)
    blendMode(MULTIPLY)
    background(255)
    ellipseMode(CENTER)
    smooth()
    strokeCap(ROUND)
    frameRate(24)
    flowers.append(spawn_flower())

def draw():
    global flowers
    background(255)
    blendMode(REPLACE)
    noStroke()
    fill(255)
    rect(0, 0, width, height)
    blendMode(MULTIPLY)

    # How frequent to spawn flowers (in terms of # of frames)
    spawn_rate = 40

    # Create flower every _____ frame
    if (frameCount % spawn_rate == 0):
        flowers.append(spawn_flower())

    new_flowers = [update_flower(flower) for flower in filter(lambda f: f.is_dead(), flowers)]
    for flower in new_flowers:
        flower.draw()
    flowers = new_flowers
    
def spawn_flower():
    x = random(width)
    y = random(height)
    growth_rate = random(2, 5)
    decay_rate = random(1, 3)
    flower_color = color(420, 69, 0)
    life = 255
    target_radius = random(50, 200)
    target_length = random(height / 16 + target_radius, (height / 8 ) - y + target_radius)
    stem_target_radius = random(.15, .45) * target_radius

    return Flower(x, y, 0, 0, 0, growth_rate, decay_rate, target_length, target_radius, stem_target_radius, life, flower_color)


def update_flower(flower):
    new_stem_radius = min(flower.target_stem_radius, flower.curr_stem_radius + flower.growth_rate)
    new_life = flower.life
    new_length = flower.curr_length
    new_radius = flower.curr_radius

    if new_stem_radius == flower.target_stem_radius:
        new_life = max(0, flower.life - flower.decay_rate) if flower.is_full_grow() else flower.life
        new_length = min(flower.target_length, flower.curr_length + flower.growth_rate)
        new_radius = min(flower.target_radius, flower.curr_radius + flower.growth_rate)
    
    return Flower(flower.x, flower.y, new_radius, new_length, new_stem_radius, flower.growth_rate, flower.decay_rate, flower.target_length, flower.target_radius, flower.target_stem_radius, new_life, flower.color)
