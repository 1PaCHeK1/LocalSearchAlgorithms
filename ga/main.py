import random
from bisect import bisect
from typing import Iterable
from LocalSearchAlgorithms.ga.core import Gen, GA


class GAFlowShop(GA):
    
    def crossover(self, leftgen:Gen, rightgen:Gen) -> None:
        new_gen1_code = leftgen[:len(leftgen)//3] + rightgen[len(leftgen)//3:2*len(leftgen)//3] + leftgen[2*len(leftgen)//3:]
        new_gen2_code = rightgen[:len(leftgen)//3] + leftgen[len(leftgen)//3:2*len(leftgen)//3] + rightgen[2*len(leftgen)//3:]
        
        new_gen1 = Gen(new_gen1_code, self.func(new_gen1_code))
        new_gen2 = Gen(new_gen2_code, self.func(new_gen2_code))

        if len(self.population) < self.maxpopulation+1:
            tmp = [ i.func for i in self.population]
            index = bisect(tmp, new_gen1.func)
            self.population.insert(index, new_gen1)
        if len(self.population) < self.maxpopulation+1:
            tmp = [ i.func for i in self.population]
            index = bisect(tmp, new_gen2.func)
            self.population.insert(index, new_gen2)

    def mutation(self, gen:Gen) -> None:
        for _ in range(max(len(self.data)//2-gen.age, 0)):
            index1 = random.randint(0, len(gen)-1)
            index2 = random.randint(0, len(gen)-1)
            tmp = gen.chromosomes[index1]
            gen.chromosomes[index1] = gen.chromosomes[index2]
            gen.chromosomes[index2] = tmp
            gen.func = self.func(gen)

    def func(self, solution:Iterable) -> float:
        return self.__cmax(solution, len(self.data), len(self.data[0]))

    def creategen(self) -> Gen:
        gen_code = list(range(len(self.data[0]))) 
        random.shuffle(gen_code)
        return Gen(gen_code, self.func(gen_code))

    def filter(self) -> None:
        self.population = [ gen for gen in self.population 
            if len(set(range(self.__n)) - set(gen)) == 0 ]
        self.population = self.population[len(self.population)//3:]

    def __cmax(self, gen, i, r) -> float: 
        if r == 0:
            return sum([self.data[s][gen[0]] for s in range(i)])
        elif i == 0:
            return sum([self.data[0][gen[s]] for s in range(r)])
        
        return max(self.__cmax(gen, i-1, r),
                self.__cmax(gen, i, r-1)) + \
                (self.data[i-1][gen[r-1]] if i > 1 and r > 1 else 0)
