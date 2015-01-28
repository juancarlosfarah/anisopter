################################################################################
# File: Target_animation.py
# Author: Erik Grabljevec
# E-mail: erikgrabljevec5@gmail.com
# Description: Tool to animate flies.
#              ...
################################################################################

import pyglet

# Class FlyAnimation
# ==================
# This class contains different possible fly animation.
# ...
class ParallelAnimation(pyglet.window.Window):
    def __init__(self, N):
        super(ParallelAnimation, self).__init__()
        self.x = 35
        self.y = 5
        self.N = N
        self.image = [pyglet.resource.image("Images/fly2.jpg") for i in range(N)]

    def update_frames(self, dt):
        self.y += 10

    def on_draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        for i in range(self.N):
            self.image[i].blit(self.x+100*i, self.y, 0,
                                self.image[i].width, self.image[i].height)

class FlyAnimation():

    def __init__(self):
        pass

    def run_parallel(self, n):
        window = ParallelAnimation(n)
        pyglet.clock.schedule_interval(window.update_frames, 1/10.0)
        pyglet.app.run()

test = FlyAnimation()
test.run_parallel(2)