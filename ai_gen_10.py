
import torch
import itertools as it


from player import AIPlayer
from hand import YatzyHand
from deep_rl import create_state, create_action_value_dict, create_value_action_dict
from deep_sl import Model_1, Model_2
import re



class AIGenTenPointZero(AIPlayer):
    def __init__(self, name, generation='10.0'):
        super().__init__(name, generation=generation)
        self.model = Model_1()
        self.load()

        self.value_dict = self.create_value_action_dict()

    def turn(self):
        hand = YatzyHand()

        rerolls = 0
        while rerolls < 2:

            move = self.choose_move(hand, reroll=True)

            if move >= 15:
                rerolls += 1
                indices = self.get_indices(move)

                hand = hand.reroll(indices)
            else:
                break

        move = self.choose_move(hand, reroll=False)

        action = self.value_dict[move]

        score = getattr(hand, action)()

        self.update_scoresheet(action, score)
    

    def test_turn(self):
        hand = YatzyHand()
        

        rerolls = 0
        while rerolls < 2:
            print('')
            input('Hand: {}'.format(hand))
            print('')

            move = self.choose_move(hand, reroll=True)

            if move >= 15:
                rerolls += 1
                indices = self.get_indices(move)
                print('Rerolling {}'.format(indices))

                hand = hand.reroll(indices)
            else:
                break
        
        print('Final hand: {}'.format(hand))
        print('')

        move = self.choose_move(hand, reroll=False)

        

        action = self.value_dict[move]

        input('Move: {}'.format(action))
        print('')

        score = getattr(hand, action)()

        self.update_scoresheet(action, score)
        self.print_scoresheet()
    

    def get_indices(self, action):
        temp = re.findall(f'\d', self.value_dict[action])
        return [int(x) for x in temp]


    def load(self):
        self.model.load_state_dict(torch.load('sl_models/gen_{}.pt'.format(self.generation)))
        self.model.eval()
        
    def available_moves(self, reroll=False):
        final = []
        i = 0
        for key, value in self.scoresheet.items():
            if value == None:
                final.append(i)
            i += 1
        
        if reroll:
            for i in range(15, 46):
                final.append(i)
                i += 1
                
        return torch.tensor(final)

    def create_value_action_dict(self):    
        actions = {}

        counter = 0
        for action in self.scoresheet.keys():
            actions[counter] = action
            counter += 1


        rerolls = []
        for i in range(1, 6):   
            for combo in it.combinations([0, 1, 2, 3, 4], r=i):
                rerolls.append('reroll {}'.format(combo))

        for roll in rerolls:
            actions[counter] = roll
            counter += 1
        
        return actions
    
    def create_action_value_dict(self, actions):
        final = {}

        for key, value in actions.items():
            final[value] = key
        
        return final

    def choose_move(self, hand, reroll=False):
        state = create_state(self.scoresheet, hand)
        options = self.available_moves(reroll=reroll)

        with torch.no_grad():
            
            available_mask = torch.tensor(tuple(map(lambda x: x not in options, range(46))), dtype=torch.bool)
            
            results = self.model(state)
            results[available_mask] = 0
            print(torch.round(results, decimals=2))
            
            return torch.argmax(results).view(1).item()