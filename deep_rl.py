import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

import random
from collections import deque, namedtuple
import itertools as it
import math
import re


Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))

MovesTransition = namedtuple('MoveTransition', 
                            ('state', 'move', 'reward'))
RerollTransition = namedtuple('RerollTransition',
                            ('state', 'reroll', 'next_state'))
IndicesTransition = namedtuple('IndicesTransition', 
                            ('state', 'indices', 'next_state'))

## Objects


## Gen 8.0
class ReplayMemory(object):
    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)
    
    def push(self, *args):
        self.memory.append(Transition(*args))
    
    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)
    
    def __len__(self):
        return len(self.memory)


class DQN(nn.Module):
    def __init__(self, output):
        super().__init__()
        self.layer1 = nn.Linear(20, 64)
        self.layer2 = nn.Linear(64, 32)
        self.layer3 = nn.Linear(32, output)
    
    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        return self.layer3(x)


## Gen 8.1

class MovesReplayMemory(ReplayMemory):
    def push(self, *args):
        self.memory.append(MovesTransition(*args))
    


class IndicesReplayMemory(ReplayMemory):
    def push(self, *args):
        self.memory.append(IndicesTransition(*args))


class RerollReplayMemory(ReplayMemory):  
    def push(self, *args):
        self.memory.append(RerollTransition(*args))




## Helper Functions

# Gen 8.0

def create_value_action_dict(player):
    '''Creates a dictionary mapping values to actions.'''
    actions = {}

    counter = 0
    for action in player.scoresheet.keys():
        actions[counter] = action
        counter += 1


    rerolls = []
    for i in range(1, 6):   
        for combo in it.combinations([0, 1, 2, 3, 4], r=i):
            rerolls.append('reroll {}'.format(combo))

    for roll in rerolls:
        actions[counter] = roll
        counter += 1
    
    return actions

def create_action_value_dict(actions):
    final = {}

    for key, value in actions.items():
        final[value] = key
    
    return final





def available_actions(scoresheet, reroll=False):
    available = {}
    for i, (key, value) in enumerate(scoresheet.items()):
        if value is not None:
            available[i] = False
        else:
            available[i] = True
    for i in range(15, 46):
        available[i] = bool(reroll)
    return available


def select_action(state, available_actions, episode_num, eps_final, eps_initial, eps_decay, device, target_net):
    # returns a number between 1 and 46 that tells you what action to take
    sample = random.random()
    eps_threshold = eps_final + (eps_initial - eps_final) * math.exp(-1.0 * episode_num / eps_decay)
    if sample < eps_threshold:
        return torch.tensor(random.choice([x for x in available_actions if available_actions[x]])).view(1).to(device)
    else:
        with torch.no_grad():
            results = target_net(state)
            for i in range(46):
                if available_actions[i] == False:
                    results[i] = 0
            return torch.argmax(results).view(1).to(device)


def create_state(scoresheet, hand):
    s = []

    for key, value in scoresheet.items():
        if not isinstance(value, int):
            s.append(0)
        else:
            s.append(value)

    for die in hand:
        s.append(float(die) * 10)

    return torch.tensor(s)


def get_indices(action):
    numbers = re.findall(f'\d', action)
    return [int(x) for x in numbers]


def check_end(scoresheet):
    return all([isinstance(x, int) for x in scoresheet.values()])


def first_turn(scoresheet):
    return True if list(scoresheet.values()).count(None) == len(scoresheet.values()) else False


def check_state_end(state):
    state = list(state)
    return all([x != 0 for x in state])


def optimize_model(memory, bs, policy_net, device, target_net, opt):
    if len(memory) < bs:
        return
    transitions = memory.sample(bs)

    batch = Transition(*zip(*transitions))

    non_final_mask = torch.tensor(tuple(map(lambda s: not check_state_end(s), batch.next_state)), device=device, dtype = torch.bool)

    state_batch = torch.stack(batch.state)
    action_batch = torch.stack(batch.action)
    non_final_next_states = torch.stack([s for s in batch.next_state if not check_state_end(s)])
    reward_batch = torch.cat(batch.reward)

    state_action_values = policy_net(state_batch).gather(1, action_batch).squeeze()
    
    next_state_values = torch.zeros(bs, device=device)
    next_state_values[non_final_mask] = target_net(non_final_next_states).max(1)[0].detach()
    
    expected_state_action_values = next_state_values + reward_batch

    criterion = nn.SmoothL1Loss()
    loss = criterion(state_action_values, expected_state_action_values)

    opt.zero_grad()
    loss.backward()
    opt.step()


# Gen 8.1

def create_action_dicts():
    moves = {}
    reroll = {}
    indices = {}

    player = AIGenSevenPointZero('karen')

    for i, item in enumerate(player.moves):
        moves[i] = item

    for i, item in enumerate(player.reroll):
        reroll[i] = item
    
    for i, item in enumerate(player.indices):
        indices[i] = item

    return moves, reroll, indices

def available_moves(scoresheet):
    available = {}
    for i, (key, value) in enumerate(scoresheet.items()):
        if value is not None:
            available[i] = False
        else:
            available[i] = True
    return available


def available_rerolls():
    return {0: True, 1: True}

def available_indices():
    final = {}
    for i in range(1, 6):
         for comb in it.combinations([0, 1, 2, 3, 4], i):
            final.append(comb)
    return final



if __name__ == '__main__':
    player = AIGenThreePointOne('karen')
    print(create_state(player.scoresheet, YatzyHand()))