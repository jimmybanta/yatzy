

from ai_gen_8 import AIGenEightPointOne
from hand import YatzyHand
from leaderboard import Leaderboard
from rlgame import RLGame

import random

PLAYER = AIGenEightPointOne('karen')



class DeepRLGame3DQN(RLGame):
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
            
            reroll = player.choose_reroll(hand)

            if reroll == 'True':
                rerolls += 1
                indices = player.choose_indices(hand)

                hand = hand.reroll(indices)
            else:
                break


        move = player.choose_move(hand)

        score = getattr(hand, move)()

        player.update_scoresheet(move, score)

    

    def evaluate(self, num):

        final_scores = []

        player = PLAYER 

        for i in range(num):
            player.clear_scoresheet()

            turns = 0
            while turns < 15:
                self.ai_turn(player)
                turns += 1
            final_scores.append(player.calculate_score())
        
        return final_scores


if __name__ == '__main__':
    game = DeepRLGame3DQN('8.1')
    game.play(10000)