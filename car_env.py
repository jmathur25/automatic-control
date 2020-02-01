import gym
from gym import spaces
import numpy as np
from shapely.geometry import Polygon, Point, LinearRing

RANDOM_SEED = 7
np.random.seed(RANDOM_SEED)

MAX_SENSOR_DETECT = 5
ROOM_DIM_X = 20
ROOM_DIM_Y = 20
NUM_OBJECTS = 5

RC_ROBOT_DIM_X = 0.1
RC_ROBOT_DIM_Y = 0.1

OBJECT_DIM = 2 # all objects dim
OBJ_MIN_DIST = 1 # all objects must be at least this away from start

INITIAL_MOTOR_LEFT = 0
INITIAL_MOTOR_RIGHT = 0

def get_random_pos_(max_):
    val = np.random.randint(2, max_ - 2)
    return val

def get_random_pos():
    x_pos = get_random_pos_(ROOM_DIM_X)
    y_pos = get_random_pos_(ROOM_DIM_Y)
    return x_pos, y_pos

# random start post in room
START_POS_X, START_POS_Y = get_random_pos()

class RCCar:
    def __init__(self, start_x, start_y):
        self.cur_x = start_x
        self.cur_y = start_y
        xs = (START_POS_X - RC_ROBOT_DIM_X/2, START_POS_X + RC_ROBOT_DIM_X/2)
        ys = (START_POS_Y - RC_ROBOT_DIM_Y/2, START_POS_Y + RC_ROBOT_DIM_Y/2)
        points = [(xs[0], ys[0]), (xs[0], ys[1]), (xs[1], ys[1]), (xs[1], ys[0])]
        self.poly = Polygon(points)
    
CAR = RCCar(START_POS_X, START_POS_Y)

class RoomObject:
    def __init__(self, obj_x, obj_y):
        self.center_x = obj_x
        self.center_y = obj_y
        xs = (obj_x - OBJECT_DIM/2, obj_x + OBJECT_DIM/2)
        ys = (obj_y - OBJECT_DIM/2, obj_y + OBJECT_DIM/2)
        points = [(xs[0], ys[0]), (xs[0], ys[1]), (xs[1], ys[1]), (xs[1], ys[0])]
        self.poly = Polygon(points)

def generate_random_object(cur_objs):
    # repeat until we get a satisfactory object
    for _ in range(100):
        x, y = get_random_pos()
        obj = RoomObject(x, y)
        if obj.poly.distance(CAR.poly) > OBJ_MIN_DIST:
            isok = True
            for existing_obj in cur_objs:
                if obj.poly.distance(existing_obj.poly) < OBJ_MIN_DIST:
                    isok = False
                    break
            if isok:
                return obj
    raise Exception("Could not generate all the objects")
            
OBJECTS = []
while len(OBJECTS) != NUM_OBJECTS:
    OBJECTS.append(generate_random_object(OBJECTS))

def print_all_object_locations():
    print('Object locations:')
    print('------------------')
    print(f'CAR x,y: {CAR.cur_x},{CAR.cur_y}')
    for obj in OBJECTS:
        print(f'Obj x,y: {obj.center_x},{obj.center_y}')
    print('\n')

print_all_object_locations()

class RCCarEnv(gym.Env):
  """Custom Environment that follows gym interface"""
  metadata = {'render.modes': ['human']}

  def __init__(self):
    super(RCCarEnv, self).__init__()

    # Action format: left motor (-1 to 1), right motor (-1 to 1)
    self.action_space = spaces.Box(low=np.array([-1, -1]), high=np.array([1, 1]), dtype=np.float16)

    # Distances in 4 directions up to X meters
    self.observation_space = spaces.Box(low=0, high=MAX_SENSOR_DETECT, shape=(1, 4), dtype=np.float16)

  def step(self, action):
    # Execute one time step within the environment

    return observation, reward
    
  def reset(self):
    # Reset the state of the environment to an initial state

    
  def render(self, mode='human', close=False):
    # Render the environment to the screen

