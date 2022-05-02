import datetime
import random
import time


from aigame import AIGame, AITest
from hand import YatzyHand
from leaderboard import Leaderboard
from ai_gen_7 import AIGenSevenPointZero



PLAYER = AIGenSevenPointZero('karen')


class RLGame2(AIGame):
    def __init__(self, gen):
        super().__init__(gen=gen)


    def play(self, num):
        input('Welcome to Yatzy! Are you ready?   ')
        start = datetime.datetime.now()

        self.make_name_lists()

        player = PLAYER 
        player.read_q()

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
        end = datetime.datetime.now()
        print('Time elapsed: {}'.format(end - start))
        print("Game over! Now for the leaderboard...")

        leaderboard = Leaderboard(self.gen)
        leaderboard.run(final_scores)
        print('')
        print('')


    def ai_turn(self, player):
        hand = YatzyHand()

        rerolls = 0
        while rerolls < 2:
            reroll = player.choose_action(hand, epsilon=False, q_table='reroll')

            if reroll == 'True':
                indices = player.choose_action(hand, epsilon=False, q_table='indices')
                hand = hand.reroll(indices)
                rerolls += 1
            
            else:
                break

        action = player.choose_action(hand, epsilon=False, q_table='moves')

        score = getattr(hand, action)()

        player.update_scoresheet(action, score)


    def print_final_scores(self, final_scores):
        
        final = sorted(final_scores, key= lambda x:x['score'])
        
        for i, item in enumerate(final):
            if i == len(final) - 1:
                print('And the winner is... ')
                print('')
                print('{} with {} points! Congrats!'.format(item['name'], item['score']))
                print('')

            else:
                print('{}: {} points'.format(item['name'], item['score']))
                print('')

class RLTrainer(AIGame):
    
    def train(self, num):
        player = PLAYER
        self.players.append(player)

        input("Ok {}! Let's begin! ".format(player.name))

        start = time.perf_counter()

        for i in range(num):
            player.clear_scoresheet()
        
            while None in player.scoresheet.values():
                self.ai_train_turn(player)
            
            if i % 1000 == 0:
                print('Finished game {}'.format(i))
                player.write_q()
        

        player.write_q()
        end = time.perf_counter()
        print('took {} seconds for {} runs'.format(end - start, num))
        

    def ai_train_turn(self, player):
        rerolls = 0

        hand = YatzyHand()
        old_hand = hand.copy()
        new_hand = []


        
        while rerolls < 2:
            action = player.choose_action(hand, epsilon=True, q_table='reroll')
            if action == 'True':
                player.update_reroll(hand, action)

                indices = player.choose_action(hand, epsilon=True, q_table='indices')
                hand = hand.reroll(indices)
                new_hand = hand.copy()
                rerolls += 1
                
                player.update_indices(old_hand, indices, new_hand)

            else:
                player.update_reroll(hand, action)
                break

            

        action = player.choose_action(hand, epsilon=True, q_table='moves')
        score = getattr(hand, action)()

        score /= player.divisors[action]

        player.update_moves(hand, action, score)
        player.update_scoresheet(action, score)


class RLTest2(AITest):

    def play(self):
        player = PLAYER
        self.players.append(player)
        player.read_q()

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
        action = None

        rerolls = 0
        while rerolls < 2:
            reroll = player.choose_action(hand, epsilon=False, q_table='reroll')

            if reroll == 'True':
                print('')
                input('Hand: {}'.format(hand))
                print('')

                
                indices = player.choose_action(hand, epsilon=False, q_table='indices')
                print('Rerolling {}...'.format(indices))
                hand = hand.reroll(indices)
                rerolls += 1
            
            else:
                break

        action = player.choose_action(hand, epsilon=False, q_table='moves')

        print('')
        print('Hand: {}'.format(hand))
        input('Action decided: {}'.format(action))
        print('')

        score = getattr(hand, action)()

        player.update_scoresheet(action, score)
        player.print_scoresheet()



if __name__ == "__main__":

    game = RLGame2("7.0")
    game.play(10000)

