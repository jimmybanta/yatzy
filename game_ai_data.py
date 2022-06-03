


from game_ai import AIGame
from ai_gen_5 import AIGenFivePointTwo



class AIDataGatherer(AIGame):
    def __init__(self, num_games, player, lim, gen, datapoints=False):
        super().__init__(num_games, player)
        self.lim = lim
        self.datapoints = datapoints
        self.gen = gen
    
    def data_game_loop(self):
        turns = 0
        self.player.game_data = {}
        while turns < 15:
            self.player.data_turn()
            turns += 1

        if self.player.calculate_score() >= self.lim:
            self.player.update_lim_data()
            
    

    def play(self):


        for i in range(self.num_games):
            self.player.reset_scoresheet()

            self.data_game_loop()

            if i % 1000 == 0:
                print('Game {} complete'.format(i))
            if i % 10000 == 0:
                self.player.save_game_data('sl_data/{}_data.json'.format(self.gen))

            if self.datapoints and len(player.lim_data) >= self.datapoints:
                break

        self.player.save_game_data('sl_data/{}_data.json'.format(self.gen))
        print('Done!')

    


if __name__ == '__main__':
    player = AIGenFivePointTwo('karen')
    game = AIDataGatherer(3000, player, 0, '10.0')

    game.play()