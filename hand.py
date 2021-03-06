

from dice import D6

class YatzyHand(list):
    def __init__(self, nums=None):
        super().__init__()

        if nums:
            length = len(nums)
            if length == 5:
                for num in nums:
                    self.append(D6(value=num))
            else:
                for num in nums:
                    self.append(D6(value=num))
                for _ in range(5 - length):
                    self.append(D6())

        else:
            for _ in range(5):
                self.append(D6())
            
        self.sort()

    def _by_value(self, value):
        dice = []
        for die in self:
            if die == value:
                dice.append(value)
        return dice
    
    @property
    def total_ones(self):
        return self._by_value(1)

    @property
    def total_twos(self):
        return self._by_value(2)
    
    @property
    def total_threes(self):
        return self._by_value(3)
    
    @property
    def total_fours(self):
        return self._by_value(4)

    @property
    def total_fives(self):
        return self._by_value(5)

    @property
    def total_sixes(self):
        return self._by_value(6)

    @property
    def _sets(self):
        return {
            1:len(self.total_ones), 
            2:len(self.total_twos),
            3:len(self.total_threes),
            4:len(self.total_fours),
            5:len(self.total_fives),
            6:len(self.total_sixes)
        }
        
    def ones(self):
        return sum(self.total_ones)

    def twos(self):
        return sum(self.total_twos)

    def threes(self):
        return sum(self.total_threes)

    def fours(self):
        return sum(self.total_fours)

    def fives(self):
        return sum(self.total_fives)

    def sixes(self):
        return sum(self.total_sixes)

    def one_pair(self):
        dice = [0]
        for i in range(1,7):
            if self._sets[i] >= 2:
                dice.append(2 * i)
        return max(dice)

    def two_pair(self):
        dice = []
        if (list(self._sets.values()).count(2) == 2 or 
            (list(self._sets.values()).count(2) == 1 and list(self._sets.values()).count(3) == 1)):

            for i in range(1,7):
                if self._sets[i] >= 2:
                    dice.append(2 * i)
            return sum(dice)
        return 0
    
    def three_kind(self):
        for i in range(1,7):
            if self._sets[i] >= 3:
                return 3 * i
        return 0


    def four_kind(self):
        for i in range(1,7):
            if self._sets[i] >= 4:
                return 4 * i
        return 0
    
    def small_straight(self):
        if self == [1,2,3,4,5]:
            return 15
        return 0

    def large_straight(self):
        if self == [2,3,4,5,6]:
            return 20
        return 0

    def full_house(self):
        final = 0
        if 3 in self._sets.values() and 2 in self._sets.values():
            for i in range(1,7):
                if self._sets[i] == 3:
                    final += 3 * i
                if self._sets[i] == 2:
                    final += 2 * i
        return final

    def chance(self):
        return sum([int(die) for die in self])

    def yatzy(self):
        if 5 in self._sets.values():
            return 50
        return 0
        
    def reroll(self, indices):
        non_rerolled = [int(self[i]) for i in range(5) if i not in indices]
        rerolled = [int(D6()) for _ in range(len(indices))]

        return YatzyHand(non_rerolled + rerolled)

