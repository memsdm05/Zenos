from Zenos_package import *


class TestWindow(Window):  # basic 3d Tests
    c = ThreeD.Cube((2, 3, 10), 1, RED)
    origin = ThreeD.Cube((0, 0, 0), .1)

    def __init__(self):
        super(TestWindow, self).__init__()

    def periodic(self, dt):
        super(TestWindow, self).periodic(dt)
        self.c.move(pitch=10*dt, yaw=20*dt, roll=50*dt)


if __name__ == '__main__':
    x = TestWindow()
    # x.set_background(Resources.LIGHT_BLUE)
    x.lock_mouse()
    x.start()