import gym
import rc_car_env
import numpy as np
env = gym.make('rc_car_env-v0')

num_episodes = 10

for _ in range(num_episodes):
    for _ in range(100):
        env.render()
        obs, reward, done, info = env.step(np.array([1, 1]))
        print("reward:", reward)
        if done:
            break
    env.close()
    while True:
        try:
            env.reset()
            break
        except:
            continue
            
print("ran successfully")

