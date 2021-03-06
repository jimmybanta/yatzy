## Deep RL Models

import torch


from player import AIPlayer
from deep_rl import DQN, create_state, available_actions, create_action_dict
from hand import YatzyHand
from ai_gen_7 import AIGenSevenPointZero

from os.path import exists

class AIGenEightPointZero(AIPlayer):
    def __init__(self, name, generation='8.0.1'):
        super().__init__(name, generation=generation)
        self.name = name

        self.model = DQN(46)
        self.model.load_state_dict(torch.load('dqn_models/8.0/gen_8.0_1mruns.pt'))
        self.model.eval()

        self.action_dict = create_action_dict(self)

    
    def choose_action(self, scoresheet, hand, reroll=False):

        state = create_state(scoresheet, hand)
        options = available_actions(self.scoresheet, reroll=reroll)

        with torch.no_grad():
            results = self.model(state)
            for i in range(46):
                if options[i] == False:
                    results[i] = 0
            return self.action_dict[torch.argmax(results).view(1).item()]



    def copy(self):
        copy = AIGenEightPointZero(self.name)
        copy.scoresheet = self.scoresheet.copy()

        return copy



class AIGenEightPointOne(AIPlayer):
    def __init__(self, name, number, generation='8.1.1'):
        super().__init__(name, generation=generation)
        self.name = name
        self.number = number

        self.moves_dqn = DQN(15)
        self.reroll_dqn = DQN(2)
        self.indices_dqn = DQN(31)
        self.moves_dqn.eval()
        self.reroll_dqn.eval()
        self.indices_dqn.eval()

        self.moves_dict, self.reroll_dict, self.indices_dict = create_action_dicts()

        self.path = f'dqn_models/8.1test3/{self.number}/'

    
    def load_dqn(self):
        if exists(f'{self.path}moves.pt'):
            #print(self.path)
            self.moves_dqn.load_state_dict(torch.load(f'{self.path}moves.pt'))
            self.reroll_dqn.load_state_dict(torch.load(f'{self.path}reroll.pt'))
            self.indices_dqn.load_state_dict(torch.load(f'{self.path}indices.pt'))
        else:
            print("MODELS DON'T EXIST!")



    def choose_move(self, hand, test=False):
        state = create_state(self.scoresheet, hand)
        if test:
            print(state)
        options = available_moves(self.scoresheet)

        if test:
            print('')
            print(self.scoresheet)
            print('')

        with torch.no_grad():
            results = self.moves_dqn(state)
            if test:
                self.print_moves_results(results)
                print('')
            for i in range(15):
                if options[i] == False:
                    results[i] = 0
            return self.moves_dict[torch.argmax(results).view(1).item()]


    def choose_reroll(self, hand, test=False):
        state = create_state(self.scoresheet, hand)

        with torch.no_grad():
            results = self.reroll_dqn(state)
            if test:
                print(results)
            return self.reroll_dict[torch.argmax(results).view(1).item()]


    def choose_indices(self, hand, test=False):
        state = create_state(self.scoresheet, hand)

        with torch.no_grad():
            results = self.indices_dqn(state)
            if test:
                print(results)
            return self.indices_dict[torch.argmax(results).view(1).item()]


    def copy(self):
        copy = AIGenEightPointOne(self.name, self.number)
        copy.scoresheet = self.scoresheet.copy()

        return copy

    def print_moves_results(self, results):
        d = {}
        for i, key in enumerate(self.scoresheet.keys()):
            d[key] = results[i].item()
        
        print(sorted(d.items(), key=lambda x:x[1], reverse=True))


class AIGenEightPointTwo(AIGenEightPointOne):
    def __init__(self, name, number, generation='8.2.1'):
        super().__init__(name, number, generation=generation)

        self.path = f'dqn_models/8.2test0/{self.number}/'


    def copy(self):
        copy = AIGenEightPointTwo(self.name, self.number)
        copy.scoresheet = self.scoresheet.copy()

        return copy





def create_action_dicts():
    moves = {}
    reroll = {}
    indices = {}

    player = AIGenSevenPointZero('karen')

    for i, item in enumerate(player.moves):
        moves[i] = item

    for i, item in enumerate(player.reroll):
        reroll[i] = item
    
    for i, item in enumerate(player.indices):
        indices[i] = item

    return moves, reroll, indices


def available_moves(scoresheet):
    available = {}
    for i, (key, value) in enumerate(scoresheet.items()):
        if value is not None:
            available[i] = False
        else:
            available[i] = True
    return available





if __name__ == "__main__":
    ai = AIGenEightPointZero('karen')
    hand = YatzyHand()
    print(hand)
    print(ai.choose_action(ai.scoresheet, hand, reroll=True))