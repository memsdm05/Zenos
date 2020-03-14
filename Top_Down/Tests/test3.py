from Top_Down.Zenos_package import *


class TestWindow(Window):
    c = ThreeD.Cube((2, 3, 10), 1, RED)

    def __init__(self):
        super(TestWindow, self).__init__()
        self.sky = ThreeD.RectPrism((0, 0, 50), 1, 100, 70, LIGHT_BLUE)
        self.ground = ThreeD.RectPrism((0, -2, 0), 100, 1000, 1, BROWN)
        self.c.set_front_texture(PINK)

    def periodic(self, dt):
        self.clear()
        self.render(self.c, self.ground)
        # print(self.position)


if __name__ == '__main__':
    x = TestWindow()
    x.set_background(LIGHT_GREY)
    x.lock_mouse()
    x.start()
