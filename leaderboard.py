from ast import Pass
import csv
import statistics
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
import os.path

GENERATIONS = ['human', 
                '1.0', '1.1', '1.2', 
                '2.0', '2.1', 
                '3.0', '3.1', '3.2', 
                '4.0', '4.1', 
                '5.0', '5.1', '5.2', 
                '6.0', '6.1', '6.1.1', '6.2', '6.3', '6.4',
                '7.0', '7.1', '7.2', '7.2.1',
                '8.0.0', '8.0.1', '8.1'
                ]

N_BINS = 374

class Leaderboard(list):
    def __init__(self, gen):
        super().__init__()
        self.gen = gen

    def load(self):
        if os.path.exists('leaderboards/lboard_{}.csv'.format(self.gen)):
            with open('leaderboards/lboard_{}.csv'.format(self.gen), 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    d = {}
                    d['generation'] = row['generation']
                    d['name'] = row['name']
                    d['score'] = int(row['score'])
                    self.append(d)

            self = sorted(self, key=lambda x:x['score'], reverse=True)

    def update(self, final_scores):
        for score in final_scores:
            self.append(score)

        self.sort(key=lambda x:x['score'], reverse=True)

    def write(self):
        with open('leaderboards/lboard_{}.csv'.format(self.gen), 'w') as file:
            fields = ['generation', 'name', 'score']
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(self)

    def analyze(self):
        scores = []
        for dic in self:
            if dic['generation'] == self.gen:
                scores.append(int(dic['score']))

        iterations = len(scores)
        avg = statistics.mean(scores)
        median = statistics.median(scores)
        mode = statistics.mode(scores)
        std = statistics.pstdev(scores)

        with open('analysis.csv', 'a') as file:
            fields = ['generation', 'iterations', 'average', 'median', 'mode', 'standard deviation']
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writerow({
                'generation':self.gen, 
                'iterations':iterations, 
                'average':avg, 
                'median':median, 
                'mode':mode, 
                'standard deviation':std})

    def run(self, final_scores):
        self.load()
        self.update(final_scores)
        self.write()
        self.analyze()

    def print(self, end, start=0):
        print('')
        print('Here is the leaderboard!')
        print('')
        for i, person in enumerate(self):
            if i < start:
                continue
            if i > end - 1:
                continue
            if person['generation'] == 'human':
                print('{}: {} ({}) - {} points'.format(i + 1, person['name'], person['generation'], person['score']))
            else:
                print('{}: {} (Generation {}) - {} points'.format(i + 1, person['name'], person['generation'], person['score']))
        print('')

    def print_top_ten(self):
        self = self[0:10]
        print('')
        print('Here is the leaderboard!')
        print('')
        for i, person in enumerate(self):
            if person['generation'] == 'human':
                print('{}: {} ({}) - {} points'.format(i + 1, person['name'], person['generation'], person['score']))
            else:
                print('{}: {} (Generation {}) - {} points'.format(i + 1, person['name'], person['generation'], person['score']))
        print('')

    def print_bottom_ten(self):
        length = len(self)
        self = self[length - 10: length]
        print('')
        print('Losers!')
        print('')
        start = 1
        for person in self[::-1]:
            print('{}: {} (Generation {}) - {} points'.format(start, person['name'], person['generation'], person['score']))
            start += 1
        print('')

    def plot_data(self):
        data = []

        for item in self:
            if item['generation'] == self.gen:
                data.append(item['score'])
        
        plt.hist(data, color='blue', bins=N_BINS)
        plt.xlim([0, 374])
        plt.title('Generation {} Score Distribution'.format(self.gen))
        plt.xlabel('Score')
        plt.ylabel('Games')
        plt.show()

    def print_stats(self):
        with open('analysis.csv','r') as file:
            fields = ['generation', 'iterations', 'average', 'median', 'mode', 'standard deviation']
            reader = csv.DictReader(file, fieldnames=fields)
            for row in reader:
                if row['generation'] == self.gen:
                    iterations = row['iterations']
                    average = row['average']
                    median = row['median']
                    mode = row['mode']
                    std = row['standard deviation']

        print('Generation {} Stats:'.format(self.gen))
        print('')
        print('Total iterations: {}'.format(iterations))
        print('Average score: {}'.format(round(float(average), 2)))
        print('Median score: {}'.format(median))
        print('Mode: {}'.format(mode))
        print('Standard Deviation: {}'.format(round(float(std),2)))

class TopTen(list):
    def __init__(self):
        super().__init__()
        self.generations = GENERATIONS

    def load(self):
        for generation in self.generations:
            with open('leaderboards/lboard_{}.csv'.format(generation), 'r') as file:
                reader = csv.DictReader(file)
                value = 0
                for row in reader:
                    if value > 20:
                        break
                    d = {}
                    d['generation'] = row['generation']
                    d['name'] = row['name']
                    d['score'] = row['score']
                    self.append(d)
                    value += 1
        
        self.sort(key=lambda x:int(x['score']), reverse=True)

    def print(self):
        self = self[0:10]
        print('')
        print('Here is the leaderboard!')
        print('')
        for i, person in enumerate(self):
            if person['generation'] == 'human':
                print('{}: {} ({}) - {} points'.format(i + 1, person['name'], person['generation'], person['score']))
            else:
                print('{}: {} (Generation {}) - {} points'.format(i + 1, person['name'], person['generation'], person['score']))
        print('')

    def write(self):
        self = self[0:10]
        with open('leaderboards/topten.csv', 'w') as file:
            fields = ['generation', 'name', 'score']
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(self)

    def run(self):
        self.load()
        self.write()
        self.print()

class BottomTen(TopTen):

    def load(self):
        for generation in self.generations:
            length = 0
            with open('leaderboards/lboard_{}.csv'.format(generation), 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    length += 1

            with open('leaderboards/lboard_{}.csv'.format(generation), 'r') as file:
                reader = csv.DictReader(file)
                value = 0
                for row in reader:
                    value += 1
                    if value < length - 20:
                        continue
                    d = {}
                    d['generation'] = row['generation']
                    d['name'] = row['name']
                    d['score'] = row['score']
                    self.append(d)


        self.sort(key=lambda x:int(x['score']))
                
    def print(self):
        self = self[0:10]
        print('')
        print('Losers!')
        print('')
        for i, person in enumerate(self):
            if person['generation'] == 'human':
                print('{}: {} ({}) - {} points'.format(i + 1, person['name'], person['generation'], person['score']))
            else:
                print('{}: {} (Generation {}) - {} points'.format(i + 1, person['name'], person['generation'], person['score']))
        print('')

    def write(self):
        self = self[0:10]
        with open('leaderboards/bottomten.csv', 'w') as file:
            fields = ['generation', 'name', 'score']
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(self)

class TopFifty(TopTen):
    def load(self):
        for generation in self.generations:
            with open('leaderboards/lboard_{}.csv'.format(generation), 'r') as file:
                reader = csv.DictReader(file)
                value = 0
                for row in reader:
                    if value > 50:
                        break
                    d = {}
                    d['generation'] = row['generation']
                    d['name'] = row['name']
                    d['score'] = row['score']
                    self.append(d)
                    value += 1
        
        self.sort(key=lambda x:int(x['score']), reverse=True)

    def write(self):
        self = self[0:50]
        with open('leaderboards/topfifty.csv', 'w') as file:
            fields = ['generation', 'name', 'score']
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(self)

    def run(self):
        self.load()
        self.write()

class BottomFifty(BottomTen):
    def load(self):
        for generation in self.generations:
            length = 0
            with open('leaderboards/lboard_{}.csv'.format(generation), 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    length += 1

            with open('leaderboards/lboard_{}.csv'.format(generation), 'r') as file:
                reader = csv.DictReader(file)
                value = 0
                for row in reader:
                    value += 1
                    if value < length - 50:
                        continue
                    d = {}
                    d['generation'] = row['generation']
                    d['name'] = row['name']
                    d['score'] = row['score']
                    self.append(d)


        self.sort(key=lambda x:int(x['score']))

    def write(self):
        self = self[0:50]
        with open('leaderboards/bottomfifty.csv', 'w') as file:
            fields = ['generation', 'name', 'score']
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(self)

    def run(self):
        self.load()
        self.write()

def analyze(gen):
    leaderboard = Leaderboard(gen)
    top_ten = TopTen()
    if gen not in GENERATIONS:
        GENERATIONS.append(gen)
    bottom_ten = BottomTen()

    top_fifty = TopFifty()
    bottom_fifty = BottomFifty()

    leaderboard.load()

    top_ten.run()
    print('')
    print('')
    bottom_ten.run()
    print('')
    print('')
    top_fifty.run()
    bottom_fifty.run()
    leaderboard.print_stats()
    print('')
    print('')
    leaderboard.plot_data()


if __name__ == '__main__':

    analyze('human')
