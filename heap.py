class Heap:

    def __init__(self, A=None, *, max_size=None, compkey=lambda x: x):
        if A is not None:
            self.A = A
            self.heapsize = len(A) - 1
        else:
            self.A = [None] * max_size
            self.heapsize = -1
        self.compkey = compkey

    def right(self, i):
        return 2 * i + 2

    def left(self, i):
        return 2 * i + 1

    def parent(self, i):
        return (i - 1) // 2

    def swap(self, i, j):
        self.A[i], self.A[j] = self.A[j], self.A[i]
