## Deep RL Models

import torch


from player import AIPlayer
from deep_rl import DQN, create_state, available_actions, create_action_dict
from hand import YatzyHand



class AIGenEightPointZero(AIPlayer):
    def __init__(self, name, generation='8.0.1'):
        super().__init__(name, generation=generation)
        self.name = name

        self.model = DQN()

        self.model.load_state_dict(torch.load('dqn_models/gen_8.0_1mruns.pt'))

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





if __name__ == "__main__":
    ai = AIGenEightPointZero('karen')
    hand = YatzyHand()
    print(hand)
    print(ai.choose_action(ai.scoresheet, hand, reroll=True))