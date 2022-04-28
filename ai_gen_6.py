## Reinforcement learning

from player import AIPlayer



class ai_gen_six(AIPlayer):
    def __init__(self, name, generation='6.0'):
        super().__init__(name, generation=generation)
        self.q = {}
    



if __name__ == '__main__':

    player = ai_gen_six('joe')
    print(player.name)
    print(player.q)
    print(player.generation)