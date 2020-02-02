import torch
import numpy as np
from model import Agent

STATE_SIZE = 6
ACTION_SIZE = 2

class ModelInterface():
    def __init__(self):
        self.agent = Agent(state_size=STATE_SIZE, action_size=ACTION_SIZE, random_seed=10)
        self.agent.actor_local.load_state_dict(torch.load('model/checkpoint_actor.pth', map_location='cpu'))
        self.agent.critic_local.load_state_dict(torch.load('model/checkpoint_critic.pth', map_location='cpu'))
        self.agent.actor_local.eval()
        self.agent.critic_local.eval()

    def get_action_q(self, state, action):
        s = np.zeros((128, 6))
        s[0, :] = state
        
        a = np.zeros((128, 2))
        a[0, :] = action
        
        state = torch.Tensor(s)
        action = torch.Tensor(a)
        
        return self.agent.critic_local(state, action).detach().numpy()[0, 0]

    def get_action(self, state):
        return self.agent.act(state)

