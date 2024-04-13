def partition(A, *, start=0, end=None, ppos=None):
    assert A is not None
    assert 0 <= start < len(A)
    assert end is None or start < end <= len(A)
    assert ppos is None or start <= ppos < end

    """Partition A.

    Positional arguments:
        A    : the list to partition.
    Keyword arguments:
        start: partition A from this position; ignore what's before;
                defaults to 0;
        end  : partition A up until this position NOT included; ignore
                what's after; defaults to the length of A;
        ppos : use the element at this position as the pivot; defaults
                to the last element of A.
    """

    if end is None:
        end = len(A)

    if ppos is None:
        ppos = end - 1

    pivot = A[ppos]
    A[ppos], A[end - 1] = A[end - 1], A[ppos]

    # if start <= k < i then A[k] <= pivot
    # if i < k <= j     then A[k] > pivot

    i = start
    for j in range(start, end):
        if A[j] <= pivot:
            A[j], A[i] = A[i], A[j]
            i = i + 1

    return i - 1


# Used in medianofmedians to sort the fixed-size lists
def insertionsort(A, *, start=0, end=None):
    assert A is not None
    assert 0 <= start < len(A)
    assert end is None or start < end <= len(A)

    """Sort A.

    Position arguments:
        A    : the list to sort.
    Keyword arguments:
        start: start sorting from this position; ignore what's before;
                defaults to 0;
        end  : stop sorting at this position NOT included; ignore
                what's after; defaults to the length of A.
    """

    if end is None:
        end = len(A)

    for j in range(start + 1, end):
        k = A[j]
        i = j - 1
        while i >= start and k <= A[i]:
            A[i + 1] = A[i]
            i = i - 1
        A[i + 1] = k
