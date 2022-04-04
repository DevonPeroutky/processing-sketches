class Coordinate(object):

    def __init__(self, x, y, coor_color = None):
        self.X = x
        self.Y = y
        self.COLOR = coor_color
        self.RED_VALUE = coor_color >> 16 & 0xFF if coor_color else None
        self.BLUE_VALUE = coor_color & 0xFF if coor_color else None
        self.GREEN_VALUE = coor_color >> 8 & 0xFF if coor_color else None

    def set_color(self, color):
        self.COLOR = color
        self.RED_VALUE = color >> 16 & 0xFF if color else None
        self.BLUE_VALUE = color & 0xFF if color else None
        self.GREEN_VALUE = color >> 8 & 0xFF if color else None

    def __key(self):
        return (self.X, self.Y)

    def __eq__(self, other):
        if isinstance(other, Coordinate):
            return self.__key() == other.__key()
        return NotImplemented

    def __str__(self):
        if self.COLOR:
            return "({}, {}) --> ({}, {}, {})".format(self.X, self.Y, self.RED_VALUE, self.GREEN_VALUE, self.BLUE_VALUE)
        else:
            return "({}, {})".format(self.X, self.Y)

    def __hash__(self):
        return hash(self.__key())

