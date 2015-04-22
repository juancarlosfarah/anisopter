"""
Tool to animate dragonfly targets. User only interacts with class Animation.
To create new animation create new instance of class Animation.
For any information on how to use this module refer to class Animation.
"""


import Image
from math import atan2
from math import cos 
from math import pi
from math import sin
from math import sqrt
from random import *
import os
from subprocess import call

import gizeh
import numpy
import cv2


class Dragonfly(object):
    '''
    This class follows Targets and stuff.
    '''
    def __init__(self, path):
        self.pos = path[0][0:2]
        self.path = path

    def get_position(self, time):
        index = 0
        while (index < len(self.path)) and (self.path[index][2] < time):
            index += 1
        return self.path[index][0:2]

    def update(self, time):
        self.pos = self.get_position(time)


class Background(object):
    '''
    This class store background used in animation.
    '''
    def __init__(self, directory, speed=0):
        self.directory = directory

        self.img = Image.open(directory)
        self.img.load()
        self.data = numpy.asarray(self.img, dtype="int32")

        self.pos = [0,0]
        self.speed = speed

    def update(self):
        self.pos[0] += self.speed
        self.pos[1] += self.speed


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

    def get_pos(self, frame):
        '''
        Returns position of target at frame "frame". It returns starting
        position for randomly moving and stationary targets.
        '''

        if self.type != 2:
            return self.start
        else:
            x_c = self.end[0] - self.start[0]
            y_c = self.end[1] - self.start[1]
            deg = atan2(y_c, x_c)
            dx = frame * self.v * cos(deg)
            dy = frame * self.v * sin(deg)
            result = [self.start[0]+dx, self.start[1]+dy]
            return result


class AnimationWindow(object):
    """
    This class keeps track of current animation frame.
    """
    
    def __init__(self, target_list, width, height, bg=False, dragonfly=False):
        self.bg = bg
        self.dragon = dragonfly
        self.target_list = target_list
        self.N = len(target_list)
        self.time = 0
        self.width = width
        self.height = height

    def update_frame(self, time):
        if self.bg:
            self.bg.update()

        if self.dragon:
            self.dragon.update(time)

        for i in range(self.N):
            self.target_list[i].next_position()

    def draw(self):
        surface = gizeh.Surface(width=self.width, height=self.height,
                                bg_color=(1,1,1))

        if self.bg:
            fill = gizeh.ImagePattern(self.bg.data, self.bg.pos, filter='best')
            bg_circle = gizeh.circle(r=self.width*5, fill=fill)
            bg_circle.draw(surface)

        if self.dragon:
            xy_pos = self.dragon.pos
            dragon_circle = gizeh.circle(r=10, xy=xy_pos, fill = (1,0,0))
            dragon_circle.draw(surface)

        for target in self.target_list:
            circle = gizeh.circle(r=target.size, xy=target.pos, fill= (0,0,0))
            circle.draw(surface)

        surface.get_npimage()

        img_name = "temp/scr" + str(self.time) + ".png"
        surface.write_to_png(img_name)

        self.time += 1


# TO-DO: setters and getters for dragonfly position.
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
        self.dragonfly = False
        self.width = width
        self.height = height
        self.bg = False
        self.total_frames = 50
        self.fps = 20
        
    def make_directory(self, directory):
        self.directory = directory
        if not os.path.exists(directory):
            os.makedirs(directory)

    def create_movie(self, out_directory, fps, total_frames):
        img1 = cv2.imread("temp/scr0.png")
        height, width, layers =  img1.shape
        codec = cv2.cv.CV_FOURCC('M','J','P','G')
        video = cv2.VideoWriter(out_directory, codec, fps, (width, height))

        for i in range(total_frames):
            img_name = "temp/scr" + str(i) + ".png"
            img = cv2.imread(img_name)
            video.write(img)

        # TO-DO: change this not to be hard coded.
        dir = out_directory.strip(".avi")

        command = "avconv -i %s.avi -c:v libx264 -c:a copy %s.mp4" % (dir, dir)
        call(command.split())

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

    def add_dragonfly(self, path):
        """
        Adds background to animation. It can be either stationary or moving.

        Args:
            path: sets path that dragonfly will follow
        """
        self.dragonfly = Dragonfly(path)
        
    def add_background(self, img_dir=False, speed=0):
        """
        Adds background to animation. It can be either stationary or moving.
        
        Args:
            img_dir: Sets directory of background image.
                If it stays False background is white.
            speed: Sets how fast the background is moving.
        """
        
        self.bg = Background(img_dir, speed)

    def run(self, out_directory, fps=20, total_frames=50):
        """
        Run animation and save it in out_directory.
        
        Args:
            out_directory: Sets directory of output movie. It must end in .avi!
            fps: Sets fps used to make animation. It must be larger than 0.
            total_frames: Total frames that movie will contain.
        """

        self.fps = fps
        self.total_frames = total_frames
        self.make_directory("temp")
        history = [self.target_list, self.bg, self.dragonfly] # Save to reset.
        window = AnimationWindow(self.target_list, self.width, self.height, 
                                 self.bg, self.dragonfly)
        # Next line makes window update every 1.0/fps seconds after
        # running method update_frames on window.
        for i in range(total_frames):
            time = 1.0 * i / total_frames
            window.update_frame(time)
            window.draw()

        self.create_movie(out_directory, fps, total_frames)
        [self.target_list, self.bg, self.dragonfly] = history

    def get_targets_positions(self, time):
        """
        Get list of positions of target at time "time".
        The return format is [[x1, y1], [x2, y2], ... [xn, yn]]

        Args:
            frame: at which frame you want positions of targets.
        """
        result = []
        for target in self.target_list:
            frame = int(time * self.total_frames)
            pos = target.get_pos(frame)
            result.append(pos)
        return result

    def get_dragonfly_position(self, time):
        """
        Get position of dragonfly at time "time".

        Args:
            time: at which time in interval [0, 1] do you want to know
                  the distance.
        """
        return self.dragonfly.get_position(time)

    def get_distance_dragonfly_to_closest_target(self, time):
        """
        Get distance of dragonfly to closest target.

        Args:
            time: at which time in interval [0, 1] do you want to know
                  the distance.
        """
        dragon = self.get_dragonfly_position(time)
        targets = self.get_targets_positions(time)
        print dragon
        print targets
        best_result = 1001001001
        for target in targets:
            dx = dragon[0] - target[0]
            dy = dragon[1] - target[1]
            d = sqrt(dx * dx + dy * dy)
            best_result = min(best_result, d)
        return best_result