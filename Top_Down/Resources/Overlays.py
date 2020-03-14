import pyglet


class TemplateOverlay:
    _mode = "c4B"
    def raw(self):
        pass

    def low_level(self, vertex_count):
        return self._mode, self.raw() * vertex_count


class Color(TemplateOverlay):
    def __init__(self, x, y, z, alpha=255, type="rgb"):
        self.opacity = alpha
        self.type = type
        self.val1 = x
        self.val2 = y
        self.val3 = z

    def convertToRGB(color):
        if color.type == "bgr":
            color.val1, color.val2 = color.val2, color.val1

    def convertToBGR(color):
        if color.type == "rgb":
            color.val1, color.val2 = color.val2, color.val1

    def convertToHSV(color):
        pass

    def _assert_RGB(self):
        if self.type != "rgb":
            self.convertToRGB()

    def raw(self):
        self._assert_RGB()
        return self.val1, self.val2, self.val3, self.opacity


class Gradient(TemplateOverlay):
    pass


class Texture(TemplateOverlay):
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