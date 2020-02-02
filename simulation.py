import gym
import rc_car_env
import numpy as np
from model_interface import ModelInterface
import sys
mi = ModelInterface()

if __name__ == "__main__":
    simple = True
    assert len(sys.argv) == 3
    assert sys.argv[1] in ['simple', 'regular'], print("arg: simple OR regular")
    simple = sys.argv[1] == 'simple'
    num_it = int(sys.argv[2])

    env = gym.make('rc_car_env-v0')
    state = env.reset(simple=simple)

    default_action = np.array([1, 1])
        
    THRESHOLD = 20

    for _ in range(num_it):
        env.render()
        ma = mi.get_action(state)
        print("state", state.tolist())
        print("model action:", ma)
        print("expected q for model action:", mi.get_action_q(state, ma))
        exp_q = mi.get_action_q(state, default_action)
        print("expected q for input:", mi.get_action_q(state, default_action))
        state, reward, done, info = env.step(default_action)
        if exp_q < THRESHOLD:
            # default_action = np.array([-1, -1])
            # model can take over
            default_action = mi.get_action(state)
        print("reward:", reward)
        print("--------------------------------\n\n")
        if done:
            break


