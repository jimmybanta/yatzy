import random

from ai_gen_3 import AI_gen_threepointtwo


class AI_gen_fourpointzero(AI_gen_threepointtwo):
    def __init__(self, name, generation='4.0'):
        super().__init__(name, generation=generation)

    def override(self, hand):
        options = []
        for column in self.scoresheet:
            if self.scoresheet[column] == None:
                options.append(column)

        if hand.yatzy() == 50 and 'yatzy' in options:
            return True, 'yatzy'
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
        else:
            return False, 'bla'

class AI_gen_fourpointone(AI_gen_threepointtwo):
    def __init__(self, name, generation='4.1'):
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
        else:
            return False, 'bla'


    def choose_nums(self,hand):
        indices_lower = []
        indices_upper = []
        if hand.four_kind():
            if hand[0] != hand[1]:
                return [0]
            if hand[4] != hand[3]:
                return [4]
        for i,die in enumerate(hand):
            if die.value in [1,2,3]:
                indices_lower.append(i)
        if indices_lower:
            return indices_lower
        else:
            for i in range(5):
                value = random.random()
                if value < .5:
                    indices_upper.append(i)
            return indices_upper

class AI_gen_fourpointtwo(AI_gen_fourpointone):
    def __init__(self, name, generation='4.2'):
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

    def choose_nums(self,hand):
        indices = []
        if hand.four_kind():
            if hand[0] != hand[1]:
                return [0]
            if hand[4] != hand[3]:
                return [4]
        for i in range(5):
            value = random.random()
            if value < .5:
                indices.append(i)
        return indices



class AI_gen_fourpointthree(AI_gen_threepointtwo):
    def __init__(self, name, generation='4.3'):
        super().__init__(name, generation=generation)
    
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

    def choose_nums(self,hand):
        indices = []
        if hand.four_kind():
            if hand[0] != hand[1]:
                return [0]
            if hand[4] != hand[3]:
                return [4]
        
        for i in range(5):
            value = random.random()
            if value < .5:
                indices.append(i)
        return indices