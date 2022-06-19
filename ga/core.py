import random
import abc
from typing import Iterable 

class Gen:
    chromosomes : list[int]
    age : int
    func : float

    def __init__(self, chromosomes, func=None):
        self.chromosomes = chromosomes
        self.age = 0
        self.func = func

    def nextage(self):
        self.age +=1

    def __len__(self):
        return len(self.chromosomes)

    def __iter__(self):
        return iter(self.chromosomes)
    
    def __getitem__(self, key):
        return self.chromosomes[key]

    def __eq__(self, o: object):
        return o and abs(self.func - o.func) < 1e-5

    def __str__(self):
        return  'gen: ' + ' '.join(map(str, self.chromosomes)) + f' generation: {self.age} fun : {self.func}'

class GA(abc.ABC):
    data : list
    population : list[Gen]
    maxpopulation : int
    maxage : int
    share : int

    def __init__(self, data, maxpopulation,
        maxage=None, share=-1, maxiter=10, n=None, options={}, callable=None):
    
        self.data = data
        self.maxpopulation = maxpopulation
        self.maxage = maxage
        self.maxiter = maxiter
        self.share = share if share > 0 else maxpopulation // 5
        self.callable = callable
        self.n = n or len(data)
        self.options = { 'first_p' : options.get('first_p', 5),
                         'second_p' : options.get('second_p', 35)}

    @abc.abstractmethod
    def crossover(self, leftgen:Gen, rightgen:Gen) -> None:
        pass
    
    @abc.abstractmethod
    def mutation(self, gen:Gen) -> None:
        pass

    @abc.abstractmethod
    def func(self, solution:Iterable) -> float:
        pass

    @abc.abstractmethod
    def creategen(self) -> Gen:
        pass

    @abc.abstractmethod
    def filter(self) -> None:
        pass
    
    def fitness(self) -> Gen:
        self.population = [ self.creategen() for _ in range(self.maxpopulation//2) ]
        self.population.sort(key=lambda item : item.func, reverse=True)
        iteration = 0
        best_solution = None
        while iteration < self.maxiter:
            for _ in range(self.share):
                index1 = self.getindex(random.randint(0, 100))
                index2 = self.getindex(random.randint(0, 100))
                self.crossover(self.population[index1], self.population[index2])

            [ self.mutation(gen) for gen in self.population ]
            [ gen.nextage() for gen in self.population ]
            self.filter()
            self.population.sort(key=lambda item : item.func, reverse=True)

            if self.population[-1] == best_solution:
                iteration += 1
            else:
                iteration = 0
                best_solution = self.population[-1]

        return self.population[-1]
    
    def getindex(self, value:int) -> int:
        if value < self.options['first_p']:
            return random.randint(0, int(len(self.population)*0.1))
        elif value < self.options['second_p']:
            return random.randint(int(len(self.population)*0.1), int(len(self.population)*0.5))
        else:
            return random.randint(int(len(self.population)*0.6), len(self.population)-1)

