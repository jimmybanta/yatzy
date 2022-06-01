
import random

from player import AIPlayer


class AIGenOnePointZero(AIPlayer):
    '''50% chance of choosing to reroll, 50% chance of rerolling any one die, random choice of move'''
    def __init__(self, name, generation='1.0'):
        super().__init__(name, generation=generation)
        self.prob = 0.5

    def choose_move(self, hand=False):
        return random.choice([item for item in self.scoresheet if self.scoresheet[item] == None])

    def choose_reroll(self, hand=False):
        return True if random.random() < self.prob else False

    def choose_indices(self, hand=False):
        return[i for i in range(5) if random.random() < self.prob]


class AIGenOnePointOne(AIGenOnePointZero):
    '''Never rerolls, random choice of move'''
    def __init__(self, name, generation='1.1'):
        super().__init__(name, generation=generation)

    def choose_reroll(self, hand=False):
        return False


class AIGenOnePointTwo(AIGenOnePointZero):
    '''Always rerolls, 50% chance of rerolling any die, random choice of move'''
    def __init__(self, name, generation='1.2'):
        super().__init__(name, generation=generation)

    def choose_reroll(self, hand=False):
        return True
