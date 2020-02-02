import gym
from gym import spaces
import numpy as np
from shapely.geometry import Polygon, Point, LinearRing
import shapely.affinity as affinity
import math

from .config import ROOM_DIM_X, ROOM_DIM_Y, MAX_SENSOR_DETECT, WHEEL_DIAMETER, RC_ROBOT_DIAMETER, MIN_TIME_PER_ROTATION, MAX_ANGULAR_VELOCITY, WHEEL_DISTANCE, FRAMES_PER_SECOND


def create_hexagon(center_x, center_y, radius):
    side30 = radius / 2
    side60 = math.sqrt(3) * side30
    point1 = (center_x  + radius, center_y)
    point2 = (center_x  + side30, center_y + side60)
    point3 = (center_x  - side30, center_y + side60)
    point4 = (center_x - radius, center_y)
    point5 = (center_x - side30, center_y - side60)
    point6 = (center_x + side30, center_y - side60)
    
    return [point1, point2, point3, point4, point5, point6]

class RCCar:
    def __init__(self, start_x, start_y):
        self.cur_x = start_x
        self.cur_y = start_y

        self.next_x = self.cur_x
        self.next_y = self.cur_y

        self.prev_x = self.cur_x
        self.prev_y = self.cur_y

        self.cur_theta = math.pi / 2
        self.next_theta = self.cur_theta

        robot_hex = create_hexagon(self.cur_x, self.cur_y, RC_ROBOT_DIAMETER / 2)
        robot_shell = create_hexagon(self.cur_x, self.cur_y, RC_ROBOT_DIAMETER / 2 + MAX_SENSOR_DETECT)

        self.poly = Polygon(robot_hex)

        self.sensor_fields = []
        # make 5 of the sensor fields
        for i in range(5):
            trap = Polygon([robot_shell[i], robot_hex[i], robot_hex[i + 1], robot_shell[i + 1]])
            self.sensor_fields.append(trap)
        # last 6
        trap = Polygon([robot_shell[5], robot_hex[5], robot_hex[0], robot_shell[0]])
        self.sensor_fields.append(trap)

        self.penalties = 0

    def find_next_frame_data(self, action):
        wheel_angular_velocities = self.action_to_rotational_velocity(action)
        wheel_linear_velocities = wheel_angular_velocities * WHEEL_DIAMETER / 2

        w = (wheel_linear_velocities[1] - wheel_linear_velocities[0]) / WHEEL_DISTANCE
        if (wheel_linear_velocities[1] - wheel_linear_velocities[0]) < 0.01:
            self.next_x = self.cur_x + wheel_linear_velocities[0] * 1/FRAMES_PER_SECOND * math.cos(self.cur_theta)
            self.next_y = self.cur_y + wheel_linear_velocities[0] * 1/FRAMES_PER_SECOND * math.sin(self.cur_theta)
            self.next_theta = self.cur_theta
            return
        # turning in place, use one motor
        elif (wheel_linear_velocities[1] + wheel_linear_velocities[0]) < 0.01:
            wheel_linear_velocities[1] = 0

        r = WHEEL_DISTANCE / 2 * ((wheel_linear_velocities[1] + wheel_linear_velocities[0]) / (wheel_linear_velocities[1] - wheel_linear_velocities[0]))
        icc = [self.cur_x - r * math.sin(self.cur_theta), self.cur_y + r * math.cos(self.cur_theta)]

        w_t = w * 1/FRAMES_PER_SECOND
        mod_x, mod_y = self.cur_x - icc[0], self.cur_y - icc[1]
        self.next_x = math.cos(w_t) * mod_x  - math.sin(w_t) * mod_y
        self.next_y = math.sin(w_t) * mod_x + math.cos(w_t) * mod_y
        self.next_x += icc[0]
        self.next_y += icc[1]
        self.next_theta = w_t + self.cur_theta

    def apply_transform(self, dx, dy):
        for i in range(len(self.sensor_fields)):
            trap = self.sensor_fields[i]
            # apply dx, dy
            trap = affinity.translate(trap, dx, dy)
            self.sensor_fields[i] = trap
        # update robot polygon
        self.poly = affinity.translate(self.poly, dx, dy)

        self.cur_x += dx
        self.cur_y += dy
    
    def apply_rotation(self, dtheta):
        for i in range(len(self.sensor_fields)):
            trap = self.sensor_fields[i]
            # apply dtheta
            trap = affinity.rotate(trap, dtheta * 180/(math.pi), 'center')
            self.sensor_fields[i] = trap
        self.poly = affinity.rotate(self.poly, dtheta * 180/(math.pi), 'center')

    def update_robot_bounds(self, objects):
        self.prev_x = self.cur_x
        self.prev_y = self.cur_y

        # update sensor fields
        dx = self.next_x - self.cur_x
        dy = self.next_y - self.cur_y
        dtheta = self.next_theta - self.cur_theta
        self.apply_transform(dx, dy)
        self.apply_rotation(dtheta)

        # absolutes
        self.cur_x = self.next_x
        self.cur_y = self.next_y
        self.cur_theta = self.next_theta

        for obj in objects[1:]: # ignore car at index 0
            if self.poly.contains(obj.poly) or self.poly.intersects(obj.poly):
                self.penalties += 1
        
        # keep robot in bounds
        if self.cur_x > ROOM_DIM_X - RC_ROBOT_DIAMETER / 2:
            dx = ROOM_DIM_X - RC_ROBOT_DIAMETER / 2 - self.cur_x
            self.apply_transform(dx, 0)
            self.next_x = self.cur_x
            
        elif self.cur_x < 0 + RC_ROBOT_DIAMETER / 2:
            dx = (0 + RC_ROBOT_DIAMETER / 2) - self.cur_x
            self.apply_transform(dx, 0)
            self.next_x = self.cur_x
       
        if self.cur_y > ROOM_DIM_Y - RC_ROBOT_DIAMETER / 2:
            dy = (ROOM_DIM_Y - RC_ROBOT_DIAMETER / 2) - self.cur_y
            self.apply_transform(0, dy)
            self.next_y = self.cur_y

        elif self.cur_y < 0 + RC_ROBOT_DIAMETER / 2:
            dy = (0 + RC_ROBOT_DIAMETER / 2) - self.cur_y
            self.apply_transform(0, dy)
            self.next_y = self.cur_y
        
    def get_penalties(self):
        penalties = self.penalties
        self.penalties = 0
        return penalties

    def action_to_rotational_velocity(self, action):
        return MAX_ANGULAR_VELOCITY * (action / 1.0)

    def update(self, action, objects):   
        print(action)     
        self.update_robot_bounds(objects)
        self.find_next_frame_data(action)

    def get_sensor_data(self, objects):
        """ Scans environment and determines if objects are in radar and if so to which sensor and the distance """
        to_ret = [MAX_SENSOR_DETECT for _ in range(6)]
        for i, trap in enumerate(self.sensor_fields):
            for obj in objects[1:]: # ignore car at index 0
                if trap.contains(obj.poly) or trap.intersects(obj.poly):
                    dist = self.poly.distance(obj.poly)
                    if dist < to_ret[i]:
                        to_ret[i] = dist
        
        return to_ret
        

    