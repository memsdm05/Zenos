from math import sqrt, atan, pi


def distance(x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    return sqrt(dx**2 + dy**2)


def towards(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    angle = atan(dy / dx) if dx != 0 else pi/2 if dy > 0 else 3*pi/2
    angle += pi if dx < 0 else 0
    return angle


class Vector2:
    def __init__(self, x, y):
        self.pos = x, y
        self.x = x
        self.y = y
        self.magnitude = self._magnitude()
        self.x_hat, self.y_hat = self._unit_vectors()

    def _magnitude(self):
        return distance(0, 0, *self.pos)

    def _angle(self):
        return towards(0, 0, self.x, self.y)

    def _unit_vectors(self):
        proportion = 1/self.magnitude
        return self.x * proportion, self.y * proportion

    def resize(self, length):
        proportion = length/self.magnitude
        self.x = self.x * proportion
        self.y = self.y * proportion
        self.pos = self.x, self.y

    def __add__(self, other):
        x1, y1 = self.pos
        x2, y2 = other.endpoint.pos
        return Vector2(x1+x2, y1+y2)

    def __sub__(self, other):
        return -(self + other)

    def __mul__(self, other):  # cross-mult
        x1, y1 = self.pos
        if type(other) == Vector2:
            x2, y2 = other.endpoint.pos
        else:
            x2 = y2 = other
        return Vector2(x1 * x2, y1 * y2)

    def __pow__(self, power, modulo=None):  # dot product
        pass