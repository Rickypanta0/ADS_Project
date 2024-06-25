from Min_Max_heap import MinHeap, MaxHeap

def heap_select(A, k):
    assert A is not None
    assert 0 <= k < len(A)

    if k <= (len(A) // 2):
        H1 = MinHeap(A)
        H2 = MinHeap(compkey=lambda x: x[0])
    else:
        H1 = MaxHeap(A)
        k = len(A) - k - 1
        H2 = MaxHeap(compkey=lambda x: x[0])
    H1.build()
    H2.insert((H1.A[0], 0))

    for _ in range(k):
        r, i = H2.extract()
        left = H1.left(i)
        right = H1.right(i)
        if left <= H1.heapsize:
            H2.insert((H1.A[left], left))
        if right <= H1.heapsize:
            H2.insert((H1.A[right], right))
    return H2.extract()[0]



if __name__ == '__main__':
    A = [int(x) for x in input().strip().split(' ')]
    k = int(input()) - 1

    print(heap_select(A, k))

