import datetime
import random
import time


from aigame import AIGame, AITest
from ai_gen_6 import ai_gen_sixpointzero
from hand import YatzyHand

STANDARD_SCORESHEET = {
            'ones': None, 
            'twos': None, 
            'threes': None, 
            'fours': None, 
            'fives': None, 
            'sixes': None, 
            'one_pair': None, 
            'two_pair': None, 
            'three_kind': None, 
            'four_kind': None,
            'small_straight': None,
            'large_straight': None, 
            'full_house': None, 
            'chance': None, 
            'yatzy': None
            }

## remember to reset the scoresheet after each game

## make it so you can add reroll to list of available actions

class RLGame(AIGame):

    def play(self, num):

        input('Welcome to Yatzy! Are you ready?   ')
        start = datetime.datetime.now()

        self.make_name_lists()

        for _ in range(num):
            first_name = random.choice(self.first_names)
            last_name = random.choice(self.last_names)
            name = first_name + ' ' + last_name
            self.players.append(ai_gen_sixpointzero(name))

    
        turns = 0
        while turns < 15:
            for player in self.players:
                self.ai_turn(player)
            turns += 1
            print('Turn {} complete'.format(turns))

        final_scores = self.calculate_final_scores()
        end = datetime.datetime.now()
        print('Time elapsed: {}'.format(end - start))
        print("Game over! Now for the leaderboard...")

        self.print_final_scores(final_scores)


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
        name = 'karen'
        player = ai_gen_sixpointzero(name)
        self.players.append(player)

        input("Ok {}! Let's begin! ".format(name))

        start = time.perf_counter()
        for _ in range(num):
            player.clear_scoresheet()
        
            while None in player.scoresheet.values():
                self.ai_train_turn(player)
        

        player.write_q('test')
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
        name = 'karen'
        player = ai_gen_sixpointzero(name)
        self.players.append(player)
        player.read_q('sixpointzero')

        input("Ok {}! Let's begin! ".format(name))

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



    game = RLTest('6.0')
    game.play()
    