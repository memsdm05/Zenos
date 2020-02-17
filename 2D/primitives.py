import pyglet
from math import pi, sqrt

WHITE = (255, 255, 255)


def distance(p1, p2):
    x1, y1 = p1.pos
    x2, y2 = p2.pos
    dx, dy = x2 - x1, y2 - y1
    return sqrt(dx**2 + dy**2)


class _Primative():
    def __init__(self, color):
        self.color = color

    def render(self):
        pass


class Polygon(_Primative):
    def __init__(self, list_of_points, color=WHITE, fill=False):
        super(Polygon, self).__init__(color)
        self.vertices = list_of_points
        self.length = len(list_of_points)
        self.lines = []
        for i in range(self.length):
            p1 = list_of_points[i]
            p2 = list_of_points[0] if i == self.length - 1 else list_of_points[i+1]
            self.lines.append(Line(p1, p2))


class RegularPolygon(Polygon):
    pass


class Quad(Polygon):  # why is quad a thing
    pass
        

class Rectangle(Quad):
    def __init__(self, point, w, h, color=WHITE, fill=False):
        x, y = point.pos
        vertices = ((x, y), (x + w, y), (x + w, y + h), (x, y + h))
        super(Rectangle, self).__init__(vertices, color, fill)


class Square(Rectangle, RegularPolygon):
    def __init__(self, point, side):
        Rectangle.__init__(self, point, side, side)
        RegularPolygon.__init__(self, self.list_of_points)


class Triangle(Polygon):  # why is this a thing
    pass


class Line(_Primative):
    def __init__(self, point1, point2, color=WHITE):
        super(Line, self).__init__(color)
        x1, y1 = point1.pos
        x2, y2 = point1.pos
        self.dx = x2 - x1
        self.dy = y2 - y1
        self.p1 = point1
        self.p2 = point2
        self.slope = self.dy / self.dx if self.dx != 0 else 0

    def render(self):
        pyglet.graphics.draw()


class Point(_Primative):
    def __init__(self, x, y, color=WHITE):
        super(Point, self).__init__(color)
        self.x = x
        self.y = y
        self.pos = x, y


class Ellipse(_Primative):
    def __init__(self, pos, horizontal_radius, vertical_radius):
        super(Ellipse, self).__init__()
        self.horizontal_radius = horizontal_radius
        self.vertical_radius = vertical_radius
        self.center = pos
        self.horizontal_diameter = 2 * self.horizontal_radius
        self.vertical_diameter = 2 * self.vertical_radius
        self.area = pi * horizontal_radius * vertical_radius


class Circle(Ellipse):
    def __init__(self, pos, radius):
        super(Circle, self).__init__(pos, radius, radius)
        self.radius = radius
        self.diameter = radius * 2

    def distance(self, point):
        pass

