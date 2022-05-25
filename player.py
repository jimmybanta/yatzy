import csv
import random
import datetime

from hand import YatzyHand

class Player:
    def __init__(self, name='karen', ai=False, generation='human'):
        self.name = name
        self.ai = ai
        self.generation = generation
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
        
    def print_scoresheet(self):
        for category, score in self.scoresheet.items():
            if score == None:
                print(f'{category}: ')
            else:
                print(f'{category}: {score}')

    def update_scoresheet(self, category, score):
        self.scoresheet[category] = score

    def clear_scoresheet(self):
        for key in self.scoresheet:
            self.scoresheet[key] = None

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



if __name__ == "__main__":

    player = Player('karen')
    
    print('')
    print('player.scoresheet: ')
    print('')
    print(player.scoresheet)
    print('')
