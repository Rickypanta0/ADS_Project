from heap import *

class MinHeap(Heap):
    
    def Heapify(self, i):
        r=Heap.right(i)
        l=Heap.left(i)
        if self.heapsize>=r and self.A[i]>self.A[r]:
            m=r
        else:
            m=i
        if self.heapsize>=l and self.A[m]>self.A[l]:
            m=l
        if m!=i:
            Heap.swap(i,m)
            self.Heapify(m)
    
    def Heap_Extract(self):
        key=self.A[0]
        self.swap(self.heapsize,0)
        self.heapsize-=1
        self.Heapify(0)
        return key
    
    def Heap_Insert(self,k):
        if len(self.A)>self.heapsize:
            self.heapsize+=1
            self.A[self.heapsize]=k
            i=self.heapsize
            while i>0 and self.A[i]<self.A[Heap.parent(i)]:
                Heap.swap(i,Heap.parent(i))
                i=Heap.parent(i)
    
    def Build_Heap(self):
        for i in range(self.heapsize//2,-1,-1):
            self.Heapify(i)
            
class MaxHeap(Heap):
    
    def Heapify(self, i):
        r=Heap.right(i)
        l=Heap.left(i)
        if self.heapsize>=r and self.A[i]<self.A[r]:
            m=r
        else:
            m=i
        if self.heapsize>=l and self.A[m]<self.A[l]:
            m=l
        if m!=i:
            Heap.swap(i,m)
            self.Heapify(m)
    
    def Heap_Extract(self):
        key=self.A[0]
        self.swap(self.heapsize,0)
        self.heapsize-=1
        self.Heapify(0)
        return key
    
    def Heap_Insert(self,k):
        if len(self.A)>self.heapsize:
            self.heapsize+=1
            self.A[self.heapsize]=k
            i=self.heapsize
            while i>0 and self.A[i]>self.A[Heap.parent(i)]:
                Heap.swap(i,Heap.parent(i))
                i=Heap.parent(i)
    
    def Build_Heap(self):
        for i in range(self.heapsize//2,-1,-1):
            self.Heapify(i)