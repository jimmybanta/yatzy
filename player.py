import csv
import random
import datetime

from hand import YatzyHand

class Player:
    '''A player. Has a name, generation, whether it's an ai or human, and a scoresheet.'''
    def __init__(self, name=False, ai=False, generation=False):
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
        '''Prints out the scoresheet.'''
        for category, score in self.scoresheet.items():
            if score == None:
                print(f'{category}: ')
            else:
                print(f'{category}: {score}')

    def update_scoresheet(self, category, score):
        '''Updates a given category in the scoresheet with a score.'''
        self.scoresheet[category] = score

    def reset_scoresheet(self):
        '''Resets the scoresheet.'''
        for key in self.scoresheet:
            self.scoresheet[key] = None

    def calculate_score(self):
        '''Calculates the current score of the scoresheet.'''
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


class HumanPlayer(Player):
    def __init__(self, name):
        super().__init__(name=name, ai=False, generation='human')

    def turn(self):
        '''An individual turn, for a human player.'''
        hand = YatzyHand()

        print('')
        print('Here is your hand: {}'.format(hand))
        print('')

        rerolls = 0
        while rerolls < 2:
            reroll = input('Would you like to reroll? y/n   ')
            if reroll.lower() == 'y':
                print('')
                values = [int(a) for a in input("List the indices of the dice you'd like to reroll:  ").split(',')]
                hand = hand.reroll(values)
                print('')
                print('Here is your new hand: {}'.format(hand))
                print('')
                rerolls += 1
            if reroll.lower() == 'n':
                print('')
                break
            if reroll == 'sheet':
                self.print_scoresheet()

        while True:
            category = input('What category would you like to use?  ')
            print('')

            if category == 'sheet':
                self.print_scoresheet()

            elif category in self.scoresheet and self.scoresheet[category] is None:
                self.scoresheet[category] = getattr(hand, category)()
                self.print_scoresheet()
                self.used.append(category)
                break
            
            elif category == 'quit':
                self.quit = True
                break

            else:
                print('Invalid category! Try again.')
                print('')



class AIPlayer(Player):
    '''An AI player; has a name and generation.'''
    def __init__(self, name, generation):
        super().__init__(name, ai=True, generation=generation)


    def turn(self):
        '''An individual turn, for an AI.'''

