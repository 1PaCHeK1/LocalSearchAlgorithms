from LocalSearchAlgorithms.ants.core import AntAlgorithm

class AntFAvarange(AntAlgorithm):
    def func(self, ant) -> float:
        result = []
        for i in range(len(self.graph)):
            result.append((result[-1] if len(result) else 0) + self.graph[ant.visited[i]])
        return sum(result)/len(self.graph)

    def calc_distance(self, point, ant) -> float:
        return self.graph[point]
