
'''Run to play a game, and save your score to the leaderboard.'''

from hand import YatzyHand
from player import HumanPlayer
from game import Game
from leaderboard import Leaderboard



class HumanGame(Game):
    '''Allows a human to play a game by themself.'''
    def __init__(self):
        super().__init__()
        self.quit = False
        self.gen = 'human'

    def play(self):
        '''Runs the game.'''

        input('Welcome to Yatzy! Hit enter to play...  ')
        print('')
        name = input('What is your name?  ')
        print('')

        self.player = HumanPlayer(name)

        input("Ok {}! Let's begin! ".format(name))

        self.game_loop()

        self.final_scores.append(self.calculate_final_score())

        print("Game over! Now for the scores...")
        print('')
        
        self.print_final_scores(self.final_scores)

        self.run_leaderboard()

        print('')
        print('Thanks for playing!')
        print('')



if __name__ == '__main__':

    game = HumanGame()
    game.play()