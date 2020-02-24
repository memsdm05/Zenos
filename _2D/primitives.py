from pyglet.gl import *
from math import *

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

    def render(self):
        glBegin(GL_LINE_LOOP)
        for x, y in self.vertices:
            glVertex2d(x, y)
        glEnd()


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
        self.list_of_points = None
        Rectangle.__init__(self, point, side, side)
        RegularPolygon.__init__(self, self.list_of_points)


class Triangle(Polygon):  # why is this a thing
    pass


class Line(_Primative):
    def __init__(self, x1, y1, x2, y2, color=WHITE):
        super(Line, self).__init__(color)
        self.pos1 = x1, y1
        self.pos2 = x2, y2
        self.dx = x2 - x1
        self.dy = y2 - y1
        self.slope = self.dy / self.dx if self.dx != 0 else 0

    def render(self):
        glBegin(GL_LINES)
        glVertex2d(*self.pos1)
        glVertex2d(*self.pos2)
        glEnd()


class Point(_Primative):
    def __init__(self, x, y, color=WHITE):
        super(Point, self).__init__(color)
        self.x = x
        self.y = y
        self.pos = x, y

    def render(self):
        glBegin(GL_POINT)
        glVertex2d(self.x, self.y)
        glEnd()



class Ellipse(_Primative):
    def __init__(self, pos, horizontal_radius, vertical_radius, color=WHITE):
        super(Ellipse, self).__init__(color)
        self.horizontal_radius = horizontal_radius
        self.vertical_radius = vertical_radius
        self.center = pos
        self.horizontal_diameter = 2 * self.horizontal_radius
        self.vertical_diameter = 2 * self.vertical_radius
        self.area = pi * horizontal_radius * vertical_radius
        self.perimeter = self._perimeter()
        self._resolution = self.perimeter // 2  # number of vertices
        self._verts = self._get_verts()

    def _get_verts(self):
        verts = []
        cx, cy = self.center
        for i in range(self._resolution):
            angle = radians(float(i) / self._resolution * 360.0)
            x = self.horizontal_radius * cos(angle) + cx
            y = self.vertical_radius * sin(angle) + cy
            verts.append((x, y))
        return verts

    def _perimeter(self):
        a, b = self.horizontal_radius, self.vertical_radius
        return pi * (3*(a+b) - sqrt((3*a+b)(a+3*b)))

    def render(self):
        glBegin(GL_LINE_LOOP)
        for x, y in self._verts:
            glVertex2d(x, y)
        glEnd()


class Circle(Ellipse):
    def __init__(self, pos, radius):
        super(Circle, self).__init__(pos, radius, radius)
        self.radius = radius
        self.diameter = radius * 2

    def _perimeter(self):
        return 2 * pi * self.radius

    def distance(self, point):
        return distance(self.center, point) - self.radius

