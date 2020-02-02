from gym.envs.registration import register

register(
    id='rc_car_env-v0',
    entry_point='rc_car_env.envs:RCCarEnv',
)
