from Zenos_package import *


class TestWindow(Window):
    c = TwoD.Rectangle((500, 300), 200, 100, Gradient(WHITE, BLACK, "horizontal"))

    def periodic(self, dt):
        self.clear()
        self.render(self.c)

    def on_mouse_motion(self, x, y, dx, dy):
        self.c.moveTo((x, y))


if __name__ == '__main__':
    x = TestWindow()
    # x.set_background(Resources.LIGHT_BLUE)
    x.start()