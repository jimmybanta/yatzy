'''AIGame runs a certain number of game simulations, and returns results and stats.
    AITest allows you to run one game and see how the AI plays.'''

import csv
import random
import datetime

from numpy import average


from hand import YatzyHand
from leaderboard import Leaderboard
from game import Game

from ai_gen_5 import AIGenFivePointTwo




class AIGame(Game):
    '''Allows for running 'num_games' games, for a given AI.'''
    def __init__(self, num_games, player):
        super().__init__(player)
        self.player = player
        self.num_games = num_games

        self.first_names = []
        self.last_names = []


    def load_names(self):
        '''Loads the names into the given name lists.'''
        with open('names.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.first_names.append(row['first_name'])
                self.last_names.append(row['last_name'])


    def get_name(self):
        '''Returns a random name.'''
        first_name = random.choice(self.first_names)
        last_name = random.choice(self.last_names)
        return first_name + last_name


    def play(self):

        self.load_names()

        for i in range(self.num_games):
            self.player.name = self.get_name()
            self.player.reset_scoresheet()

            self.game_loop()

            self.final_scores.append(self.calculate_final_score())

            if i % 1000 == 0:
                print('Game {} complete'.format(i))
        
        self.run_leaderboard()
        self.run_analysis()
            

class AIGame_data(AIGame):
    def __init__(self):
        super().__init__(gen='5.2')
        self.yatzy_hands = 0
        self.total_rerolls = 0

    def play(self, num):
        input('Welcome to Yatzy! Are you ready?   ')
        start = datetime.datetime.now()

        self.make_name_lists()

        for _ in range(num):
            first_name = random.choice(self.first_names)
            last_name = random.choice(self.last_names)
            name = first_name + ' ' + last_name
            self.players.append(AI_gen_fivepointtwo(name))

    
        turns = 0
        while turns < 15:
            for player in self.players:
                self.AIturn_with_override(player)
            turns += 1
            print('Turn {} complete'.format(turns))

        end = datetime.datetime.now()
        print('Time elapsed: {}'.format(end - start))
        print("Game over! Now for the leaderboard...")

        print('')
        print('')
        data = [
            {'ones': 0, 'total': 0},
            {'twos': 0, 'total': 0},
            {'threes': 0, 'total': 0},
            {'fours': 0, 'total': 0},
            {'fives': 0, 'total': 0},
            {'sixes': 0, 'total': 0},
            {'one_pair': 0, 'total': 0},
            {'two_pair': 0, 'total': 0},
            {'three_kind': 0, 'total': 0},
            {'four_kind': 0, 'total': 0},
            {'small_straight': 0, 'total': 0},
            {'large_straight': 0, 'total': 0},
            {'full_house': 0, 'total': 0},
            {'chance': 0, 'total': 0},
            {'yatzy': 0, 'total': 0}
        ]
        top_sheet_bonuses = [0, 0]

        
        for player in self.players:
            sum = player.scoresheet['ones'] + player.scoresheet['twos'] + player.scoresheet['threes'] + player.scoresheet['fours'] + player.scoresheet['fives'] + player.scoresheet['sixes']
            for i, item in enumerate(player.scoresheet.items()):
                if item[1] != 0:
                    data[i][item[0]] += 1
                    data[i]['total'] += item[1]
            if sum >= 63:
                top_sheet_bonuses[0] += 1
            top_sheet_bonuses[1] += sum
                    

        print('Gen {}'.format(self.gen))
        print('')
        '''
        for item in data:
            play = list(item.keys())[0]
            print(f"Total {play}: {item[play]} out of {num} ---- Average: {item['total'] / item[play]}")
        '''

        print('')
        print('Total rerolls: {}'.format(self.total_rerolls))
        print('Total yatzy hands: {}'.format(self.yatzy_hands))
        print('')
        '''
        print('Total top-sheet bonuses: {} out of {}'.format(top_sheet_bonuses[0], num))
        print('Average top-sheet score: {}'.format(average(top_sheet_bonuses[1] / num)))
        '''
        print('')
        print('')
        

    def AIturn_with_override(self, player):
        hand = YatzyHand()
        if hand.yatzy() == 50:
            self.yatzy_hands += 1
        play = None

        rerolls = 0
        while rerolls < 2:
            override = player.override(hand)

            if override[0]:
                play = override[1]
                break
            elif player.choose_reroll():
                rerolls += 1
                self.total_rerolls += 1
                nums = player.choose_nums(hand)
                hand = hand.reroll(nums)
                if hand.yatzy() == 50:
                    self.yatzy_hands += 1
                play = player.choose_play(hand)
            else:
                play = player.choose_play(hand)
                break

        play = player.choose_play(hand)

        score = getattr(hand, play)()

        player.update_scoresheet(play, score)


class AITest(AIGame):
    def __init__(self, player):
        self.player = player
        self.final_scores = []

    def play(self):
        input('Welcome to Yatzy! Are you ready?   ')

        input("Ok {}! Let's begin! ".format(self.player.name))

        turns = 0
        while turns < 15:
            
            self.player.test_turn()
            turns += 1

        self.final_scores.append(self.calculate_final_score())
        print("Game over! Now for the score...")
        print('')
        self.print_final_scores()
        print('')

        print("{}'s Scoresheet:".format(self.player.name))
        self.player.print_scoresheet()


        print('')

        print('Thanks for playing!')
        print('')







if __name__ == "__main__":



    game = AIGame(100, AIGenFivePointTwo('karen'))

    game.play()