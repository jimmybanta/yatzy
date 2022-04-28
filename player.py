import csv
import random
import datetime

from hand import YatzyHand

class Player:
    def __init__(self, name, ai=False, generation='human'):
        self.name = name
        self.ai = ai
        self.scoresheet = {
            'ones': None, 
            'twos': None, 
            'threes': None, 
            'fours': None, 
            'fives': None, 
            'sixes': None, 
            'one_pair': None, 
            'two_pair': None, 
            'three_kind': None, 
            'four_kind': None,
            'small_straight': None,
            'large_straight': None, 
            'full_house': None, 
            'chance': None, 
            'yatzy': None
            }
        self.generation = generation
        
    def print_scoresheet(self):
        for category, score in self.scoresheet.items():
            if score == None:
                print(f'{category}: ')
            else:
                print(f'{category}: {score}')

    def update_scoresheet(self, category, score):
        self.scoresheet[category] = score

    def calculate_score(self):
        score = 0
        top = ['ones', 'twos', 'threes', 'fours', 'fives', 'sixes']
        bottom = ['one_pair', 'two_pair', 'three_kind', 'four_kind','small_straight','large_straight', 'full_house', 'chance', 'yatzy']
        for category in top:
            if self.scoresheet[category] != None:
                score += self.scoresheet[category]
        if score >= 63:
            score += 50
        for category in bottom:
            if self.scoresheet[category] != None:
                score += self.scoresheet[category]
        return score

class AIPlayer(Player):
    def __init__(self, name, generation):
        super().__init__(name, ai=True, generation=generation)




# second gen: priority to override a call if it's a good hand, 75% chance of reroll, random dice choices
class AI_second_gen(AIPlayer):
    def __init__(self):
        super().__init__()
        self.gen = '2.3'

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

    def score(self, hand):
        options = []
        for column in self.scoresheet:
            if self.scoresheet[column] == None:
                options.append(column)

        scores = {}
        plays = []
        for option in options:
            scores[option] = getattr(hand, option)()
        m = max(scores.values())
        for play, score in scores.items():
            if score == m:
                plays.append(play)
        if 'chance' in plays and hand.chance() < 20 and len(plays) > 1:
            plays.remove('chance')
        return random.choice(plays)
        
    def will_reroll(self):
        prob = .75
        if random.random() < prob:
            return True
        else:
            return False

    def AI_decide_nums(self, hand):
        nums = []
        for die in hand:
            if random.random() < .4:
                nums.append(die.value)
        return nums


class AI_third_gen(AIPlayer):
    def __init__(self):
        super().__init__()
        self.gen = 'third'

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
        elif hand.four_kind() >= 12 and 'four_kind' in options:
            return True, 'four_kind'
        elif hand.three_kind() >= 12 and 'three_kind' in options:
            return True, 'three_kind'
        elif hand.two_pair() >= 20 and 'two_pair' in options:
            return True, 'two_pair'
        elif hand.chance() >= 23 and 'chance' in options:
            return True, 'chance'
        else:
            return False, 'bla'


    def score(self, hand):
        options = []
        for column in self.scoresheet:
            if self.scoresheet[column] == None:
                options.append(column)

        scores = {}
        plays = []
        for option in options:
            scores[option] = getattr(hand, option)()
        m = max(scores.values())
        for play, score in scores.items():
            if score == m:
                plays.append(play)
        if 'chance' in plays and hand.chance() < 20 and len(plays) > 1:
            plays.remove('chance')
        return random.choice(plays)
        