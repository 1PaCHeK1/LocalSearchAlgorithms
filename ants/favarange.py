from ants.core import AntAlgorithm
# import matplotlib.pyplot as plot

class AntFAvarange(AntAlgorithm):
    def func(self, ant) -> float:
        result = []
        for i in range(len(self.graph)):
            result.append((result[-1] if len(result) else 0) + self.graph[ant.visited[i]])
        return sum(result)/len(self.graph)

    def calc_distance(self, point, ant) -> float:
        return self.graph[point]

# def runtest(title, mtx, n, cls, params):
#     solutions = []
#     for _ in range(n):
#         solution = cls(mtx, **params).fitness()
#         solutions.append(solution.func)

#     plot.xlabel("Cmax")
#     plot.ylabel("Count")
#     plot.hist(solutions)
#     plot.show()

# works = [1, 5, 3, 7, 4, 10, 6, 15]
# runtest("Ant", works, 3000, AntSpt, { 'max_iter': 20 })