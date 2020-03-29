from Zenos_package import *


class TestWindow(Window):
    c = TwoD.Square((500, 300), 300, RED)
    in_3 = False

    def start(self):
        super(TestWindow, self).start()
        self.position = 0, 0, -20

    def on_mouse_motion(self, x, y, dx, dy):
        if self.in_3:
            super(TestWindow, self).on_mouse_motion(x, y, dx, dy)
        else:
            self.c.moveTo((x, y))

    def on_key_press(self, symbol, modifiers):
        if symbol == self.keys.SPACE:
            self.in_3 = True
            self.c = self.c.get_3D_version((0, 0, 0))
            self.lock_mouse()


if __name__ == '__main__':
    x = TestWindow()
    x.set_background(LIGHT_BLUE)
    x.start()