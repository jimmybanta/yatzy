# Reinforcement learning - with 3 q-tables

import itertools as it
import random

from player import AIPlayer


class AIGenSevenPointZero(AIPlayer):
    def __init__(self, name, generation='7.0'):
        super().__init__(name, generation=generation)

        self.q_reroll = {}
        self.q_indices = {}
        self.q_moves = {}

        self.alpha = 0.5
        self.epsilon = 0.75

        self.indices = []
        for i in range(1, 6):
            for comb in it.combinations([0, 1, 2, 3, 4], i):
                self.indices.append(comb)
        
        self.reroll = ['True', 'False']
        self.moves = [key for key in self.scoresheet]

    
    def available_actions(self, q_table=False):
        if q_table == 'reroll':
            return self.reroll
        elif q_table == 'indices':
            return self.indices
        elif q_table == 'moves':
            return [key for key in self.scoresheet if self.scoresheet[key] is None]

    
    def update(self, old_hand, action, reward, new_hand=False, q_table=False):
        old_hand = tuple([int(x) for x in old_hand])
        new_hand = tuple([int(x) for x in new_hand]) if new_hand else False

        old_q = self.get_q_value(old_hand, action, q_table=q_table)

        if new_hand:
            future = self.future_reward(new_hand, q_table=q_table)
            self.update_q_value(old_hand, action, old_q, reward, future, q_table=q_table)
        else:
            self.update_q_value(old_hand, action, old_q, reward, 0, q_table=q_table)

    def get_q_value(self, hand, action, q_table=False):
        key = (hand, action)

        q = getattr(self, 'q_{}'.format(q_table))

        if key in q.keys():
            return q[key]
        else:
            return 0
    
    def future_reward(self, state, q_table=False):
        q = getattr(self, 'q_{}'.format(q_table))
        rewards = []
        for key in q:
            if state in key:
                rewards.append(q[key])
        
        rewards.append(0)
        return max(rewards)


    def update_q_value(self, hand, action, old_q, reward, future, q_table=False):
        new_q = old_q + self.alpha(reward + future - old_q)

        q = getattr(self, 'q_{}'.format(q_table))

        q[(hand, action)] = new_q


    def choose_action(self, hand, epsilon=False, q_table=False):
        hand = tuple([int(x) for x in hand])

        options = self.available_actions(q_table=q_table)
        q = getattr(self, 'q_{}'.format(q_table))

        random.shuffle(options)

        if epsilon:
            if random.random() < self.epsilon:
                return random.choice(options)
            else:
                return max(options, key= lambda x:q[(hand, x) if (hand, x) in q.keys() else 0])
        else:
            return max(options, key= lambda x:q[(hand, x) if (hand, x) in q.keys() else 0])


            


    
if __name__ == "__main__":
    player = AIGenSevenPointZero('karen')
    player.scoresheet['ones'] = 2
    print(player.available_actions(q_table='moves'))