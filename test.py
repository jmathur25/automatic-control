import gym
import rc_car_env
env = gym.make('rc_car_env-v0')

for _ in range(100):
    env.render()
    env.step(env.action_space.sample())

