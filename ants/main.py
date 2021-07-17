from LocalSearchAlgorithms.ants.core import Ant, AntAlgorithm, Solution
from typing import Union

class AntFlowShop(AntAlgorithm):
    def func(self, ant:Union[Ant, Solution]) -> float:
        return self.__cmax(ant, len(self.graph), len(self.graph[0]))

    def calc_distance(self, point, ant) -> float:  
        return self.graph[0][point]
        
        maximum = 0
        m = len(self.graph)
        w = set(range(len(self.graph[0]))) - set(ant.visited)
        for i in range(m):
            cmax = self.__cmax(ant, i, len(ant.visited))
            col_sum = sum([ self.graph[i][u] for u in w])
            min_machine = min([sum([ self.graph[l][u] 
                for l in range(i+1, m) ]) for u in w]) if i + 1 < m else 0
    
            maximum = max(maximum, cmax + col_sum + min_machine)
        return maximum

    def __cmax(self, ant, i, r) -> float: 
        if r == 0:
            return sum([self.graph[s][ant.visited[0]] for s in range(i)])
        elif i == 0:
            return sum([self.graph[0][ant.visited[s]] for s in range(r)])
        
        return max(self.__cmax(ant, i-1, r),
                self.__cmax(ant, i, r-1)) + \
                (self.graph[i-1][ant.visited[r-1]] if i > 1 and r > 1 else 0)

