import random
from LocalSearchAlgorithms.SOpt.core import Solution, Sopt

class SoptFloShop(Sopt):
    def func(self, plan:Solution):
        return self.__cmax(plan, len(self.data), len(self.data[0]))

    def create_plan(self) -> Solution:
        plan = list(range(len(self.data[0])))
        random.shuffle(plan)
        return Solution(plan, self.func(plan))

    def __cmax(self, plan:Solution, i, r) -> float: 
        if r == 0:
            return sum([self.data[s][plan[0]] for s in range(i)])
        elif i == 0:
            return sum([self.data[0][plan[s]] for s in range(r)])
        
        return max(self.__cmax(plan, i-1, r),
                self.__cmax(plan, i, r-1)) + \
                (self.data[i-1][plan[r-1]] if i > 1 and r > 1 else 0)