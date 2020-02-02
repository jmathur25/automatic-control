import gym
from gym import spaces
import numpy as np
import math
from shapely.geometry import Polygon, Point, LinearRing
from gym.envs.classic_control import rendering
import shapely.affinity as affinity

# neighboring files
from .car_dynamics import RCCar, MAX_SENSOR_DETECT
from .config import VIEWER_DIM, MAX_SENSOR_DETECT, ROOM_DIM_X, ROOM_DIM_Y, NUM_OBJECTS, OBJECT_DIM, OBJECT_MIN_DIST, \
                INITIAL_MOTOR_LEFT, INITIAL_MOTOR_RIGHT, MAX_ITERATIONS, FRAMES_PER_SECOND, MAX_ANGULAR_VELOCITY, WHEEL_DIAMETER

"""
--------------------------------
Initialize functions
--------------------------------
"""

def get_random_pos_(max_):
    val = np.random.randint(2, max_ - 2)
    return val

def get_random_pos():
    x_pos = get_random_pos_(ROOM_DIM_X)
    y_pos = get_random_pos_(ROOM_DIM_Y)
    return x_pos, y_pos

class RoomObject:
    def __init__(self, obj_x, obj_y):
        self.center_x = obj_x
        self.center_y = obj_y
        xs = (obj_x - OBJECT_DIM/2, obj_x + OBJECT_DIM/2)
        ys = (obj_y - OBJECT_DIM/2, obj_y + OBJECT_DIM/2)
        points = [(xs[0], ys[0]), (xs[0], ys[1]), (xs[1], ys[1]), (xs[1], ys[0])]
        self.poly = Polygon(points)

class RoomWall:
    def __init__(self, center_x, center_y, x_len, y_len):
        self.center_x = center_x
        self.center_y = center_y
        xs = (center_x - x_len/2, center_x + x_len/2)
        ys = (center_y - y_len/2, center_y + y_len/2)
        points = [(xs[0], ys[0]), (xs[0], ys[1]), (xs[1], ys[1]), (xs[1], ys[0])]
        self.poly = Polygon(points)

def generate_random_object(cur_objs):
    # repeat until we get a satisfactory object
    for _ in range(100):
        x, y = get_random_pos()
        obj = RoomObject(x, y)
        isok = True
        for existing_obj in cur_objs:
            if obj.poly.distance(existing_obj.poly) < OBJECT_MIN_DIST:
                isok = False
                break
        if isok:
            return obj
    raise Exception("Could not generate all the objects")

def print_all_object_locations(objects):
    print('Object locations:')
    print('------------------')
    print(f'CAR: {objects[0].poly}')
    for i in range(1, len(objects)):
        print(f'Obj: {objects[i].poly}')
    print('\n')


"""
--------------------------------
Environment written below
--------------------------------
"""



class RCCarEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(RCCarEnv, self).__init__()

        # Action format: left motor (-1 to 1), right motor (-1 to 1)
        self.action_space = spaces.Box(low=np.array([-1, -1]), high=np.array([1, 1]), dtype=np.float16)

        # Distances in 4 directions up to X meters
        self.observation_space = spaces.Box(low=0, high=MAX_SENSOR_DETECT, shape=(1, 4), dtype=np.float16)

        # random start post in room
        start_pos_x, start_pos_y = get_random_pos() 
        self.car = RCCar(start_pos_x, start_pos_y)
        self.objects = []
        self.objects.append(self.car)
        while len(self.objects) != NUM_OBJECTS + 1:
            self.objects.append(generate_random_object(self.objects))
        
        leftwall = RoomWall(0, ROOM_DIM_Y/2, 1, ROOM_DIM_Y)
        rightwall = RoomWall(ROOM_DIM_X, ROOM_DIM_Y/2, 1, ROOM_DIM_Y)
        upwall = RoomWall(ROOM_DIM_X/2, ROOM_DIM_Y, ROOM_DIM_X, 1)
        downwall = RoomWall(ROOM_DIM_X/2, 0, ROOM_DIM_X, 1)
        self.objects.append(leftwall)
        self.objects.append(rightwall)
        self.objects.append(upwall)
        self.objects.append(downwall)

        self.viewer = None

        self.iterations = 0

    def step(self, action):
        # execution action of form np.array([left_motor, right_motor])
        self.car.update(action, self.objects)
        #print(action)
        self.iterations += 1

        obs = self.measure_observations()
        reward = self.compute_reward(obs)

        if self.iterations == MAX_ITERATIONS:
            done = True
        else:
            done = False

        return obs, reward, done, {}

    def measure_observations(self):
        ''' Measure distance from car to objects using 6 "sensors" '''
        sensor_data = self.car.get_sensor_data(self.objects)
        return np.array(sensor_data)

    def compute_reward(self, obs):
        ''' Compute reward '''
        penalties = self.car.get_penalties()
        speed = math.sqrt((self.car.cur_x - self.car.prev_x)**2 + (self.car.cur_y - self.car.prev_y)**2) * 1/FRAMES_PER_SECOND
        speed_max = MAX_ANGULAR_VELOCITY * WHEEL_DIAMETER / 2 * 1/FRAMES_PER_SECOND
        speed_norm = speed / speed_max

        speed_reward = 10 * speed_norm

        # penalize being near an obstacle and going fast
        a = 50
        closest_obs = np.min(obs)
        if closest_obs <= 0:
            closest_obs = 0.01
        obstacle_reward = -a * (speed_norm * 1/closest_obs)

        # each penalty is -20
        penalties_reward = penalties * -20

        return speed_reward + obstacle_reward + penalties_reward

    def reset(self):
        # random start post in room
        start_pos_x, start_pos_y = get_random_pos() 
        self.car = RCCar(start_pos_x, start_pos_y)
        self.objects = []
        self.objects.append(self.car)
        while len(self.objects) != NUM_OBJECTS + 1:
            self.objects.append(generate_random_object(self.objects))
        
        leftwall = RoomWall(0, ROOM_DIM_Y/2, 1, ROOM_DIM_Y)
        rightwall = RoomWall(ROOM_DIM_X, ROOM_DIM_Y/2, 1, ROOM_DIM_Y)
        upwall = RoomWall(ROOM_DIM_X/2, ROOM_DIM_Y, ROOM_DIM_X, 1)
        downwall = RoomWall(ROOM_DIM_X/2, 0, ROOM_DIM_X, 1)
        self.objects.append(leftwall)
        self.objects.append(rightwall)
        self.objects.append(upwall)
        self.objects.append(downwall)

        self.viewer = None

        self.iterations = 0

    def poly_to_coords(self, poly, factor=20, expand=1):
        if expand != 1:
            poly = affinity.scale(poly, xfact=expand, yfact=expand)
        pts = poly.exterior.coords.xy
        points = [(factor*pts[0][i] + 100, factor*pts[1][i] + 100) for i in range(len(pts[0]))]
        return points
    
    def render(self, mode='human', close=False):
        # Render the environment to the screen
        if self.viewer is None:
            self.viewer = rendering.Viewer(VIEWER_DIM, VIEWER_DIM)

            for obj in self.objects[1:]:
                points = self.poly_to_coords(obj.poly)
                part = rendering.FilledPolygon(points)
                # part = rendering.FilledPolygon([(100,100), (100,200), (200,200), (200,100)])
                self.viewer.add_geom(part)

            # render car
            car = self.objects[0]
            points = self.poly_to_coords(car.poly, expand=10)
            self.car_render = rendering.FilledPolygon(points)
            self.viewer.add_geom(self.car_render)
        else:
            car = self.objects[0]
            points = self.poly_to_coords(car.poly, expand=10)
            self.car_render.v = points

        self.viewer.render()

        return None

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None


