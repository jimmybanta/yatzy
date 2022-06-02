


from game_ai import AIGame
from ai_gen_5 import AIGenFivePointTwo



class AIDataGatherer(AIGame):
    def __init__(self, num_games, player):
        super().__init__(num_games, player)
    
    def data_game_loop(self):
        turns = 0
        self.player.game_data = {}
        while turns < 15:
            self.player.data_turn()
            turns += 1

        if self.player.calculate_score() > 300:
            self.player.update_three_hundred()
            self.player.save_game_data('300data.json')
    

    def play(self):

        for i in range(self.num_games):
            self.player.reset_scoresheet()

            self.data_game_loop()

            if i % 1000 == 0:
                print('Game {} complete'.format(i))

    


if __name__ == '__main__':
    player = AIGenFivePointTwo('karen')
    game = AIDataGatherer(10000000, player)

    game.play()