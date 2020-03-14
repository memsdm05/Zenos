import pyglet
from math import *
from Top_Down.Resources.Overlays import WHITE, Texture, Color, Gradient
from Top_Down.Resources.Rendering import *
from Top_Down.Low_Level import LowLevel

# utility functions
convert_pos = LowLevel.convert_pos


def distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    dx = x2 - x1
    dy = y2 - y1
    return sqrt(dx*dx + dy*dy)


def towards(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    dx = x2 - x1
    dy = y2 - y1
    angle = atan(dy / dx) if dx != 0 else pi / 2 if dy > 0 else 3 * pi / 2
    angle += pi if dx < 0 else 0
    return angle


def rotate(list_of_points, amount, center=None):
    pass


def reflect():
    pass


# layout for what everything should have
class Template_2d(ElementTemplate):
    dimension = 2
    _indexed = False
    mode = pyglet.graphics.GL_LINES
    _vertex_type = "v2f"

    def moveTo(self, pos):
        pos = convert_pos(pos)
        x1, y1 = pos
        x2, y2 = self.location
        dx = x1 - x2
        dy = y1 - y2
        self.move(dx, dy)

    def rotate(self, amount):
        self.vertices = rotate(self.vertices, amount, self._find_center())
        self.update()

    def move(self, dx, dy):
        self.vertices = [(x+dx, y+dy) for x, y in self.vertices]
        x, y = self.location
        self.location = x + dx, y + dy
        self.update()

    def _find_center(self):
        all_x = [x for x, y in self.vertices]
        all_y = [y for x, y in self.vertices]
        return sum(all_x) // len(all_x), sum(all_y) // len(all_y)


class Text:
    def __init__(self, pos, str, font_size, font_color=WHITE):
        pass


class Shape(Template_2d):
    mode = pyglet.graphics.GL_POLYGON
    _outline = pyglet.graphics.GL_LINE_LOOP

    def __init__(self, overlay):
        super(Shape, self).__init__(overlay)
        self.texture = overlay
        # self.outline_color = None
        # self.fill_color = None

    def render_outline(self):
        self.vertex_list.draw(self._outline)


class Polygon(Shape):
    def __init__(self, list_of_points, color=WHITE):
        super(Polygon, self).__init__(color)
        self.vertices = [convert_pos(pos) for pos in list_of_points]
        self.length = len(list_of_points)
        self.lines = []
        for i in range(self.length):
            p1 = list_of_points[i]
            p2 = list_of_points[0] if i == self.length - 1 else list_of_points[i + 1]
            self.lines.append(Line(p1, p2))
        self._initialize()


class RegularPolygon(Polygon):
    def __init__(self, center, radius):
        super(RegularPolygon, self).__init__()


class Rectangle(Polygon):
    _mode = pyglet.graphics.GL_QUADS

    def __init__(self, pos, w, h, texture=WHITE):
        x, y = pos
        self.center = convert_pos(pos)
        vertices = ((x, y), (x + w, y), (x + w, y - h), (x, y - h))
        self.vertices = vertices
        super(Rectangle, self).__init__(vertices, texture)


class Square(Rectangle):
    def __init__(self, point, side, texture=WHITE):
        Rectangle.__init__(self, point, side, side, texture)


class Line(Template_2d):
    _mode = pyglet.graphics.GL_LINE

    def __init__(self, pos1, pos2, overlay=WHITE):
        super(Line, self).__init__(overlay)
        self.texture = overlay
        pos1 = convert_pos(pos1)
        pos2 = convert_pos(pos2)
        self.vertices = [pos1, pos2]
        x1, y1 = pos1
        x2, y2 = pos2
        self.pos1 = pos1
        self.pos2 = pos2
        self.dx = x2 - x1
        self.dy = y2 - y1
        self.slope = self.dy / self.dx if self.dx != 0 else 0
        self._initialize()


class Point(Template_2d):
    _mode = pyglet.graphics.GL_POINT

    def __init__(self, x, y, color=WHITE):
        super(Point, self).__init__()
        x, y = convert_pos((x, y))
        self.texture = color
        self.vertices = [(x, y)]
        self.x = x
        self.y = y
        self.pos = x, y
        self._initialize()


class Ellipse(Shape):
    def __init__(self, pos, horizontal_radius, vertical_radius, overlay=WHITE):
        super(Ellipse, self).__init__(overlay)
        pos = convert_pos(pos)
        self.horizontal_radius = horizontal_radius
        self.vertical_radius = vertical_radius
        self.location = pos
        self.horizontal_diameter = 2 * self.horizontal_radius
        self.vertical_diameter = 2 * self.vertical_radius
        self.area = pi * horizontal_radius * vertical_radius
        self.perimeter = self._perimeter()
        self._resolution = self.perimeter // 2  # number of vertices
        self.vertices = self._get_verts()
        self._initialize()

    def _get_verts(self):
        verts = []
        cx, cy = self.location
        for i in range(int(self._resolution)):
            angle = radians(float(i) / self._resolution * 360.0)
            x = self.horizontal_radius * cos(angle) + cx
            y = self.vertical_radius * sin(angle) + cy
            verts.append((x, y))
        return verts

    def _perimeter(self):
        a, b = self.horizontal_radius, self.vertical_radius
        return pi * (3 * (a + b) - sqrt((3 * a + b)*(a + 3 * b)))


class Circle(Ellipse):  # could change to regular polygon
    def __init__(self, pos, radius, texture=WHITE):
        self.radius = radius
        self.diameter = radius * 2
        super(Circle, self).__init__(pos, radius, radius)
        self.texture = texture

    def _perimeter(self):
        return 2 * pi * self.radius

    def distance(self, point):
        return distance(self.center, point) - self.radius
