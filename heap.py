class Heap:

    def __init__(self, A=None, *, compkey=lambda x: x):
        self.A = A if A is not None else []
        self.heapsize = len(self.A) - 1
        self.compkey = compkey

    def right(self, i):
        return 2 * i + 2

    def left(self, i):
        return 2 * i + 1

    def parent(self, i):
        return (i - 1) // 2

    def swap(self, i, j):
        self.A[i], self.A[j] = self.A[j], self.A[i]
