import random

from ai_gen_2 import AI_gen_twopointzero


class AI_gen_threepointzero(AI_gen_twopointzero):
    def __init__(self, name, generation='3.0'):
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
        elif hand.chance() >= 24 and 'chance' in options:
            return True, 'chance'
        else:
            return False, 'bla'

class AI_gen_threepointone(AI_gen_threepointzero):
    def __init__(self, name, generation='3.1'):
        super().__init__(name, generation=generation)

    def choose_reroll(self):
        return True

class AI_gen_threepointtwo(AI_gen_threepointone):
    def __init__(self, name, generation='3.2'):
        super().__init__(name, generation=generation)
    
    def choose_nums(self,hand):
        indices_lower = []
        indices_upper = []
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







if __name__ == '__main__':
    pass