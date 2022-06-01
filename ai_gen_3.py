import random

from ai_gen_2 import AIGenTwoPointZero
from hand import YatzyHand

class AIGenThreePointZero(AIGenTwoPointZero):
    '''Prioritizes getting bottom-sheet by choosing moves based on the override values; 
        if none, then it chooses by highest score. 
        50% probability of rerolling; 50% probability of rerolling any one die.'''
    def __init__(self, name, generation='3.0'):
        super().__init__(name, generation=generation)
        self.override_values = {'yatzy': 50, 'large_straight': 20, 'small_straight': 15, 'full_house': 22,
                'four_kind': 20, 'three_kind': 15, 'two_pair': 18, 'chance': 24}

    def override(self, hand):
        for move in self.override_values:
            if getattr(hand, move)() >= self.override_values[move] and move in self.options:
                return move
        return False

    def choose_reroll(self, hand):
        if self.override(hand): return False

        return super().choose_reroll()

    def choose_move(self, hand):
        override = self.override(hand)
        if override: return override
        
        return super().choose_move(hand)



class AIGenThreePointOne(AIGenThreePointZero):
    '''Prioritizes getting bottom-sheet by choosing moves based on the override values; 
        if none, then it chooses by highest score. 
        Always rerolls; 50% probability of rerolling any one die.'''
    def __init__(self, name, generation='3.1'):
        super().__init__(name, generation=generation)

    def choose_reroll(self, hand):
        return False if self.override(hand) else True


class AIGenThreePointTwo(AIGenThreePointOne):
    '''Prioritizes getting bottom-sheet by choosing moves based on the override values; 
        if none, then it chooses by highest score. 
        Always rerolls; Rerolls any 1's, 2's, or 3's. If there are none, 50% chance of rerolling a 4, 5, or 6.'''
    def __init__(self, name, generation='3.2'):
        super().__init__(name, generation=generation)
        self.prob = 0.5
    
    def choose_indices(self, hand):
        indices_lower = [i for i, die in enumerate(hand) if die.value in [1,2,3]]
        
        indices_upper = [i for i in range(5) if random.random() < self.prob]

        return indices_lower if indices_lower else indices_upper



if __name__ == '__main__':
    player = AIGenThreePointTwo('karen')
    hand = YatzyHand([1,2,3,4,5])
    print(hand)
    print(player.choose_nums(hand))