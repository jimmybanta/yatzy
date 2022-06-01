
import random

from ai_gen_3 import AIGenThreePointTwo
from ai_gen_4 import AIGenFourPointThree

## need to keep refactoring

class AIGenFivePointZero(AIGenThreePointTwo):
    '''Prioritizes the top-sheet by rerolling to try to get at least 3 of a number.
        Then it prioritizes yatzy, then bottom-sheet, then chooses a move randomly. 
        Always rerolls.'''
    def __init__(self, name, generation='5.0'):
        super().__init__(name, generation=generation)
        self.override_values = {'yatzy': 50, 'sixes': 18, 'fives': 15, 'fours': 12, 
                                'threes': 9, 'twos': 6, 'ones': 3, 
                                'large_straight': 20, 'small_straight': 15, 'full_house': 22,
                                'four_kind': 20, 'three_kind': 15, 
                                'two_pair': 18, 'chance': 25}

    def reroll_for_topsheet(self, hand, value):
        plays = ['sixes', 'fives', 'fours', 'threes', 'twos', 'ones']
        indices = []

        for i, play in enumerate(plays):
            num = 6 - i
            if hand.count(num) >= value and play in self.options:
                for i, die in enumerate(hand):
                    if die != num:
                        indices.append(i)
                break

        return indices if indices else False

    def choose_indices(self, hand):
        top = self.reroll_for_topsheet(hand, 2)

        return super().choose_indices(hand) if not top else top
        
    def choose_move(self, hand):
        override = self.override(hand)
        if override: return override

        return random.choice(self.options)



class AIGenFivePointOne(AIGenFourPointThree, AIGenFivePointZero):
    '''Prioritizes the top-sheet by rerolling to try to get at least 3 of a number.
        Then it prioritizes yatzy, then bottom-sheet, then chooses a move randomly - first from bottom sheet, then from top. 
        Always rerolls. Chooses indicess by rerolling for top-sheet, then yatzy, then rerolling lower dice.'''
    def __init__(self, name, generation='5.1'):
        super().__init__(name, generation=generation)
    
    def choose_move(self, hand):
        override = self.override(hand)
        if override: return override

        return random.choice(self.bottom_options) if self.bottom_options else random.choice(self.top_options)

    def choose_indices(self, hand):
        top_two = self.reroll_for_topsheet(hand, 2)
        if top_two: return top_two
        
        if hand.four_kind() and not hand.yatzy():
            return [0] if hand[0] != hand[1] else [4]
        
        top_one = self.reroll_for_topsheet(hand, 1)
        if top_one: return top_one

        indices_lower = [i for i, die in enumerate(hand) if die.value in [1,2,3]]
        
        indices_upper = [i for i in range(5) if random.random() < self.prob]

        return indices_lower if indices_lower else indices_upper




class AIGenFivePointTwo(AIGenFivePointOne):
    '''Prioritizes yatzy by rerolling to try to get 5-of-a-kind. 
        Then it prioritizes top-sheet by rerolling to try to get at least 3 of a number.
        Then bottom-sheet, then chooses a move randomly - first from bottom sheet, then from top. 
        Always rerolls. Chooses indicess by rerolling for top-sheet, then yatzy, then rerolling lower dice.'''
    def __init__(self, name, generation='5.2.1'):
        super().__init__(name, generation=generation)
        self.override_values = {'yatzy': 50, 'sixes': 18, 'fives': 15, 'fours': 12, 
                                'threes': 9, 'twos': 6, 'ones': 3, 
                                'large_straight': 20, 'small_straight': 15, 'full_house': 22,
                                'four_kind': 20, 'three_kind': 15, 
                                'two_pair': 18, 'chance': 25}

    def override_move(self, hand):
        for move in self.override_values:
            if getattr(hand, move)() >= self.override_values[move] and move in self.options:
                return move
        return False

    def override_reroll(self, hand):
        if 'yatzy' in self.options:
            if hand.yatzy() == 50:
                return 'yatzy'
            elif hand.four_kind():
                return False
            elif hand.three_kind():
                return False
        
        return self.override_move(hand)

    def choose_reroll(self, hand):
        return False if self.override_reroll(hand) else True

    def choose_move(self, hand):
        override = self.override_move(hand)
        if override: return override

        return random.choice(self.bottom_options) if self.bottom_options else random.choice(self.top_options)

    def choose_indices(self, hand):
        if hand.four_kind() and not hand.yatzy():
            return [0] if hand[0] != hand[1] else [4]

        top_two = self.reroll_for_topsheet(hand, 2)
        if top_two: return top_two
        
        top_one = self.reroll_for_topsheet(hand, 1)
        if top_one: return top_one

        indices_lower = [i for i, die in enumerate(hand) if die.value in [1,2,3]]
        
        indices_upper = [i for i in range(5) if random.random() < self.prob]

        return indices_lower if indices_lower else indices_upper



if __name__ == '__main__':
    pass
