"""
Tool to animate dragonfly targets. User only interacts with class Animation.
To create new animation create new instance of class Animation.
For any information on how to use this module refer to class Animation.
"""


from math import atan2
from math import cos 
from math import pi
from math import sin
from math import sqrt
from random import *
import os

import pyglet
from pyglet.gl import *

import cv2


class Target(object):
    """
    This class represents different targets that will move on the screen.
    """
    
    def __init__(self, type, start, end, v, size, color):
        self.type = type
        self.start = start
        self.pos = start
        self.end = end
        self.v = v
        self.size = size
        self.color = color
        
    def __eq__(self, other):
        result = True
        
        result &= self.type == other.type
        
        result &= self.start == other.start 
        result &= self.pos == other.pos
        result &= self.end == other.end
        result &= self.v == other.v
        result &= self.size == other.size
        result &= self.color == other.color

        return result

    def change_position(self, dx, dy):
        self.pos[0] += dx
        self.pos[1] += dy

    def next_position(self):
        """
        Moves Target's position according to its type.
        """
        
        if self.type == 0:
            self.change_position(0, 0)
        elif self.type == 1:
            dx = randint(-self.v, self.v)
            dy = randint(-self.v, self.v)
            self.change_position(dx, dy)
        elif self.type == 2:
            # Find direction in which we are moving.
            x_c = self.end[0] - self.start[0]
            y_c = self.end[1] - self.start[1]
            deg = atan2(y_c, x_c)
            # And move in that direction, making length of move "self.v".
            dx = self.v * cos(deg)
            dy = self.v * sin(deg)
            self.change_position(dx, dy)
            
            
class AnimationWindow(pyglet.window.Window):
    """
    This class is extension of class pyglet.window.Window. We make it over      
    pyglet.window.Window so we have easier work with some functions.
    """
    
    def __init__(self, target_list, width, height, bg_image, bg_speed):
        super(AnimationWindow, self).__init__()
        
        self.bg_image = bg_image
        if self.bg_image:
            self.bg_speed = bg_speed
            self.background = pyglet.image.load(self.bg_image).get_texture()
            
        self.target_list = target_list
        self.N = len(target_list)
        self.time = 0

    def circle(self, x, y, radius, color):
        glColor3f(color[0], color[1], color[2])
        iterations = int(2*radius*pi)+15
        s = sin(2*pi / iterations)
        c = cos(2*pi / iterations)
        dx, dy = radius, 0
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(x, y)
        for i in range(iterations):
            glVertex2f(x+dx, y+dy)
            dx, dy = (dx*c - dy*s), (dy*c + dx*s)
        glEnd()

    def update_frames(self, dt):
        for i in range(self.N):
            self.target_list[i].next_position()

    def on_draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        
        if self.bg_image:
            glColor3f(1, 1, 1)
            bg_pos = -self.time * self.bg_speed
            self.background.blit(bg_pos, bg_pos)
            
        for i in range(self.N):
            x = self.target_list[i].pos[0]
            y = self.target_list[i].pos[1]
            size = self.target_list[i].size
            color = self.target_list[i].color
            self.circle(x, y, size, color)
            
        image_name = "temp/scr" + str(self.time) + ".png"
        pyglet.image.get_buffer_manager().get_color_buffer().save(image_name)
        self.time += 1

    def stop(self, dt):
        pyglet.app.exit()


class Animation(object):
    """ 
    This class handles different possible target animations.
    
    Interact with this class with next methods:
    - add_target
    - add_background
    - run
    For more information on these methods refer to their doc.
    """
    
    def __init__(self, width=640, height=480):
        self.target_list = []
        self.width = width
        self.height = height
        self.bg_image = False
        self.bg_speed = 0
        
    def make_directory(self, directory):
        self.directory = directory
        if not os.path.exists(directory):
            os.makedirs(directory)

    def create_movie(self, out_directory, total_frames):
        img1 = cv2.imread("temp/scr0.png")
        height, width, layers =  img1.shape
        codec = cv2.cv.CV_FOURCC('M','J','P','G')
        video = cv2.VideoWriter(out_directory, codec, 20.0, (width,height))

        for i in range(total_frames):
            img_name = "temp/scr" + str(i) + ".png"
            img = cv2.imread(img_name)
            video.write(img)

        video.release()
        cv2.destroyAllWindows()

    def add_target(self, type, start=[0, 0], end=[100, 100], 
                   v=5, size=10, color=[0, 0, 0]):
        """
        Adds target in animation with several different options.
        
        Args:
            type: It is either 0 for stationary target,
                1 for randomly moving target or 2 for target
                moving from start to end position in straight line.
            start: Starting position.
            end: Ending position, only relavant for type 2.
            v: Sets velocity of target.
            size: Sets size of target.
            color: Sets color of target.
        """      
        
        new_target = Target(type, start, end, v, size, color)
        self.target_list.append(new_target)
        
    def add_background(self, img_dir=False, speed=0):
        """
        Adds background to animation. It can be either stationary or moving.
        
        Args:
            img_dir: Sets directory of background image.
                If it stays False background is white.
            speed: Sets how fast the background is moving.
        """
        
        self.bg_image = img_dir
        self.bg_speed = speed

    def run(self, out_directory, fps=10, total_frames=50):
        """
        Run animation and save it in out_directory.
        
        Args:
            out_directory: Sets directory of output movie.
            fps: Sets fps used to make animation. It must be larger than 0.
            total_frames: Total frames that movie will contain.
        """
        
        self.make_directory("temp")
        window = AnimationWindow(self.target_list, self.width, self.height, 
                                 self.bg_image, self.bg_speed)
        # Next line makes window update every 1.0/fps seconds after
        # running method update_frames on window.
        pyglet.clock.schedule_interval(window.update_frames, 1.0/fps)
        pyglet.clock.schedule_once(window.stop, total_frames/fps)
        pyglet.app.run()
        window.close()
        self.create_movie(out_directory, total_frames)
