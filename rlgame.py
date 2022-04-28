
from aigame import AIGame, AITest
from ai_gen_6 import ai_gen_sixpointzero
from hand import YatzyHand

## remember to reset the scoresheet after each game

## make it so you can add reroll to list of available actions



class RLTrainer(AIGame):
    pass



class RLTest(AITest):

    def play(self):
        name = 'karen'
        player = ai_gen_sixpointzero(name)

        input("Ok {}! Let's begin! ".format(name))

        turns = 0
        while turns < 15:
            


            
            
            for player in self.players:
                print('')
                print("{}'s Turn!".format(player.name))

                self.AIturn_with_override(player)
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
        hand = tuple(YatzyHand())
        play = None

        rerolls = 0
        while rerolls < 2:
            print('')
            input('Hand: {}'.format(hand))
            print('')

            action = player.choose_action(hand, epsilon=True, reroll=True)

            if action == 'reroll':
                rerolls += 1
                continue
            else:
                print('Not rerolling')
                print('')
                break
        


            if player.choose_reroll():
                rerolls += 1
                nums = player.choose_nums()
                print('')
                input('Rerolling indices {}'.format(nums))
                print('')
                hand = hand.reroll(nums)
                play = player.choose_play(hand)
            else:
                print('Not rerolling')
                print('')
                play = player.choose_play(hand)
                break
        input('Hand: {}'.format(hand))


        input('Play decided: {}'.format(play))
        print('')

        score = getattr(hand, play)()

        player.update_scoresheet(play, score)
        player.print_scoresheet()



test = RLTest('6.0')
print(test.ai_turn())