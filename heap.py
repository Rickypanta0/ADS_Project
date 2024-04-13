class Heap:
    def __init__(self, A=None) -> None:
        self.A = A if A is not None else []
        self.heapsize = len(self.A) - 1

    @staticmethod
    def right(i):
        return 2 * i + 2

    @staticmethod
    def left(i):
        return 2 * i + 1

    def parent(self, i):
        return (i - 1) // 2

    def swap(self, i, j):
        self.A[i], self.A[j] = self.A[j], self.A[i]

