import math
import random
import abc
from typing import Generator, Union

class Ant:
    path : list[tuple[int, int]]
    visited : list[int]

    def __init__(self, start_position:int):
        self.path = []
        self.visited = [start_position]

    def move(self, point):
        self.path.append((self.visited[-1], point))
        self.visited.append(point)

class Solution:
    path : list[tuple[int, int]]
    order : list[int]
    func : float

    def __init__(self, path, order, func):
        self.path = path
        self.order = order
        self.func = func

    def __lt__(self, other):
        return self.func < other.func

    def __eq__(self, o: object) -> bool:
        return o and all([ o.order[i] == self.order[i] for i in range(len(self.order)) ])

class AntAlgorithm(abc.ABC):
    graph : list[list[float]]
    pheromone_graph : list[list[float]]
    alpha : float
    beta : float
    elite_ant : int
    max_iter : int
    evaporation : float
    pheromonePerAnt : float

    def __init__(self, graph, alpha=0.5, beta=0.5,
        evaporation=0.1, pheromonePerAnt=0.2, elite_ant=3, max_iter=15, pheromone_graph_size=None):
        
        self.graph = graph
        self.alpha = alpha
        self.beta = beta
        self.elite_ant = elite_ant
        self.max_iter = max_iter
        self.evaporation = evaporation
        self.pheromonePerAnt = pheromonePerAnt
        self.pheromone_graph = [[ 1
                            for _ in range(pheromone_graph_size 
                                if pheromone_graph_size else len(self.graph))]
                            for _ in range(pheromone_graph_size
                                if pheromone_graph_size else len(self.graph))
        ]
        self.__n = pheromone_graph_size if pheromone_graph_size \
                    else len(self.graph)
    
    @abc.abstractmethod
    def func(self, ant:Union[Ant, Solution]) -> float:
        pass

    @abc.abstractmethod
    def calc_distance(self, point, ant=None) -> float:
        pass

    def fitness(self) -> Solution:
        opt_solution = Solution([], [], math.inf)
        iteration = 0
        best_solution = None
        while iteration < self.max_iter:
            solutions = []
            for ant in self.create_ant():
                while len(ant.visited) != self.__n:
                    move = self.next_point(ant)
                    ant.move(move)
                solutions.append(Solution(ant.path, ant.visited, self.func(ant)))
            
            if min(solutions, key=lambda s: s.func) < opt_solution:
                opt_solution = min(solutions, key=lambda s: s.func)

            self.add_pheromone(opt_solution, solutions)

            if opt_solution == best_solution:
                iteration += 1
            else:
                iteration = 0
                best_solution = opt_solution

        return opt_solution

    def create_ant(self) -> Generator:
        for i in range(self.__n):
            yield Ant(i)

    def next_point(self, ant:Ant) -> int:
        start = ant.visited[-1]
        veracity = [0] * self.__n
        for i in range(self.__n):
            if i not in ant.visited and start != i:
                veracity[i] = (self.pheromone_graph[0][i])**self.alpha * \
                (1/self.calc_distance(i, ant))**self.beta

        veracity = [ int(i/(sum(veracity) if sum(veracity) else 1)*100) for i in veracity ]
        point = random.randint(0, 100)
        distance = [ abs(veracity[i]-point) 
            if i not in ant.visited else math.inf  for i in range(len(veracity)) ]
        return distance.index(min(distance))

    def add_pheromone(self, opt_solution, solutions:list[Solution]) -> None:
        for start in range(self.__n):
            for end in range(len(self.pheromone_graph[start])):
                next_pheromone = (1-self.evaporation) * self.pheromone_graph[start][end]
                for sol in solutions:
                    try:    sol.path.index((start, end))
                    except ValueError: continue
                    else:   next_pheromone += self.pheromonePerAnt/sol.func
                self.pheromone_graph[start][end] = next_pheromone

        for start, end in opt_solution.path:
            self.pheromone_graph[start][end] += self.elite_ant * self.pheromonePerAnt/opt_solution.func