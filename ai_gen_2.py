import random


from player import AIPlayer


# first gen: 50% probability of reroll, 50% probability to reroll each die, choose the max score play for each turn
class AI_gen_twopointzero(AIPlayer):
    def __init__(self, name, generation='2.0'):
        super().__init__(name, generation=generation)
        
    def choose_play(self, hand):
        scores = {}
        plays = []
        for column in self.scoresheet:
            if self.scoresheet[column] != None:
                continue
            scores[column] = getattr(hand, column)()
        m = max(scores.values())
        for play, score in scores.items():
            if score == m:
                plays.append(play)
        return random.choice(plays)

    def choose_reroll(self):
        prob = .5
        if random.random() < prob:
            return True
        else:
            return False

    def choose_nums(self):
        indices = []
        for i in range(5):
            value = random.random()
            if value < .5:
                indices.append(i)

        return indices

class AI_gen_twopointone(AI_gen_twopointzero):
    def __init__(self, name, generation='2.1'):
        super().__init__(name, generation=generation)

    def choose_reroll(self):
        return True
    
    def choose_nums(self):
        return [0,1,2,3,4]

if __name__ == '__main__':
    pass