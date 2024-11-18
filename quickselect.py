from sorting import partition


def quick_select(A, k, *, start=0, end=None):
    assert A is not None
    assert 0 <= k < len(A)
    assert 0 <= start < len(A)
    assert end is None or start < end <= len(A)

    """
    Seleziona il k-esimo elemento più piccolo da A[start:end].

    Argomenti:
    - A     : vettore di cui calcolare il k-esimo elemento
    - k     : indice dell'elemento da calcolare
    - start : posizione iniziale da considerare
    - end   : posizione finale da considerare
    """

    if end is None:
        end = len(A)

    p = partition(A, start=start, end=end)

    while p != k:
        if p > k:
            end = p
        else:
            start = p + 1
        p = partition(A, start=start, end=end)

    return A[k]


if __name__ == "__main__":
    A = [int(x) for x in input().strip().split(" ")]
    k = int(input()) - 1

    print(quick_select(A, k))
