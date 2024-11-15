def partition(A, *, start=0, end=None, pivot=None):
    assert A is not None
    assert 0 <= start < len(A)
    assert end is None or start < end <= len(A)

    """
    Partiziona il vettore A.
    
    Argomenti:
    - A     : il vettore da partizionare
    - start : posizione iniziale da considerare. Se non specificata è 0.
    - end   : posizione finale esclusa da considerare. Se non specificata 
                è la lunghezza di A.
    - pivot : pivot da utilizzare.
    """

    if end is None:
        end = len(A)

    if pivot is None:
        ppos = end - 1
    else:
        # il costo rimane lineare
        ppos = A.index(pivot, start, end)

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


def insertion_sort(A, *, start=0, end=None, compkey=lambda x: x):
    assert A is not None
    assert 0 <= start < len(A)
    assert end is None or start < end <= len(A)

    """
    Ordina il vettore A.
    
    Argomenti:
    - A       : il vettore da ordinare
    - start   : posizione iniziale da considerare. Se non specificata è 0.
    - end     : posizione finale da considerare. Se non specificata è la
                lunghezza di A.
    - compkey : funzione che ritorna la chiave da utilizzare per i confronti.
    """

    if end is None:
        end = len(A)

    for j in range(start + 1, end):
        k = A[j]
        i = j - 1
        while i >= start and compkey(k) <= compkey(A[i]):
            A[i + 1] = A[i]
            i = i - 1
        A[i + 1] = k
