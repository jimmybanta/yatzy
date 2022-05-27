import datetime
import random
import time


from game_ai import AIGame, AITest
from ai_gen_6 import ai_gen_sixpointone, ai_gen_sixpointzero, ai_gen_sixpointtwo, ai_gen_sixpointthree, ai_gen_sixpointfour
from hand import YatzyHand
from leaderboard import Leaderboard


PLAYER = ai_gen_sixpointfour('karen')
Q_TABLE = 'sixpointfour'


class RLGame(AIGame):
    def __init__(self, gen):
        super().__init__(gen=gen)



    def play(self, num):
        input('Welcome to Yatzy! Are you ready?   ')
        start = datetime.datetime.now()

        self.make_name_lists()

        player = PLAYER 
        player.read_q(Q_TABLE)

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
        action = None

        rerolls = 0
        while rerolls < 2:
            
            action = player.choose_action(hand, epsilon=True, reroll=True)

            if 'reroll' in action:
                rerolls += 1
                indices = [int(k) for k in action if ord(k) < 53 and ord(k) > 47]

                hand = hand.reroll(indices)
            else:
                break

        if 'reroll' in action:
            action = player.choose_action(hand, epsilon=True, reroll=False)

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
                player.write_q(Q_TABLE)
        

        player.write_q(Q_TABLE)
        end = time.perf_counter()
        print('took {} seconds for {} runs'.format(end - start, num))
        

    def ai_train_turn(self, player):
        rerolls = 0

        hand = YatzyHand()
        old_hand = []
        new_hand = []


        while rerolls < 3:
            if rerolls < 2:
                action = player.choose_action(hand, epsilon=True, reroll=True)
            else:
                action = player.choose_action(hand, epsilon=True, reroll=False)

            if 'reroll' in action:
                old_hand = hand.copy()
                rerolls += 1
                indices = [int(k) for k in action if ord(k) < 53 and ord(k) > 47]

                hand = hand.reroll(indices)
                new_hand = hand.copy()
                
                player.update(old_hand, action, 0, new_hand=new_hand)

            else:
                score = getattr(hand, action)()
                player.update(hand, action, score)
                player.update_scoresheet(action, score)
                break



class RLTest(AITest):

    def play(self):
        player = PLAYER
        self.players.append(player)
        player.read_q(Q_TABLE)

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
            print('')
            input('Hand: {}'.format(hand))
            print('')

            action = player.choose_action(hand, epsilon=False, reroll=True)

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
            action = player.choose_action(hand, epsilon=False, reroll=False)

        input('Hand: {}'.format(hand))
        input('Action decided: {}'.format(action))
        print('')

        score = getattr(hand, action)()

        player.update_scoresheet(action, score)
        player.print_scoresheet()




if __name__ == "__main__":


    game = RLGame('6.4')
    game.play(10000)
