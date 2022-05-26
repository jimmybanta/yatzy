
import random
import pdb

from ai_gen_8 import AIGenEightPointZero
from rlgame import RLGame, RLTest
from hand import YatzyHand
from leaderboard import Leaderboard


PLAYER = AIGenEightPointZero('karen')



class DeepRLGame(RLGame):
    def __init__(self, gen):
        super().__init__(gen=gen)
    

    def play(self, num):
        input('Welcome to Yatzy! Are you ready?   ')

        self.make_name_lists()

        player = PLAYER 

        for i in range(num):
            player.clear_scoresheet()
            first_name = random.choice(self.first_names)
            last_name = random.choice(self.last_names)
            name = first_name + ' ' + last_name
            player.name = name

            turns = 0
            while turns < 15:
                self.ai_turn(player)
                turns += 1
            
            new_player = player.copy()
            self.players.append(new_player)
            if i % 1000 == 0:
                print('Game {} complete'.format(i))
        

        final_scores = self.calculate_final_scores()
        print("Game over! Now for the leaderboard...")

        leaderboard = Leaderboard(self.gen)
        leaderboard.run(final_scores)
        print('')
        print('')


    def ai_turn(self, player):
        hand = YatzyHand()

        rerolls = 0
        while rerolls < 2:
            
            action = player.choose_action(player.scoresheet, hand, reroll=True)

            if 'reroll' in action:
                rerolls += 1
                indices = [int(k) for k in action if ord(k) < 53 and ord(k) > 47]

                hand = hand.reroll(indices)
            else:
                break

        if 'reroll' in action:
            action = player.choose_action(player.scoresheet, hand, reroll=False)

        score = getattr(hand, action)()

        player.update_scoresheet(action, score)





class DeepRLTest(RLTest):
    def __init__(self, gen='Test'):
        super().__init__(gen='Test')
        self.player = PLAYER

    def play(self):
        player = self.player
        self.players.append(player)

        input("Ok {}! Let's begin! ".format(player.name))

        turns = 0
        while turns < 15:
            self.ai_turn(player)
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
    

    def ai_turn(self, player):
        hand = YatzyHand()

        rerolls = 0

        while rerolls < 2:
            print('')
            input('Hand: {}'.format(hand))
            print('')

            action = player.choose_action(player.scoresheet, hand, reroll=True)

            print('action: ', action)

            if 'reroll' in action:
                rerolls += 1
                indices = [int(k) for k in action if ord(k) < 53 and ord(k) > 47]

                print('')
                input('Rerolling indices {}'.format(indices))
                print('')
                hand = hand.reroll(indices)
            else:
                print('Not rerolling')
                print('')
                break

        if 'reroll' in action:
            action = player.choose_action(player.scoresheet, hand, reroll=False)

        input('Hand: {}'.format(hand))
        input('Action decided: {}'.format(action))
        print('')

        score = getattr(hand, action)()

        player.update_scoresheet(action, score)
        player.print_scoresheet()



if __name__ == "__main__":


    game = DeepRLGame('8.0.1')
    game.play(10000)