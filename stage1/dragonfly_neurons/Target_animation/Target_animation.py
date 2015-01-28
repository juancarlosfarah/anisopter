################################################################################
# File: Target_animation.py
# Author: Erik Grabljevec
# E-mail: erikgrabljevec5@gmail.com
# Description: Tool to animate flies.
#              Pretty hard coded. Should there be any need to change that let
#              let me know.
################################################################################

import pyglet
from random import *

ImagePath = "Images/fly2.jpg"

# Class ParallelAnimation
# =======================
# This class is extension of Class pyglet.window.Window. It animates
# N flies flying randomly. It is very hard coded.
class ParallelAnimation(pyglet.window.Window):
    def __init__(self, N):
        super(ParallelAnimation, self).__init__()
        self.y = 5
        self.N = N
        self.image = [pyglet.resource.image(ImagePath) for i in range(N)]

    def update_frames(self, dt):
        self.y += 10

    def on_draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        for i in range(self.N):
            self.image[i].blit(35+100*i, self.y, 0,
                                self.image[i].width, self.image[i].height)

# Class RandomAnimation
# =====================
# This class is extension of Class pyglet.window.Window. It animates
# N flies flying in parallel. It is very hard coded.
class RandomAnimation(pyglet.window.Window):
    def __init__(self, N):
        super(RandomAnimation, self).__init__()
        self.N = N
        self.pos = [[randint(0, self.width), randint(0, self.height)] for
                    i in range(self.N)]
        self.image = [pyglet.resource.image(ImagePath) for i in range(N)]

    def update_frames(self, dt):
        for i in range(self.N):
            dx = randint(-20, 20)
            dy = randint(-20, 20)
            self.pos[i][0] += dx
            self.pos[i][1] += dy

    def on_draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        for i in range(self.N):
            self.image[i].blit(self.pos[i][0], self.pos[i][1])

# Class FlyAnimation
# ==================
# This class contains different possible fly animation.
# Method run_random runs n flies randomly around the screen.
# Method run_parallel runs n flies in parallel through the screen.
class FlyAnimation():
    def __init__(self):
        pass

    def run_parallel(self, n):
        window = ParallelAnimation(n)
        pyglet.clock.schedule_interval(window.update_frames, 1/10.0)
        pyglet.app.run()

    def run_random(self, n):
        window = RandomAnimation(n)
        pyglet.clock.schedule_interval(window.update_frames, 1/10.0)
        pyglet.app.run()


# Test for running N random flies
# ===============================
N = 5
test = FlyAnimation()
test.run_parallel(N)