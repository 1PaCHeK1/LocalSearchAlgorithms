from ants.core import AntAlgorithm

class AntTravelingSalesman(AntAlgorithm):
    def func(self, ant) -> float:
        result = 0
        for f, t in ant.path:
            result += self.graph[f][t]
        result += self.graph[ant.path[-1][-1]][ant.path[0][0]]
        return result

    def calc_distance(self, point, ant) -> float:
        return self.graph[ant.visited[-1]][point]


# mtx =  [
#     [math.inf, 1, 7, 3, 14, 2],
#     [3, math.inf, 6, 9, 1, 24],
#     [6, 14, math.inf, 3, 7, 3],
#     [2, 3, 5, math.inf, 9, 11],
#     [15, 7, 11, 2, math.inf, 4],
#     [20, 5, 13, 4, 18, math.inf],
# ]