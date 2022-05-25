import random

class Die:
    def __init__(self, sides, value=0):
        self.value = value or random.randint(1, sides)

    def __int__(self):
        return self.value
    
    def __eq__(self, other):
        return int(self) == other
    
    def __ne__(self, other):
        return  int(self) != other

    def __gt__(self, other):
        return int(self) > other
    
    def __lt__(self, other):
        return int(self) < other

    def __ge__(self, other):
        return int(self) > other or int(self) == other

    def __le__(self, other):
        return int(self) < other or int(self) == other
    
    def __str__(self):
        return f'{self.value}'
    
    def __repr__(self):
        return str(self.value)


class D6(Die):
    def __init__(self, value=0):
        super().__init__(6, value=value)
