
import random

from ai_gen_3 import AIGenThreePointTwo
from ai_gen_4 import AI_gen_fourpointthree

## need to keep refactoring

class AIGenFivePointZero(AIGenThreePointTwo):
    def __init__(self, name, generation='5.0'):
        super().__init__(name, generation=generation)

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




    def choose_nums(self, hand):
        top = self.reroll_for_topsheet(hand, 2)

        return super().choose_nums(hand) if not top else top
        

    def choose_play(self, hand):
        options = []
        for column in self.scoresheet:
            if self.scoresheet[column] == None:
                options.append(column)

        if hand.yatzy() == 50 and 'yatzy' in options:
            return 'yatzy'
        elif hand.sixes() >= 18 and 'sixes' in options:
            return 'sixes'
        elif hand.fives() >= 15 and 'fives' in options: 
            return 'fives'
        elif hand.fours() >= 12 and 'fours' in options: 
            return 'fours'
        elif hand.threes() >= 9 and 'threes' in options: 
            return 'threes'
        elif hand.twos() >= 6 and 'twos' in options:
            return 'twos'
        elif hand.ones() >= 3 and 'ones' in options:
            return 'ones'

        elif hand.large_straight() == 20 and 'large_straight' in options:
            return 'large_straight'
        elif hand.small_straight() == 15 and 'small_straight' in options:
            return 'small_straight'
        elif hand.full_house() >= 22 and 'full_house' in options:
            return 'full_house'
        elif hand.four_kind() >= 20 and 'four_kind' in options:
            return 'four_kind'
        elif hand.three_kind() >= 15 and 'three_kind' in options:
            return 'three_kind'
        elif hand.two_pair() >= 18 and 'two_pair' in options:
            return 'two_pair'
        elif hand.chance() >= 25 and 'chance' in options:
            return 'chance'
        
        return random.choice(options)



class AIGenFivePointOne(AIGenFivePointZero):
    def __init__(self, name, generation='5.1'):
        super().__init__(name, generation=generation)
    
    def choose_play(self, hand):
        options_upper = []
        options_lower = []
        upper = ['ones', 'twos', 'threes', 'fours', 'fives', 'sixes']
        for column in self.scoresheet:
            if column in upper:
                if self.scoresheet[column] == None:
                    options_upper.append(column)
            else:
                if self.scoresheet[column] == None:
                    options_lower.append(column)

        if hand.yatzy() == 50 and 'yatzy' in options_lower:
            return 'yatzy'
        elif hand.sixes() >= 18 and 'sixes' in options_upper:
            return 'sixes'
        elif hand.fives() >= 15 and 'fives' in options_upper: 
            return 'fives'
        elif hand.fours() >= 12 and 'fours' in options_upper: 
            return 'fours'
        elif hand.threes() >= 9 and 'threes' in options_upper: 
            return 'threes'
        elif hand.twos() >= 6 and 'twos' in options_upper:
            return 'twos'
        elif hand.ones() >= 3 and 'ones' in options_upper:
            return 'ones'

        elif hand.large_straight() == 20 and 'large_straight' in options_lower:
            return 'large_straight'
        elif hand.small_straight() == 15 and 'small_straight' in options_lower:
            return 'small_straight'
        elif hand.full_house() >= 22 and 'full_house' in options_lower:
            return 'full_house'
        elif hand.four_kind() >= 20 and 'four_kind' in options_lower:
            return 'four_kind'
        elif hand.three_kind() >= 15 and 'three_kind' in options_lower:
            return 'three_kind'
        elif hand.two_pair() >= 18 and 'two_pair' in options_lower:
            return 'two_pair'
        elif hand.chance() >= 25 and 'chance' in options_lower:
            return 'chance'
        
        if options_lower:
            return random.choice(options_lower)
        else:
            return random.choice(options_upper)

    def choose_nums(self, hand):
        top_two = self.reroll_for_topsheet(hand, 2)
        if top_two:
            return top_two
        
        if hand.four_kind() and not hand.yatzy():
            return [0] if hand[0] != hand[1] else [4]
        
        top_one = self.reroll_for_topsheet(hand, 1)
        if top_one:
            return top_one

        indices_lower = [i for i, die in enumerate(hand) if die.value in [1,2,3]]
        
        indices_upper = [i for i in range(5) if random.random() < self.prob]

        return indices_lower if indices_lower else indices_upper

    def override(self, hand):
        options = []
        for column in self.scoresheet:
            if self.scoresheet[column] == None:
                options.append(column)

        if hand.yatzy() == 50 and 'yatzy' in options:
            return True, 'yatzy'
        elif hand.sixes() >= 18 and 'sixes' in options:
            return True, 'sixes'
        elif hand.fives() >= 15 and 'fives' in options: 
            return True, 'fives'
        elif hand.fours() >= 12 and 'fours' in options: 
            return True, 'fours'
        elif hand.threes() >= 9 and 'threes' in options: 
            return True, 'threes'
        elif hand.twos() >= 6 and 'twos' in options:
            return True, 'twos'
        elif hand.ones() >= 3 and 'ones' in options:
            return True, 'ones'

        elif hand.four_kind() and 'yatzy' in options:
            return False, 'bla'

        elif hand.large_straight() == 20 and 'large_straight' in options:
            return True, 'large_straight'
        elif hand.small_straight() == 15 and 'small_straight' in options:
            return True, 'small_straight'
        elif hand.full_house() >= 22 and 'full_house' in options:
            return True, 'full_house'
        elif hand.four_kind() >= 20 and 'four_kind' in options:
            return True, 'four_kind'
        elif hand.three_kind() >= 15 and 'three_kind' in options:
            return True, 'three_kind'
        elif hand.two_pair() >= 18 and 'two_pair' in options:
            return True, 'two_pair'
        elif hand.chance() >= 25 and 'chance' in options:
            return True, 'chance'
        
        else:
            return False, 'bla'


