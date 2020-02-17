from Primatives import Point

class Vector2:
    def __init__(self, p1, p2=None):
        if p2 is None:
            p2 = p1
            p1 = Point(0, 0)
        self.start = p1
        self.end = p2
        self.magnitude = self._magnitude()

    def _magnitude(self):
        x1, y1 = self.start.pos
        x2, y2 = self.end.pos

    def __add__(self, other):
        pass

    def __sub__(self, other):
        return -(self + other)

    def __mul__(self, other):
        pass

    def __pow__(self, power, modulo=None):
        pass