import gym
from gym import spaces
import numpy as np
from shapely.geometry import Polygon, Point, LinearRing
import math

#Metric 
WHEEL_SIZE = 1
RC_ROBOT_DIM_X = 0.1
RC_ROBOT_DIM_Y = 0.1

RC_RIGHT_INITIAL = 0
RC_LEFT_INITIAL = 0

START_POS_X = 0
START_POS_Y = 0

VELOCITY_INITIAL = 0

TIME_PER_ROTATION = 1.2

#in cm
WHEEL_DIAMETER = 6.85

#0-255 pwm pulses 

FRAMES_PER_SECOND = 60
#60 fps

class RCCar:
    def __init__(self, start_x, start_y):
        self.cur_x = start_x
        self.cur_y = start_y
        xs = (START_POS_X - RC_ROBOT_DIM_X/2, START_POS_X + RC_ROBOT_DIM_X/2)
        ys = (START_POS_Y - RC_ROBOT_DIM_Y/2, START_POS_Y + RC_ROBOT_DIM_Y/2)
        points = [(xs[0], ys[0]), (xs[0], ys[1]), (xs[1], ys[1]), (xs[1], ys[0])]
        self.previous_rotation = [0, 0]
        self.poly = Polygon(points)

    def dist_per_rotation():
        #Distance in cm
        return math.pi * 6.85

    def get_velocity(self, rotation_speeds):

        vl = (rotation_speeds[0] - previous_rotation[0]) * (math.pi/60.0)   
        vr = ((rotation_speeds[1] - previous_rotation[1]) * (math.pi/60.0) 
        self.previous_rotation = rotation_speeds
        vr_linear = (vr * WHEEL_DIAMETER) / 2.0
        vl_linear = (vl * WHEEL_DIAMETER) / 2.0

        v_linear = (vr_linear + vl_linear) / 2.0



        #temp filler
        return [vl, vr]

    #In seconds
    def get_time_passed():
        return frames / FRAMES_PER_SECOND
    