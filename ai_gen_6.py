## Reinforcement learning

from multiprocessing.spawn import old_main_modules
import random
import itertools as it

from player import AIPlayer



class ai_gen_sixpointzero(AIPlayer):
    def __init__(self, name, generation='6.0'):
        super().__init__(name, generation=generation)
        self.q = {}
        self.alpha = .5
        self.epsilon = .5

        self.reroll_actions = []
        for i in range(1, 6):
            for comb in it.combinations([0, 1, 2, 3, 4], i):
                self.reroll_actions.append(comb)

    
    def available_actions(self, reroll=False):
        actions = []

        for action in self.scoresheet:
            if self.scoresheet[action] == None:
                actions.append(action)
        
        if reroll:
            for ra in self.reroll_actions:
                actions.append('reroll {}'.format(ra))
        
        return actions
        
    
    def update(self, old_state, action, new_state, reward):
        old_state = tuple(old_state)
        new_state = tuple(new_state)
        old_q = self.get_q_value(old_state, action)
        future = self.future_reward(new_state)
        self.update_q_value(old_state, action, old_q, reward, future)


    def get_q_value(self, state, action):
        key = (state, action)

        if key in self.q.keys():
            return self.q[key]
        else:
            return 0
    
    def future_reward(self, state):
        rewards = []
        for key in self.q.keys():
            if state in key:
                rewards.append(self.q[key])

        rewards.append(0)
        return max(rewards)
    
    def update_q_value(self, state, action, old_q, reward, future):
        new_q = old_q + self.alpha * (reward + future - old_q)
        self.q[(state, action)] = new_q
    

    def choose_action(self, hand, epsilon=False, reroll=False):
        state = tuple([int(x) for x in hand])

        actions = self.available_actions(reroll)
        
        random.shuffle(actions)

        if epsilon:
            if random.random() < self.epsilon:
                print('BAA')
                return random.choice(actions)
            else:
                return max(actions, key=lambda x:self.q[(state, x)] if (state, x) in self.q.keys() else 0)
        else:
            return max(actions, key=lambda x:self.q[(state, x)] if (state, x) in self.q.keys() else 0)
                


    def populate_q(self):
        for i in range(6):
            l = tuple([i] * 5)
            key = (l, 'yatzy')
            self.q[key] = random.randint(0, 4)
            if i == 1:
                self.q[(l, 'ones')] = random.randint(0,4)
                self.q[(l, 'twos')] = random.randint(0,4)
        



if __name__ == '__main__':

    player = ai_gen_sixpointzero('joe')
    print(player.available_actions())

