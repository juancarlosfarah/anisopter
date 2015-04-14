from visual import *
import math
import random

# Set up the space
wallR = box(pos=(6,0,0), size=(0.2,12,12), color=color.green)
wallL = box(pos=(-6,0,0), size=(0.2,12,12), color=color.green)
wallU = box(pos=(0,6,0), size=(12,0.2,12), color=color.blue)
WallD = box(pos=(0,-6,0), size=(12,0.2,12), color=color.blue)
# Create the dragonfly
#dfly = sphere(pos=(5,-2,0), radius=0.3, color=color.yellow)
#dfly.velocity = vector(0,0,0)

ball = sphere(pos=(-5,0,0), radius=0.2, color=color.cyan)
ball.velocity = vector(25,0,0)

# Lights to indicate the direction
lightL = sphere(pos=(-7,0,12), radius=1, color=color.yellow)
lightL.visible = False

lightR = sphere(pos=(7,0,12), radius=1, color=color.yellow)
lightR.visible = False

lightU = sphere(pos=(0,7,12), radius=1, color=color.yellow)
lightU.visible = False

lightD = sphere(pos=(0,-7,12), radius=1, color=color.yellow)
lightD.visible = False

deltat = 0.001
t = 0
ball.pos = ball.pos + ball.velocity*deltat

#scene.autoscale = False
while true:
    time_update=t
    xvel=random.randint(-10,10)
    yvel=random.randint(-10,10)
    ball.velocity = vector(xvel,yvel,0)
    
    
    
    while t<time_update+1:
        if ball.pos[0]>5 or ball.pos[0]<-5:
            ball.velocity[0] *= -1
        if ball.pos[1]>5 or ball.pos[1]<-5:
            ball.velocity[1] *= -1
    
        # If the target is moving to the right make the right light flash
        if ball.velocity[0] > 0:
            lightL.visible=False
            lightR.visible=True
        # Else make the left light flash
        elif ball.velocity[0] < 0:
            lightL.visible= True
            lightR.visible= False
        # Else if the target is not moving in the x coordinate
        elif ball.velocity[0] == 0:
            lightL.visible= False
            lightR.visible= False
            
        # If the target is moving up
        if ball.velocity[1] > 0:
            lightU.visible=True
            lightD.visible=False
        # Else make the down light flash
        elif ball.velocity[1] < 0:
            lightD.visible= True
            lightU.visible= False
        # Else if the target is not moving in the y coordinate
        elif ball.velocity[1] == 0:
            lightD.visible= False
            lightU.visible= False        
           
        """    
        if ball.velocity[0] < 0 and dfly.pos[0]>-6:
            xvel = math.fabs(dfly.pos[0]-ball.pos[0])
            dfly.velocity = vector(-xvel,0,0)
            
        elif ball.velocity[0] > 0 and dfly.pos[0]<6:
            xvel = math.fabs(dfly.pos[0]-ball.pos[0])
            dfly.velocity = vector(xvel,0,0)
           
        else:
            dfly.velocity = vector(0,0,0)
        """ 
             
        ball.pos = ball.pos + ball.velocity*deltat
        #dfly.pos = dfly.pos + dfly.velocity*deltat
        t = t+deltat
 
        #set the rate of computation
        rate(1000) #1000 loops/sec (since deltat=0.001 => 1 sec of animation = 1sec)
    
