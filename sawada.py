from dataclasses import dataclass


def count_elements(lst):
    output = []
    for i in set(lst):
        output.append(lst.count(i))
    return output


@dataclass
class Cell:
    next: int
    prev: int


class Sawada:
    def __init__(self, combination):
        self.head = 0
        self.necklaces = []
        self.key = {}
        self.combination = combination
        combo_set = list(set(combination))
        for i in range(len(combo_set)):
            self.key[i] = combo_set[i]
        lst_count = count_elements(combination)
        self.num_map = [i for i in range(len(set(combination))+1)]
        self.K = len(set(combination))
        self.N = len(self.combination)
        self.avail = [Cell(0, 0) for i in range(self.K+2)]
        self.a = [0] * (self.N + 1)
        self.run = [0] * (self.N + 1)
        self.num = [lst_count[i-1] for i in range(1, len(set(combination))+1)]
        self.num.insert(0, 0)
        self.begin()
        self.necklaces = [[self.key[x] for x in y] for y in self.necklaces]

    def remove(self, i):
        if i == self.head:
            self.head = self.avail[i].next
        p = self.avail[i].prev
        n = self.avail[i].next
        self.avail[p].next = n
        self.avail[n].prev = p
        return self

    def add(self, i):
        p = self.avail[i].prev
        n = self.avail[i].next
        self.avail[p].next = i
        self.avail[n].prev = i
        if self.avail[i].prev == self.K + 1:
            self.head = i
        return self

    def result(self):
        h = []
        for j in range(1, self.N + 1):
            h.append(self.num_map[self.a[j]] - 1)
        self.necklaces.append(h)
        return self

    def gen(self, t, p, s):
        if self.num[self.K] == self.N - t + 1:
            if (self.num[self.K] == self.run[t - p]) & (self.N % p == 0):
                self.result()
            elif (self.num[self.K] == self.run[t - p]) & (self.N == p):
                self.result()
            elif self.num[self.K] > self.run[t - p]:
                self.result()
        elif self.num[1] != self.N - t + 1:
            j = self.head
            s2 = s
            while j >= self.a[t - p]:
                self.run[s] = t - s
                self.a[t] = j

                self.num[j] -= 1
                if self.num[j] == 0:
                    self.remove(j)

                if j != self.K:
                    s2 = t + 1
                if j == self.a[t - p]:
                    self.gen(t + 1, p, s2)
                else:
                    self.gen(t + 1, t, s2)

                if self.num[j] == 0:
                    self.add(j)
                self.num[j] += 1

                j = self.avail[j].next
            self.a[t] = self.K
        return self

    def begin(self):
        for j in range(self.K + 1, -1, -1):
            self.avail[j].next = j - 1
            self.avail[j].prev = j + 1
        self.head = self.K

        for j in range(1, self.N + 1):
            self.a[j] = self.K
            self.run[j] = 0

        self.a[1] = 1
        self.num[1] -= 1
        if self.num[1] == 0:
            self.remove(1)

        self.gen(2, 1, 2)
        return self
