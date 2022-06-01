import csv
import time
import random

from hand import YatzyHand
from player import Player
from leaderboard import Leaderboard, analyze


class Game:
    def __init__(self, player):
        self.used = []
        self.player = player
        self.test = False
        self.final_scores = []
        

    def game_loop(self):
        self.quit = False
        turns = 0
        while turns < 15:
            if self.quit == True:
                break
            self.player.turn()
            turns += 1


    def calculate_final_score(self):
        '''Returns a dictionary with the gen, name, and final score for self.player'''
        
        final = {}
        final['generation'] = self.player.generation
        final['name'] = self.player.name
        final['score'] = self.player.calculate_score()
        
        return final

    def print_final_scores(self):
        
        final = sorted(self.final_scores, key= lambda x:x['score'])
        
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

    def run_leaderboard(self):
        '''Runs the leaderboard'''
        leaderboard = Leaderboard(self.player.generation)
        leaderboard.run(self.final_scores)
    
    def run_analysis(self):
        '''Prints out analysis of the current gen.'''
        analyze(self.player.generation)


