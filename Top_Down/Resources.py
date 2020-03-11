import pyglet

# useful functions
def create_vertex_list(points, indexed=False):  # todo allow color to be added
    dimensions = len(points[0])
    data_type = 'i' if type(points[0][0]) == int else 'f'  # specify integer or float
    mode = "v" + str(dimensions) + data_type
    length = len(points)
    position_data = []
    for point in points:
        position_data.extend(point)
    position_data = tuple(position_data)
    if indexed:
        verticies = pyglet.graphics.vertex_list_indexed(length, [i for i in range(length)], (mode, position_data))
    else:
        verticies = pyglet.graphics.vertex_list(length, (mode, position_data))
    return verticies


# useful classes
#-------------------------------#

# draw group
class Group:
    def __init__(self):
        self.type = None
        self.items2d = []
        self.items3d = []

    def add(self, other):
        pass

    def remove(self, other):
        pass

    def __add__(self, other):
        self.add(other)

    def __sub__(self, other):
        self.remove(other)


class Color:
    def __init__(self, x, y, z, alpha=255, type="rgb"):
        self.opacity = alpha
        self.type = type
        self.val1 = x
        self.val2 = y
        self.val3 = z

    def convertToRGB(color):
        pass

    def convertToBGR(color):
        pass

    def convertToHSV(color):
        pass

    def _assert_RGB(self):
        if self.type != "rgb":
            self.convertToRGB()

    def raw(self):
        self._assert_RGB()
        return self.val1, self.val2, self.val3, self.opacity

    def low_level(self, shape):
        length = len(shape.vertices)
        raw = self.raw()
        proccesed = []
        for i in range(length):
            proccesed.extend(raw)
        proccesed = tuple(proccesed)
        thing = self._get_type(), proccesed
        return thing

    def _get_type(self):
        return 'c4B'


class Gradient:
    pass


class Texture:
    pass

# constants
RED = Color(255, 0, 0)
LIGHT_RED = Color(255, 50, 50)
YELLOW = Color(255, 255, 0)
BLACK = Color(0, 0, 0)
BLUE = Color(0, 0, 255)
LIGHT_BROWN = Color(165, 42, 42)
WHITE = Color(255, 255, 255)
GREY = Color(100, 100, 100)
LIGHT_GREY = Color(150, 150, 150)
OCEAN_BLUE = Color(0, 0, 155)
LIME_GREEN = Color(127, 255, 0)
GREEN = Color(0, 255, 0)
DARK_GREEN = Color(0, 100, 0)
PINK = Color(255, 192, 203)
ORANGE = Color(255, 69, 0)
BROWN = Color(165, 42, 42)
LIGHT_BLUE = Color(173, 216, 230)