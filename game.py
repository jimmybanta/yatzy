import csv
import time
import random

from hand import YatzyHand
from player import Player, AIPlayer
from leaderboard import Leaderboard


class Game:
    def __init__(self):
        self.used = []
        self.players = []

    def human_turn(self, player):
        hand = YatzyHand()

        count = 0
        print('')
        print('Here is your hand: {}'.format(hand))
        print('')
        while count < 2:
            reroll = input('Would you like to reroll? y/n   ')
            if reroll.lower() == 'y':
                print('')
                values = [int(a) for a in input("List the indexes of the dice you'd like to reroll:  ").split(',')]
                hand = hand.reroll(values)
                print('')
                print('Here is your new hand: {}'.format(hand))
                print('')
                count += 1
            if reroll.lower() == 'n':
                print('')
                break
            if reroll == 'sheet':
                player.print_scoresheet()

        while True:
            category = input('What category would you like to use?  ')
            print('')

            if category == 'sheet':
                player.print_scoresheet()

            elif category in player.scoresheet and category not in self.used:
                player.scoresheet[category] = getattr(hand, category)()
                player.print_scoresheet()
                self.used.append(category)
                break
            
            elif category == 'quit':
                self.quit = True
                break

            else:
                print('Invalid category! Try again.')

    def AIturn(self, player):
        hand = YatzyHand()

        print('')
        print('Hand: {}'.format(hand))
        print('')

        rerolls = 0
        while rerolls < 2:
            if player.will_reroll():
                rerolls += 1
                nums = player.AI_decide_nums(hand)
                print('')
                print('Rerolling {}'.format(nums))
                print('')
                time.sleep(1)
                hand.reroll(nums)
                print('Rerolling... ')
                print('')
                time.sleep(1)
                print('New Hand: {}'.format(hand))
                time.sleep(2)
            else:
                break

        for _ in range(3):
            time.sleep(.5)
            print('thinking...')
            print('')

        play = player.score(hand)
        print('Play decided: {}'.format(play))
        print('')

        score = getattr(hand, play)()

        player.update_scoresheet(play, score)
        player.print_scoresheet()

        time.sleep(.5)

    def calculate_final_scores(self):
        final_scores = []

        for player in self.players:
            final_score = {}
            final_score['generation'] = player.generation
            final_score['name'] = player.name
            final_score['score'] = player.calculate_score()
            final_scores.append(final_score)
        
        return final_scores

    def print_final_scores(self, final_scores):
        
        final = sorted(final_scores, key= lambda x:x['score'])
        
        for i, item in enumerate(final):
            if i == len(final) - 1:
                print('And the winner is... ')
                print('')
                time.sleep(1)
                print('{} with {} points! Congrats!'.format(item['name'], item['score']))
                print('')

            else:
                print('{}: {} points'.format(item['name'], item['score']))
                time.sleep(1)
                print('')


class SinglePlayerGame(Game):
    def play(self):
        input('Welcome to Yatzy! Are you ready?   ')
        name = input('What is your name?  ')

        player = Player(name)

        self.players.append(player)

        input("Ok {}! Let's begin! ".format(name))
        self.quit = False

        turns = 0
        while turns < 15:
            if self.quit == True:
                break
            self.human_turn(player)    
            turns += 1

        final_score = self.calculate_final_scores()
        print("Game over! Now here is your score...")
        print('')
        time.sleep(1)
        
        self.print_final_scores(final_score)

        
        leaderboard = Leaderboard()
        leaderboard.load()
        leaderboard.update(final_score)
        leaderboard.print()
        leaderboard.write()

        print('')

        print('Thanks for playing!')
        print('')


if __name__ == '__main__':

    game = SinglePlayerGame()

    game.play()