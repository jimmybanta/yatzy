
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

            action = player.choose_action(hand, epsilon=True, reroll=True)

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
            action = player.choose_action(hand, epsilon=True, reroll=False)


        input('Action decided: {}'.format(action))
        print('')

        score = getattr(hand, action)()

        player.update_scoresheet(action, score)
        player.print_scoresheet()



if __name__ == "__main__":



    test = RLTest('6.0')
    test.play()
