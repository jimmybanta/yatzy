# Reinforcement learning - with 3 q-tables

import itertools as it
import random
import json
import re
import csv
from tempfile import tempdir
from weakref import finalize

from player import AIPlayer
from hand import YatzyHand


class AIGenSevenPointZero(AIPlayer):
    def __init__(self, name, generation='7.0'):
        super().__init__(name, generation=generation)
        self.title = 'sevenpointzero'

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

        self.divisors = {
                'ones': 5, 
                'twos': 10, 
                'threes': 15, 
                'fours': 20, 
                'fives': 25, 
                'sixes': 30, 
                'one_pair': 12, 
                'two_pair': 22, 
                'three_kind': 18, 
                'four_kind': 24,
                'small_straight': 15,
                'large_straight': 20, 
                'full_house': 28, 
                'chance': 30, 
                'yatzy': 50
            }

    def available_actions(self, q_table=False):
        if q_table == 'reroll':
            return self.reroll
        elif q_table == 'indices':
            return self.indices
        elif q_table == 'moves':
            return [key for key in self.scoresheet if self.scoresheet[key] is None]

    def update_reroll(self, hand, action):
        hand = tuple([int(x) for x in hand])
        
        old_q = self.get_q_value(hand, action, q_table='reroll')
        if action == 'True':
            future = self.future_reward(hand, q_table='indices')
        else:
            future = self.future_reward(hand, q_table='moves')
        self.update_q_value(hand, action, old_q, 0, future, q_table='reroll')
    
    def update_indices(self, hand, action, new_hand):
        hand = tuple([int(x) for x in hand])
        new_hand = tuple([int(x) for x in new_hand])

        old_q = self.get_q_value(hand, action, q_table='indices')
        future = self.future_reward(new_hand, q_table='moves')

        self.update_q_value(hand, action, old_q, 0, future, q_table='indices')

    def update_moves(self, hand, action, reward):
        hand = tuple([int(x) for x in hand])

        old_q = self.get_q_value(hand, action, q_table='moves')

        self.update_q_value(hand, action, old_q, reward, 0, q_table='moves')

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
        new_q = old_q + self.alpha * (reward + future - old_q)

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
                return max(options, key= lambda x:q[(hand, x)] if (hand, x) in q.keys() else 0)
        else:
            return max(options, key= lambda x:q[(hand, x)] if (hand, x) in q.keys() else 0)

    def write_q(self):
        d = ['reroll', 'indices', 'moves']

        for dic in d:
            with open('q_tables/{}/{}.json'.format(self.title, dic), 'w') as file:
                q = getattr(self, 'q_{}'.format(dic))
                temp = {}

                for item in q.items():
                    temp[str(item[0])] = item[1]
                
                temp = sorted(temp.items(), key=lambda x:x[0])

                final = {}
                for key, value in temp:
                    final[key] = value

                json.dump(final, file, indent=2)

    def read_q(self):
        d = ['reroll', 'indices', 'moves']

        for dic in d:
            with open('q_tables/{}/{}.json'.format(self.title, dic), 'r') as file:
                q = getattr(self, 'q_{}'.format(dic))

                temp = json.load(file)

                if dic != 'indices':
                    for key, value in temp.items():
                        roll = tuple([int(x) for x in re.findall(r'\d', key)])
                        action = key[19:-2]
                        q[(roll, action)] = value

                else:
                    for key, value in temp.items():
                        roll = tuple([int(x) for x in re.findall(r'\d', key[:15])])
                        indices = tuple([int(x) for x in re.findall(r'\d', key[19:])])
                        q[(roll, indices)] = value
                
    def copy(self):
        copy = AIGenSevenPointZero(self.name)
        copy.scoresheet = self.scoresheet.copy()

        return copy
            

class AIGenSevenPointOne(AIGenSevenPointZero):
    '''Updated how to update the indices q-table'''
    def __init__(self, name, generation='7.1'):
        super().__init__(name, generation=generation)
        self.title = 'sevenpointone'

        self.one_hands = {}
        self.two_hands = {}
        self.three_hands = {}
        self.four_hands = {}
        self.five_hands = {}
    
    def update_indices(self, hand, action, new_hand=False):
        hand = tuple([int(x) for x in hand])

        old_q = self.get_q_value(hand, action, q_table='indices')

        ## get average expected value of the action
        possible_hands = self.possible_hands(hand, action)

        rewards = []

        for hand in possible_hands:
            prob = possible_hands[hand]
            reward = self.future_reward(hand, q_table='moves')

            rewards.append(prob * reward)

        future = sum(rewards)

        self.update_q_value(hand, action, old_q, 0, future, q_table='indices')

    def possible_hands(self, hand, indices):
        '''Given a hand and indices to reroll, returns a dictionary
        of possible new hands, and the probability of rolling them'''

        d = {'1':'one', '2':'two', '3':'three', '4':'four', '5':'five'}

        old_hand = [int(i) for i in hand]
        new_hand = []

        for i, die in enumerate(old_hand):
            if i not in indices:
                new_hand.append(die)

        num = len(indices)

        temp = getattr(self, '{}_hands'.format(d[str(num)]))

        final = {}

        for hand, prob in temp.items():
            final[tuple(sorted(list(hand) + new_hand))] = prob

        return final

    
    def copy(self):
        copy = AIGenSevenPointOne(self.name)
        copy.scoresheet = self.scoresheet.copy()

        return copy


    def load_new_hands(self):
        d = {'1':'one', '2':'two', '3':'three', '4':'four', '5':'five'}
        for i in range(1,6):
            new_hands = getattr(self, '{}_hands'.format(d[str(i)]))
            with open(f'new_hands/{i}.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    dice = re.findall(r'\d', row['hand'])
                    dice = [int(x) for x in dice]
                    new_hands[tuple(dice)] = float(row['probability'])

    

                    



    
if __name__ == "__main__":
    player = AIGenSevenPointOne('karen')
    player.load_new_hands()
    print(player.possible_hands((1,2,3,4,5), (0,1,2)))