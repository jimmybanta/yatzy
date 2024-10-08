

from ai_gen_8 import AIGenEightPointOne, AIGenEightPointTwo
from deeprlgame import DeepRLTest
from hand import YatzyHand
from leaderboard import Leaderboard
from rlgame import RLGame

import random

PLAYER = AIGenEightPointTwo('karen', 1)



class DeepRLGame3DQN(RLGame):
    def __init__(self, gen):
        super().__init__(gen=gen)

    def play(self, num):
        input('Welcome to Yatzy! Are you ready?   ')

        self.make_name_lists()

        player = PLAYER 
        player.load_dqn()

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



class DeepRLTest3DQN(DeepRLTest):
    def __init__(self):
        super().__init__(gen='Test')
        self.player = PLAYER
        self.player.load_dqn()

    def ai_turn(self, player):
        hand = YatzyHand()

        print('')
        input('Hand: {}'.format(hand))
        print('')

        rerolls = 0
        while rerolls < 2:
            
            reroll = player.choose_reroll(hand, test=True)

            print('reroll: ', reroll)

            if reroll == 'True':
                rerolls += 1
                indices = player.choose_indices(hand, test=True)

                print('')
                input('Rerolling indices {}'.format(indices))
                print('')

                hand = hand.reroll(indices)
            else:
                print('Not rerolling')
                print('')
                break

        move = player.choose_move(hand, test=True)

        input('Hand: {}'.format(hand))
        input('Action decided: {}'.format(move))
        print('')

        score = getattr(hand, move)()

        player.update_scoresheet(move, score)





if __name__ == '__main__':
    game = DeepRLGame3DQN('8.2.1')
    game.play(1000)