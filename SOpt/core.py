import abc

class Solution:
    plan : list[int]
    func : float

    def __init__(self, plan, func) -> None:
        self.plan = plan
        self.func = func

    def copy(self):
        return self.plan.copy()

    def __len__(self):
        return len(self.plan)

    def __iter__(self):
        return iter(self.plan)
    
    def __getitem__(self, key):
        return self.plan[key]

    def __lt__(self, other):
        return self.func < other.func



class Sopt(abc.ABC):
    data : list
    solution : Solution
    verify : float
    length : int

    def __init__(self, data, length, base_plan=None, verify=None):
        self.data = data
        self.length = length
        self.verify = verify
        self.base_plan = base_plan or self.create_plan()

    @abc.abstractmethod
    def func(self, plan:Solution):
        pass

    @abc.abstractmethod
    def create_plan(self) -> Solution:
        pass

    def fitness(self):
        base_plan = self.base_plan
        new_plan = base_plan
        _key = lambda item : item.func

        while True:
            new_plan = min(base_plan, min(self.stuffing(new_plan.plan, self.length), key=_key), key=_key)

            if new_plan == base_plan or (self.verify and new_plan.func - base_plan.func < self.verify):
                break
            else:
                base_plan = new_plan

        return new_plan

    def stuffing(self, base_plan:list[int], s, start=0):
        if s == 0:
            return
        n = len(base_plan)
        for i in range(start, n-1):
            for j in range(i + 1, n):
                tmp = base_plan.copy()
                tmp[j] = 0 if tmp[j] else 1
                yield Solution(tmp, self.func(tmp))
                for plan in self.stuffing(tmp, s - 1, i+1):
                    yield Solution(plan, self.func(plan))