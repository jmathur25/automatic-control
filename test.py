import gym
import rc_car_env
import numpy as np
env = gym.make('rc_car_env-v0')



for _ in range(100):
    env.render()
    env.step(np.array([1, 1]))
    # random = env.action_space.sample()
    
# env.close()

# from shapely.geometry import Polygon
# poly = Polygon([ (0, 0), (0, 1), (1, 1), (1, 0)])
# print(poly.exterior.coords.xy)



