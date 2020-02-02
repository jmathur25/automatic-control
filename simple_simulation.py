import gym
import rc_car_env
import numpy as np
from model_interface import ModelInterface

env = gym.make('rc_car_env-v0')
state = env.reset(simple=True)
mi = ModelInterface()

default_action = np.array([1, 1])

for _ in range(100):
    env.render()
    ma = mi.get_action(state)
    print("state", state)
    print("model action:", ma)
    print("expected q for model action:", mi.get_action_q(state, ma))
    print("expected q for input:", mi.get_action_q(state, default_action))
    state, reward, done, info = env.step(default_action)
    print("reward:", reward)
    print("--------------------------------\n\n")
    if done:
        break
    
