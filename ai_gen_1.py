
import random

from player import AIPlayer


class AIGenOnePointZero(AIPlayer):
    '''50% chance of choosing to reroll, 50% chance of rerolling any one die, random choice of move'''
    def __init__(self, name):
        super().__init__(name, generation='1.0')

    def choose_move(self):
        return random.choice([item for item in self.scoresheet if self.scoresheet[item] == None])

    def choose_reroll(self):
        return True if random.random() < 0.5 else False

    def choose_indices(self):
        return[i for i in range(5) if random.random() < 0.5]


class AIGenOnePointOne(AIGenOnePointZero):
    '''Never rerolls, random choice of move'''
    def __init__(self, name):
        super().__init__(name, generation='1.1')

    def choose_reroll(self):
        return False


class AIGenOnePointTwo(AIGenOnePointZero):
    '''Always rerolls, 50% chance of rerolling any die, random choice of move'''
    def __init__(self, name):
        super().__init__(name, generation='1.2')

    def choose_reroll(self):
        return True



def reroll(self, nums):
    rerolled = []
    for num in nums:
        for die in self:
            if die == num and die not in rerolled:
                die.value = random.randint(1,6)
                rerolled.append(die)
                break