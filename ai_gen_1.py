import random

from player import AIPlayer

# 50% chance of choosing to reroll, 50% chance of rerolling any one die, random choice of play
class AI_gen_onepointzero(AIPlayer):
    def __init__(self, name, generation='1.0'):
        super().__init__(name, generation=generation)

    def choose_play(self):
        options = []
        for item in self.scoresheet:
            if self.scoresheet[item] == None:
                options.append(item)
        return random.choice(options)

    def choose_reroll(self):
        value = random.random()
        if value < .5:
            return True
        return False

    def choose_nums(self):
        indices = []
        for i in range(5):
            value = random.random()
            if value < .5:
                indices.append(i)

        return indices

# never rerolls, random choice of play
class AI_gen_onepointone(AI_gen_onepointzero):
    def __init__(self, name, generation='1.1'):
        super().__init__(name, generation=generation)

    def choose_reroll(self):
        return False

# always rerolls, random choice of play
class AI_gen_onepointtwo(AI_gen_onepointzero):
    def __init__(self, name, generation='1.2'):
        super().__init__(name, generation=generation)


    def choose_reroll(self):
        return True

    
if __name__ == '__main__':
    pass