from heap import Heap


class MinHeap(Heap):

    def heapify(self, i):
        r = self.right(i)
        l = self.left(i)
        if self.heapsize >= r and self.A[i] > self.A[r]:
            m = r
        else:
            m = i
        if self.heapsize >= l and self.A[m] > self.A[l]:
            m = l
        if m != i:
            self.swap(i, m)
            self.heapify(m)

    def extract(self):
        if self.heapsize < 0:
            return None
        key = self.A[0]
        self.A[0] = self.A[self.heapsize]
        self.A.pop()
        self.heapsize -= 1
        self.heapify(0)
        return key

    def insert(self, k):
        if len(self.A) > self.heapsize:
            self.heapsize += 1
            self.A.append(k)
            i = self.heapsize
            while i > 0 and self.A[i] < self.A[self.parent(i)]:
                self.swap(i, self.parent(i))
                i = self.parent(i)

    def build(self):
        for i in range(self.heapsize // 2, -1, -1):
            self.heapify(i)


class MaxHeap(Heap):

    def heapify(self, i):
        r = self.right(i)
        l = self.left(i)
        if self.heapsize >= r and self.A[i] < self.A[r]:
            m = r
        else:
            m = i
        if self.heapsize >= l and self.A[m] < self.A[l]:
            m = l
        if m != i:
            self.swap(i, m)
            self.heapify(m)

    def extract(self):
        if self.heapsize < 0:
            return None
        key = self.A[0]
        self.A[0] = self.A[self.heapsize]
        self.A.pop()
        self.heapsize -= 1
        self.heapify(0)
        return key

    def insert(self, k):
        if len(self.A) > self.heapsize:
            self.heapsize += 1
            self.A.append(k)
            i = self.heapsize
            while i > 0 and self.A[i] > self.A[self.parent(i)]:
                self.swap(i, self.parent(i))
                i = self.parent(i)

    def build(self):
        for i in range(self.heapsize // 2, -1, -1):
            self.heapify(i)

