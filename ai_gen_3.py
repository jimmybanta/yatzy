import random

from ai_gen_2 import AIGenTwoPointZero
from hand import YatzyHand

class AIGenThreePointZero(AIGenTwoPointZero):
    def __init__(self, name, generation='3.0'):
        super().__init__(name, generation=generation)
        self.override_values = {'yatzy': 50, 'large_straight': 20, 'small_straight': 15, 'full_house': 22,
                'four_kind': 20, 'three_kind': 15, 'two_pair': 18, 'chance': 24}
        self.override_values = {}

    def override(self, hand):
        print(self.override_values)
        for move in self.override_values:
            if getattr(hand, move)() >= self.override_values[move] and move in self.options:
                return move
        return False


class AIGenThreePointOne(AIGenThreePointZero):
    def __init__(self, name, generation='3.1'):
        super().__init__(name, generation=generation)

    def choose_reroll(self):
        return True

class AIGenThreePointTwo(AIGenThreePointOne):
    def __init__(self, name, generation='3.2'):
        super().__init__(name, generation=generation)
        self.prob = 0.5
    
    def choose_nums(self, hand):
        indices_lower = [i for i, die in enumerate(hand) if die.value in [1,2,3]]
        
        indices_upper = [i for i in range(5) if random.random() < self.prob]

        return indices_lower if indices_lower else indices_upper



if __name__ == '__main__':
    player = AIGenThreePointTwo('karen')
    hand = YatzyHand([1,2,3,4,5])
    print(hand)
    print(player.choose_nums(hand))