import numpy as np
import math

RANDOM_SEED = 7
np.random.seed(RANDOM_SEED)

# Environment parameters

VIEWER_DIM = 500 # screen pixels

ROOM_DIM_X = 10
ROOM_DIM_Y = 10
NUM_OBJECTS = 10

OBJECT_DIM = 0.5 # all objects dim
OBJECT_MIN_DIST = 0.5 # all objects must be at least this away from each other

MAX_ITERATIONS = 10000

# Robot parameters
MAX_SENSOR_DETECT = 3.5
INITIAL_MOTOR_LEFT = 0
INITIAL_MOTOR_RIGHT = 0
MIN_TIME_PER_ROTATION = 1.32

WHEEL_DIAMETER = 0.0685
MAX_ANGULAR_VELOCITY = 2 * math.pi / MIN_TIME_PER_ROTATION
WHEEL_DISTANCE = 0.02

RC_ROBOT_DIAMETER = 0.02

FRAMES_PER_SECOND = 10