class AIGenFivePointTwo(AIGenFivePointZero):
    def __init__(self, name, generation='5.2'):
        super().__init__(name, generation=generation)

    def override(self, hand):
        options = []
        for column in self.scoresheet:
            if self.scoresheet[column] == None:
                options.append(column)

        if hand.yatzy() == 50 and 'yatzy' in options:
            return True, 'yatzy'
        elif hand.four_kind() and 'yatzy' in options:
            return False, 'bla'
        elif hand.three_kind() and 'yatzy' in options:
            return False, 'bla'

        elif hand.sixes() >= 18 and 'sixes' in options:
            return True, 'sixes'
        elif hand.fives() >= 15 and 'fives' in options: 
            return True, 'fives'
        elif hand.fours() >= 12 and 'fours' in options: 
            return True, 'fours'
        elif hand.threes() >= 9 and 'threes' in options: 
            return True, 'threes'
        elif hand.twos() >= 6 and 'twos' in options:
            return True, 'twos'
        elif hand.ones() >= 3 and 'ones' in options:
            return True, 'ones'

        

        elif hand.large_straight() == 20 and 'large_straight' in options:
            return True, 'large_straight'
        elif hand.small_straight() == 15 and 'small_straight' in options:
            return True, 'small_straight'
        elif hand.full_house() >= 22 and 'full_house' in options:
            return True, 'full_house'
        elif hand.four_kind() >= 20 and 'four_kind' in options:
            return True, 'four_kind'
        elif hand.three_kind() >= 15 and 'three_kind' in options:
            return True, 'three_kind'
        elif hand.two_pair() >= 18 and 'two_pair' in options:
            return True, 'two_pair'
        elif hand.chance() >= 25 and 'chance' in options:
            return True, 'chance'
        
        else:
            return False, 'bla'

    def choose_play(self, hand):
        options_upper = []
        options_lower = []
        upper = ['ones', 'twos', 'threes', 'fours', 'fives', 'sixes', 'yatzy']
        for column in self.scoresheet:
            if column in upper:
                if self.scoresheet[column] == None:
                    options_upper.append(column)
            else:
                if self.scoresheet[column] == None:
                    options_lower.append(column)

        if hand.yatzy() == 50 and 'yatzy' in options_upper:
            return 'yatzy'
        elif hand.sixes() >= 18 and 'sixes' in options_upper:
            return 'sixes'
        elif hand.fives() >= 15 and 'fives' in options_upper: 
            return 'fives'
        elif hand.fours() >= 12 and 'fours' in options_upper: 
            return 'fours'
        elif hand.threes() >= 9 and 'threes' in options_upper: 
            return 'threes'
        elif hand.twos() >= 6 and 'twos' in options_upper:
            return 'twos'
        elif hand.ones() >= 3 and 'ones' in options_upper:
            return 'ones'

        elif hand.large_straight() == 20 and 'large_straight' in options_lower:
            return 'large_straight'
        elif hand.small_straight() == 15 and 'small_straight' in options_lower:
            return 'small_straight'
        elif hand.full_house() >= 22 and 'full_house' in options_lower:
            return 'full_house'
        elif hand.four_kind() >= 20 and 'four_kind' in options_lower:
            return 'four_kind'
        elif hand.three_kind() >= 15 and 'three_kind' in options_lower:
            return 'three_kind'
        elif hand.two_pair() >= 18 and 'two_pair' in options_lower:
            return 'two_pair'
        elif hand.chance() >= 25 and 'chance' in options_lower:
            return 'chance'
        
        if options_lower:
            return random.choice(options_lower)
        else:
            return random.choice(options_upper)
        
    def choose_nums(self, hand):
        indices = []
        plays = ['sixes', 'fives', 'fours', 'threes', 'twos', 'ones']

        if hand.four_kind():
            if hand[0] != hand[1]:
                return [0]
            if hand[4] != hand[3]:
                return [4]

        for i, play in enumerate(plays):
            num = 6 - i
            if hand.count(num) >= 2 and self.scoresheet[play] == None:
                for i, die in enumerate(hand):
                    if die != num:
                        indices.append(i)
                break
        if indices:
            return indices
        
        
        
        for i, play in enumerate(plays):
            num = 6 - i
            if hand.count(num) >= 1 and self.scoresheet[play] == None:
                for i, die in enumerate(hand):
                    if die != num:
                        indices.append(i)
                break
        if indices:
            return indices

        for i,die in enumerate(hand):
            if die.value in [1,2,3]:
                indices.append(i)
        if indices:
            return indices
        else:
            for i in range(5):
                value = random.random()
                if value < .5:
                    indices.append(i)
            return indices


if __name__ == '__main__':
    pass
