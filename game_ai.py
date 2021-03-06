'''AIGame runs a certain number of game simulations, and returns results and stats.
    AITest allows you to run one game and see how the AI plays.'''


## Still to do: finish making run_leaderboard and run_analysis, update AITest

import csv
import random
import datetime

from numpy import average


from ai_gen_4 import AI_gen_fourpointone, AI_gen_fourpointthree, AI_gen_fourpointzero, AI_gen_fourpointtwo
from ai_gen_5 import AI_gen_fivepointone, AI_gen_fivepointtwo, AI_gen_fivepointzero
from ai_gen_6 import ai_gen_sixpointzero


from hand import YatzyHand
from leaderboard import Leaderboard
from game import Game




class AIGame(Game):
    '''Allows for running 'games' games, for a given AI.'''
    def __init__(self, games, player):
        super().__init__()
        self.player = player
        self.games = games

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

        for i in range(self.games):
            self.player.name = self.get_name()
            self.player.reset_scoresheet()

            self.game_loop()

            self.final_scores.append(self.calculate_final_score())

            if i % 1000 == 0:
                print('Game {} complete'.format(i))
        
        self.run_leaderboard()
        self.run_analysis()
            

        
    
    
    def AIturn_without_override(self, player):
        hand = YatzyHand()

        rerolls = 0
        while rerolls < 2:
            if player.choose_reroll():
                rerolls += 1
                nums = player.choose_nums()
                hand = hand.reroll(nums)
            else:
                break

        play = player.choose_play(hand)

        score = getattr(hand, play)()

        player.update_scoresheet(play, score)



    def turn(self, player, override=False):
        hand = YatzyHand()
        play = None

        rerolls = 0
        while rerolls < 2:
            override = player.override(hand)

            if override[0]:
                play = override[1]
                break
            elif player.choose_reroll():
                rerolls += 1
                nums = player.choose_nums(hand)
                hand = hand.reroll(nums)
                play = player.choose_play(hand)
            else:
                play = player.choose_play(hand)
                break

        play = player.choose_play(hand)

        score = getattr(hand, play)()

        player.update_scoresheet(play, score)





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

    def play(self):
        input('Welcome to Yatzy! Are you ready?   ')

        name = 'karen'
        self.players.append(AI_gen_fivepointtwo(name))

        input("Ok {}! Let's begin! ".format(name))

        turns = 0
        while turns < 15:
            
            for player in self.players:
                print('')
                print("{}'s Turn!".format(player.name))

                self.AIturn_with_override(player)
            turns += 1

        final_scores = self.calculate_final_scores()
        print("Game over! Now for the score...")
        print('')
        self.print_final_scores(final_scores)
        print('')

        print("{}'s Scoresheet:".format(player.name))
        player.print_scoresheet()


        print('')

        print('Thanks for playing!')
        print('')

    def AIturn_with_override(self, player):
        hand = YatzyHand()
        play = None

        rerolls = 0
        while rerolls < 2:
            print('')
            input('Hand: {}'.format(hand))
            print('')

            override = player.override(hand)

            if override[0]:
                play = override[1]
                print('OVERRIDE')
                break
            else:
                if player.choose_reroll():
                    rerolls += 1
                    nums = player.choose_nums(hand)
                    print('')
                    input('Rerolling {}'.format(nums))
                    print('')
                    hand = hand.reroll(nums)
                    play = player.choose_play(hand)
                    print('Hand: {}'.format(hand))
                    print('')
                else:
                    print('Not rerolling')
                    print('')
                    play = player.choose_play(hand)
                    break


        input('Play decided: {}'.format(play))
        print('')

        score = getattr(hand, play)()

        player.update_scoresheet(play, score)
        player.print_scoresheet()

    def AIturn_without_override(self, player):
        hand = YatzyHand()
        play = None

        rerolls = 0
        while rerolls < 2:
            print('')
            input('Hand: {}'.format(hand))
            print('')

            if player.choose_reroll():
                rerolls += 1
                nums = player.choose_nums()
                print('')
                input('Rerolling indices {}'.format(nums))
                print('')
                hand = hand.reroll(nums)
                play = player.choose_play(hand)
            else:
                print('Not rerolling')
                print('')
                play = player.choose_play(hand)
                break
        input('Hand: {}'.format(hand))


        input('Play decided: {}'.format(play))
        print('')

        score = getattr(hand, play)()

        player.update_scoresheet(play, score)
        player.print_scoresheet()







if __name__ == "__main__":



    game = AIGame_data()


    game.play(1000)