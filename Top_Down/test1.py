from Top_Down import _2D, Resources
from Top_Down.Top_Level import Window

class TestWindow(Window):
    c = _2D.Square((100, 100), 10)

    def periodic(self, dt):
        self.clear()
        self.c.render_outline()

    def on_mouse_motion(self, x, y, dx, dy):
        self.c.moveTo((x, y))


if __name__ == '__main__':
    x = TestWindow()
    x.set_background(Resources.RED)
    x.start()