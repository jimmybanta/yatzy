import random

from player import AIPlayer
from ai_gen_1 import AIGenOnePointZero
from hand import YatzyHand


class AIGenTwoPointZero(AIGenOnePointZero):
    '''Chooses the max scoring move; 50% probability of rerolling, 50% probability of rerolling any one die.'''
    def __init__(self, name, generation='2.0'):
        super().__init__(name, generation=generation)
        
    def choose_move(self, hand):
        '''Returns the max scoring move.
            If there are multiple that score the max, it returns one of them at random.'''
        options = {key: getattr(hand, key)() for key, value in self.scoresheet.items() if value is None}
        final = list(options.items())
        random.shuffle(final)
        print(final)
        return max(final, key=lambda x:x[1])[0]
        

class AIGenTwoPointOne(AIGenTwoPointZero):
    def __init__(self, name, generation='2.1'):
        super().__init__(name, generation=generation)

    def choose_reroll(self):
        return True
    
    def choose_nums(self):
        return [0,1,2,3,4]





if __name__ == '__main__':
    player = AIGenTwoPointZero('karen')
    player.scoresheet =  {'ones': None, 'twos': 1, 'threes': None, 'fours': 1, 'fives': 1, 'sixes': None, 
                            'one_pair': None, 'two_pair': None, 'three_kind': None, 'four_kind': 1, 'small_straight': None, 
                            'large_straight': 1, 'full_house': 1, 'chance': 1, 'yatzy': None}
    hand = YatzyHand([1,2,3,6,6])
    print(hand)
    print(player.choose_play(hand))