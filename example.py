from ga import GAFlowShop
from ants import AntFlowShop
from SOpt import SoptFloShop
import random

def runtest(n, m, k):
    solutions = []
    with open(f'cache.txt', 'a') as cache:
        cache.write(f"start work\nInput value: n = {n}, m = {m}, k = {k}\n")
        for _ in range(k):
            mtx = [ [ random.randint(1, 20) for _ in range(n) ]
                for _ in range(m)]
            ga_func = (GAFlowShop(mtx, 25, n=len(mtx[0])).fitness().func, 'ga')
            aa_func = (AntFlowShop(mtx, max_iter=10, pheromone_graph_size=len(mtx[0])).fitness().func, 'ant')
            sa_func = (SoptFloShop(mtx, 2).fitness().func, 'sopt')
            solutions.append(min([ga_func, aa_func, sa_func]))
            cache.write(f"{len(solutions)}, {solutions[-1]}\n")
            print(f"{len(solutions)}, {solutions[-1]}")
        cache.write("end work\n\n")

    with open('results.txt', 'a') as f:
        f.write(f"Input value: n = {n}, m = {m}, k = {k}\nResults:\n")
        f.write('\tga    = ' +
            '{:.2f}'.format(len([0 for i in solutions if i[1] == 'ga'])/len(solutions)*100)  + '%\n')
        f.write('\tant   = ' + 
            '{:.2f}'.format(len([0 for i in solutions if i[1] == 'ant'])/len(solutions)*100)  + '%\n')
        f.write('\ts-opt = ' + 
            '{:.2f}'.format(len([0 for i in solutions if i[1] == 'sopt'])/len(solutions)*100) + '%\n\n')
    print("finish")

runtest(6, 3, 1000)

runtest(10, 5, 750)

runtest(15, 3, 500)

runtest(6, 12, 410)
