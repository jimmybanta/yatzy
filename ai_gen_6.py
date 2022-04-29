## Reinforcement learning

from multiprocessing.spawn import old_main_modules
import random
import itertools as it
import json

from player import AIPlayer



class ai_gen_sixpointzero(AIPlayer):
    def __init__(self, name, generation='6.0'):
        super().__init__(name, generation=generation)
        self.q = {}
        self.alpha = .5
        self.epsilon = .75

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
        
    
    def update(self, old_hand, action, reward, new_hand=False):
        old_hand = tuple([int(x) for x in old_hand])
        new_hand = tuple([int(x) for x in new_hand]) if new_hand else False

        old_q = self.get_q_value(old_hand, action)
        if new_hand:
            future = self.future_reward(new_hand)
            self.update_q_value(old_hand, action, old_q, reward, future)
        else:
            self.update_q_value(old_hand, action, old_q, reward, 0)


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
        

    def write_q(self, filename):
        with open('q_tables/{}.json'.format(filename), 'w') as file:
            temp = {}
            for item in self.q.items():
                temp[str(item[0])] = item[1]
            
            temp = sorted(temp.items(), key=lambda x:x[0])

            final = {}
            for key, value in temp:
                final[key] = value

            json.dump(final, file, indent=2)

    
    def read_q(self, filename):
        with open('q_tables/{}.json'.format(filename), 'r') as file:
            temp = json.load(file)
            for key, value in temp.items():
                roll = (int(key[2]), int(key[5]), int(key[8]), int(key[11]), int(key[14]))
                action = key[19:-2]
                self.q[(roll, action)] = value


            
    def copy(self):
        copy = ai_gen_sixpointone(self.name)
        copy.scoresheet = self.scoresheet.copy()

        return copy


class ai_gen_sixpointone(ai_gen_sixpointzero):
    def __init__(self, name, generation='6.1'):
        super().__init__(name, generation=generation)
        self.q = {}
        self.alpha = .5
        self.epsilon = .75

        self.reroll_actions = []
        for i in range(1, 6):
            for comb in it.combinations([0, 1, 2, 3, 4], i):
                self.reroll_actions.append(comb)
        
        self.actions_no_reroll = [key for key in self.scoresheet]


    def future_reward(self, state):
        rewards = []
        for key in self.q.keys():
            if key[0] == state and key[1] in self.actions_no_reroll:
                rewards.append(self.q[key])

        return sum(rewards) / len(rewards) if rewards else 0


if __name__ == '__main__':

    player = ai_gen_sixpointone('joe')

    print(player.generation)
    
    
