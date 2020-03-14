from Top_Level import Window
import _2D
import Resources


class TestWindow(Window):
    c = _2D.Ellipse((500, 300), 200, 100)

    def periodic(self, dt):
        self.clear()
        self.render(self.c)

    def on_mouse_motion(self, x, y, dx, dy):
        self.c.moveTo((x, y))


if __name__ == '__main__':
    x = TestWindow()
    # x.set_background(Resources.LIGHT_BLUE)
    x.start()