
import json



class DataReader:
    def __init__(self):
        pass
    
    def read_data(self):
        with open('data.json', 'r') as file:
            data = json.load(file)
        print(data)


if __name__ == '__main__':
    reader = DataReader()
    reader.read_data()