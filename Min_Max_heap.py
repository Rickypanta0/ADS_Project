from heap import Heap


class MinHeap(Heap):

    def heapify(self, i):
        r = self.right(i)
        l = self.left(i)
        if self.heapsize >= r and self.compkey(self.A[i]) > self.compkey(self.A[r]):
            m = r
        else:
            m = i
        if self.heapsize >= l and self.compkey(self.A[m]) > self.compkey(self.A[l]):
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
            while i > 0 and self.compkey(self.A[i]) < self.compkey(
                self.A[self.parent(i)]
            ):
                self.swap(i, self.parent(i))
                i = self.parent(i)

    def build(self):
        for i in range(self.heapsize // 2, -1, -1):
            self.heapify(i)

    def verify(self, i):
        cond = True
        left = self.left(i)
        right = self.right(i)
        if left <= self.heapsize:
            cond = cond and (self.compkey(self.A[i]) <= self.compkey(self.A[left]))
            cond = cond and self.verify(left)
        if right <= self.heapsize:
            cond = cond and (self.compkey(self.A[i]) <= self.compkey(self.A[right]))
            cond = cond and self.verify(right)
        return cond


class MaxHeap(Heap):

    def heapify(self, i):
        r = self.right(i)
        l = self.left(i)
        if self.heapsize >= r and self.compkey(self.A[i]) < self.compkey(self.A[r]):
            m = r
        else:
            m = i
        if self.heapsize >= l and self.compkey(self.A[m]) < self.compkey(self.A[l]):
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
            while i > 0 and self.compkey(self.A[i]) > self.compkey(
                self.A[self.parent(i)]
            ):
                self.swap(i, self.parent(i))
                i = self.parent(i)

    def build(self):
        for i in range(self.heapsize // 2, -1, -1):
            self.heapify(i)

    def verify(self, i):
        cond = True
        left = self.left(i)
        right = self.right(i)
        if left <= self.heapsize:
            cond = cond and (self.compkey(self.A[i]) >= self.compkey(self.A[left]))
            cond = cond and self.verify(left)
        if right <= self.heapsize:
            cond = cond and (self.compkey(self.A[i]) >= self.compkey(self.A[right]))
            cond = cond and self.verify(right)
        return cond
