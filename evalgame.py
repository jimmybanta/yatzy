


from deeprlgame2 import DeepRLGame3DQN

from ai_gen_8 import AIGenEightPointTwo



class EvalGame(DeepRLGame3DQN):
    def __init__(self, player, num):
        super().__init__(gen=None)
        self.player = player
        self.scores = []
        self.num = num
    
    def evaluate(self):
        player = self.player

        for i in range(self.num):
            player.clear_scoresheet()

            turns = 0
            while turns < 15:
                self.ai_turn(player)
                turns += 1
            
            score = player.calculate_score()
            self.scores.append(score)
    
    def results(self):
        return sum(self.scores) / len(self.scores)
        


        

class EvalBot():
    def __init__(self):
        self.moves_dqn = DQN(15)
        self.reroll_dqn = DQN(2)
        self.indices_dqn = DQN(31)
        self.moves_dqn.eval()
        self.reroll_dqn.eval()
        self.indices_dqn.eval()
        
    
