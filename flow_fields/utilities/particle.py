"""
Variables
    - Colors of lines/shapes    <-- Emotion
    - Length of lines/shapes    <-- The degree of cohesiveness of the emotion? Constant for now
    - Lifespan of the lines     <-- Magnitude of the emotion. Tie into Length? Constant for now
    - Spawn point               <-- Face location
    - Flow field angles         <-- ???
    - Opacity of lines          <-- Decay over Time
"""

from random import randint, random
from emotional_color_palette import EmotionalColorPalette

class FlowParticle:
    def __init__(self, x, y, max_length, emotion, sensitivity=1, starting_velocity=2, max_speed=3, stroke_weight=1, opacity=10):
        self.max_length = max_length
        self.pos = PVector(x, y)

        self.velocity = PVector(0, 0)
        self.sensitivity = sensitivity
        self.emotion = emotion
        self.max_speed = max_speed
        self.length = 0
        self.prev_pos = self.pos.copy()
        self.stroke_weight = stroke_weight
        self.opacity = opacity
        self.color = self._determine_color(emotion=emotion, x=x, y=y)

    def __str__(self):
        return "Position ({}, {}) Angle: {}, Magnitude: {}, Velocity: {}, Emotion: {}".format(self.pos.x, self.pos.y, degrees(self.pos.heading()), self.pos.mag(), self.velocity.mag(), self.emotion)

    def _is_out_of_bounds(self, left_x, top_y):
        x_pos = self.pos.x - left_x
        y_pos = self.pos.y - top_y
        return x_pos < left_x or x_pos > width - left_x or y_pos < top_y or y_pos > height - top_y

    def _determine_color(self, emotion, x, y):
        color_from_emotion = EmotionalColorPalette.determine_color_from_emotion(emotion)
        # color_from_position = EmotionalColorPalette.determine_color_from_position(x, y)
        # color_from_gradient = EmotionalColorPalette.determine_color_from_gradient(x, y)
        return color_from_emotion

    def _apply_vector(self, vector):
        self.velocity.add(vector)
        self.velocity.limit(self.max_speed)
        self.pos.add(self.velocity)

    def draw(self):
        # strokeCap(SQUARE)
        strokeWeight(self.stroke_weight)
        stroke(self.color[0], self.color[1], self.color[2], self.opacity)
        circle(self.pos.x, self.pos.y, 1)
        line(self.pos.x, self.pos.y, self.prev_pos.x, self.prev_pos.y)


    def iterate(self, angle_grid):

        # Determine Force from Flow Field
        flow_field_force = angle_grid.fetch_angle_vector_from_position(self.pos.x, self.pos.y)
        flow_field_force.mult(self.sensitivity)

        # Apply Accelaration
        self._apply_vector(flow_field_force)

        # Draw
        self.draw()

        # Update
        self.prev_pos.x = self.pos.x
        self.prev_pos.y = self.pos.y
        self.length += self.velocity.mag()

    def is_finished(self, left_x, top_y):
        return self._is_out_of_bounds(left_x=left_x, top_y=top_y) or self.length > self.max_length
        
    def reset(self, left_x, top_y):
        self.pos = PVector(randint(left_x, width - left_x), randint(top_y, height - top_y))
        self.length = 0
        self.prev_pos = self.pos.copy()

