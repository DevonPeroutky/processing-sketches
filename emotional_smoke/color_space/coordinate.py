class Coordinate(object):

    def __init__(self, x, y, coor_color = None):
        print("CREATING A COORDINATE")
        self.X = x
        self.Y = y
        self.COLOR = coor_color
        if (coor_color):
            self.RED_VALUE = coor_color >> 16 & 0xFF
            self.BLUE_VALUE = coor_color & 0xFF
            self.GREEN_VALUE = coor_color >> 8 & 0xFF

    def set_color(self, color):
        self.COLOR = color
        if (color):
            self.RED_VALUE = color >> 16 & 0xFF
            self.BLUE_VALUE = color & 0xFF
            self.GREEN_VALUE = color >> 8 & 0xFF

    def __key(self):
        return (self.X, self.Y)

    def __eq__(self, other):
        if isinstance(other, Coordinate):
            return self.__key() == other.__key()
        return NotImplemented

    def __str__(self):
        print("PRINTING A COORDINATE")
        if self.COLOR:
            return "({}, {}) --> ({}, {}, {})".format(self.X, self.Y, self.RED_VALUE, self.BLUE_VALUE, self.BLUE_VALUE)
        else:
            print("NO COLOR")
            return "({}, {})".format(self.X, self.Y)

    def __hash__(self):
        return hash(self.__key())

