import random

from ai_gen_3 import AIGenThreePointTwo
from hand import YatzyHand
import pdb

class AIGenFourPointZero(AIGenThreePointTwo):
    def __init__(self, name, generation='4.0'):
        super().__init__(name, generation=generation)

        self.override_values = {'yatzy': 50, 'large_straight': 20, 'small_straight': 15, 'full_house': 22,
                'four_kind': 20, 'three_kind': 15, 'two_pair': 18, 'chance': 25, 'sixes': 18, 'fives': 15, 
                'fours': 12, 'threes': 9, 'twos': 6, 'ones': 3}


class AIGenFourPointOne(AIGenThreePointTwo):
    def __init__(self, name, generation='4.1'):
        super().__init__(name, generation=generation)
        self.override_values = {'large_straight': 20, 'small_straight': 15, 'full_house': 22,
                'four_kind': 20, 'three_kind': 15, 'two_pair': 18, 'chance': 25, 'sixes': 18, 'fives': 15, 
                'fours': 12, 'threes': 9, 'twos': 6, 'ones': 3}
        self.prob = 0.5

    def override(self, hand):

        if hand.yatzy() == 50 and 'yatzy' in self.options:
            return 'yatzy'
        elif hand.four_kind() and 'yatzy' in self.options:
            return False

        return super().override(hand)


    def choose_nums(self, hand):

        if hand.four_kind() and not hand.yatzy():
            return [0] if hand[0] != hand[1] else [4]

        return super().choose_nums(hand)


class AIGenFourPointTwo(AIGenFourPointOne):
    def __init__(self, name, generation='4.2'):
        super().__init__(name, generation=generation)
        self.prob = 0.5
        self.override_values = {'sixes': 18, 'fives': 15, 'fours': 12, 
                                'threes': 9, 'twos': 6, 'ones': 3, 
                                'large_straight': 20, 'small_straight': 15, 'full_house': 22,
                                'four_kind': 20, 'three_kind': 15, 
                                'two_pair': 18, 'chance': 25}

    def choose_nums(self, hand):
        if hand.four_kind() and not hand.yatzy():
            return [0] if hand[0] != hand[1] else [4]

        return [i for i in range(5) if random.random() < self.prob]
        



class AIGenFourPointThree(AIGenFourPointTwo):
    def __init__(self, name, generation='4.3'):
        super().__init__(name, generation=generation)
        self.prob = 0.5
        self.override_values_1 = {'yatzy': 50, 'sixes': 18, 'fives': 15, 'fours': 12, 
                                'threes': 9, 'twos': 6, 'ones': 3}
        self.override_values_2 = {'large_straight': 20, 'small_straight': 15, 'full_house': 22,
                                'four_kind': 20, 'three_kind': 15, 
                                'two_pair': 18, 'chance': 25}
    
    def override(self, hand):
        
        for move in self.override_values_1:
            if getattr(hand, move)() >= self.override_values[move] and move in self.options:
                return move

        if hand.four_kind() and 'yatzy' in self.options:
            return False

        for move in self.override_values_2:
            if getattr(hand, move)() >= self.override_values[move] and move in self.options:
                return move
        
        return False


if __name__ == '__main__':
    player = AIGenFourPointOne('karen')
    hand = YatzyHand([1,1,1,1,5])
    print(hand)
    print(player.override(hand))


