from math import ceil
from functools import partial

from sorting import partition, insertion_sort

DEFAULT_BLOCK_SIZE = 5


def mom_select_non_in_place(A, k, *, start=0, end=None, block_size=DEFAULT_BLOCK_SIZE):
    assert A is not None
    assert 0 <= start < len(A)
    assert (end is None) or (start < end <= len(A))
    assert block_size > 0

    if end is None:
        end = len(A)

    assert start <= k < end

    subarray_length = end - start
    if subarray_length == 1:
        return A[start]

    # calcola il vettore delle mediane
    n_medians = ceil(subarray_length / 5)
    medians = [None] * n_medians
    for i in range(n_medians):
        block_start = start + i * block_size
        block_end = min(block_start + block_size, end)
        insertion_sort(A, start=block_start, end=block_end)
        median_position = (block_start + block_end) // 2
        medians[i] = A[median_position]

    # trova la mediana delle mediane
    mom = mom_select_non_in_place(medians, n_medians // 2)

    p = partition(A, start=start, end=end, pivot=mom)
    if p > k:
        return mom_select_non_in_place(A, k, start=start, end=p, block_size=block_size)
    elif p < k:
        return mom_select_non_in_place(
            A, k, start=p + 1, end=end, block_size=block_size
        )
    else:
        return A[k]


def mom_select_quasi_in_place(
    A, k, *, start=0, end=None, block_size=DEFAULT_BLOCK_SIZE
):
    assert A is not None
    assert 0 <= start < len(A)
    assert (end is None) or (start < end <= len(A))
    assert block_size > 0

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

    assert start <= k < end

    subarray_length = end - start
    if subarray_length == 1:
        return A[start]

    # calcola il vettore delle mediane
    n_medians = ceil(subarray_length / 5)
    for i in range(n_medians):
        block_start = start + i * block_size
        block_end = min(block_start + block_size, end)
        insertion_sort(A, start=block_start, end=block_end)
        median_position = (block_start + block_end) // 2
        A[start + i], A[median_position] = A[median_position], A[start + i]

    # trova la mediana delle mediane
    mom = mom_select_quasi_in_place(
        A,
        start + (n_medians // 2),
        start=start,
        end=start + n_medians,
        block_size=block_size,
    )
    assert mom is not None

    p = partition(A, start=start, end=end, pivot=mom)
    if p > k:
        return mom_select_quasi_in_place(
            A, k, start=start, end=p, block_size=block_size
        )
    elif p < k:
        return mom_select_quasi_in_place(
            A, k, start=p + 1, end=end, block_size=block_size
        )
    else:
        return A[k]


if __name__ == "__main__":
    A = [int(x) for x in input().strip().split(" ")]
    k = int(input()) - 1

    print(mom_select_quasi_in_place(A, k))
