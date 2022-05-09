import datetime
import random
import time
from numpy import average


from aigame import AIGame, AITest
from hand import YatzyHand
from leaderboard import Leaderboard
from ai_gen_7 import AIGenSevenPointOne, AIGenSevenPointTwo, AIGenSevenPointTwoPointOne, AIGenSevenPointZero



PLAYER = AIGenSevenPointTwoPointOne('karen')


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

class RLTrainer2(AIGame):
    
    def train(self, num):
        player = PLAYER
        self.players.append(player)
        player.read_q()
        player.load_new_hands()

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


class RLGameData(RLGame2):
    def __init__(self, gen=None):
        super().__init__(gen=gen)
        self.yatzy_hands = 0
        self.total_rerolls = 0


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
        

        end = datetime.datetime.now()
        print('Time elapsed: {}'.format(end - start))
        print("Game over! Now for the leaderboard...")


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
                    
        print('')
        print('')
        print('Gen {}'.format(self.gen))
        print('')
        '''
        for item in data:
            play = list(item.keys())[0]
            print(f"Total {play}: {item[play]} out of {num} ---- Average: {item['total'] / item[play]}")
        '''
        

        print('')
        print('Total rerolls: {}'.format(self.total_rerolls))
        #print('Total yatzy hands: {}'.format(self.yatzy_hands))

        print('')
        '''
        print('Total top-sheet bonuses: {} out of {}'.format(top_sheet_bonuses[0], num))
        print('Average top-sheet score: {}'.format(average(top_sheet_bonuses[1] / num)))
        '''
        print('')
        print('')


    def ai_turn(self, player):
        hand = YatzyHand()
        if hand.yatzy() == 50:
            self.yatzy_hands += 1 

        rerolls = 0
        while rerolls < 2:
            reroll = player.choose_action(hand, epsilon=False, q_table='reroll')


            if reroll == 'True':
                indices = player.choose_action(hand, epsilon=False, q_table='indices')
                hand = hand.reroll(indices)
                if hand.yatzy() == 50:
                    self.yatzy_hands += 1 
                rerolls += 1
                self.total_rerolls += 1
            
            else:
                break

        action = player.choose_action(hand, epsilon=False, q_table='moves')

        score = getattr(hand, action)()

        player.update_scoresheet(action, score)

if __name__ == "__main__":

    game = RLGameData(gen='7.2.1')
    game.play(1000)

