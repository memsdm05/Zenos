
class _TemplateOverlay:
    _mode = "c4B"

    def raw(self, vertices: list = [(0, 0)]):
        pass

    def lower_level(self, vertices):
        return self._mode, self.raw(vertices)

    def low_level(self, element):
        return self.lower_level(element.vertices)


class Color(_TemplateOverlay):
    previously_made = []

    def __init__(self, x: int, y: int, z: int, alpha=255, type="rgb"):
        self.opacity = alpha
        self.type = type
        self.val1 = x
        self.val2 = y
        self.val3 = z
        self.previously_made.append(self)

    def convertToRGB(color):
        if color.type == "bgr":
            color.val1, color.val2 = color.val2, color.val1

    def convertToBGR(color):
        if color.type == "rgb":
            color.val1, color.val2 = color.val2, color.val1

    def convertToHSV(color):
        pass

    def assert_RGB(self):
        if self.type != "rgb":
            self.convertToRGB()

    def raw(self, vertices: list = [(0, 0)]):
        count = len(vertices)
        self.assert_RGB()
        color_data = (self.val1, self.val2, self.val3, self.opacity) * count
        return color_data

    def mix(self, other, percentage: float = 0.5):
        my_percentage = 1 - percentage
        other.assert_RGB()
        self.assert_RGB()
        return Color(int(my_percentage*self.val1 + percentage*other.val1),
                     int(my_percentage*self.val2 + percentage*other.val2),
                     int(my_percentage*self.val3 + percentage*other.val3))


class Gradient(_TemplateOverlay):  # this is test - does not actually work
    def __init__(self, top_color: Color, bottom_color: Color, type: str = "vertical"):
        self.color1 = top_color
        self.color2 = bottom_color
        self.type = type

    def _get_index(self):
        return 0 if self.type[0] == "h" else 1 if self.type[0] == "v" else None

    def raw(self, vertices: list = [(0, 0)]):
        index = self._get_index()
        data = ()
        _max = max(vertices, key=lambda i: i[index])[index]
        _min = min(vertices, key=lambda i: i[index])[index]
        if index == 0:  # if horizontal
            _max, _min = _min, _max  # flip to make left color1
        dif = _max - _min
        for pt in vertices:
            val = pt[index]
            val -= _min
            percentage = val / dif if dif != 0 else 0.5
            color_data = self.color2.mix(self.color1, percentage).raw()
            data += color_data
        return data


class Texture(_TemplateOverlay):
    def __init__(self, image_path, coords):
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