from math import ceil
from functools import partial

from sorting import partition, insertionsort
from Min_Max_heap import MinHeap, MaxHeap


def heap_select(A, k):
    if k <= (len(A) // 2):
        H1 = MinHeap(A)
        H1.Build_Heap()
        H2 = MinHeap()
    else:
        H1 = MaxHeap(A)
        H1.Build_Heap()
        k = len(A) - k + 1
        H2 = MaxHeap()
    H2.Heap_Insert(H1.A[0])

    for i in range(k - 1):
        H2.Heap_Extract()
        left = H1.left(i)
        right = H1.right(i)
        if left <= H1.heapsize:
            H2.Heap_Insert(H1.A[left])
        if right <= H1.heapsize:
            H2.Heap_Insert(H1.A[right])
    return H2.Heap_Extract()


def median_of_medians_non_in_place(A, *, start=0, end=None, blocksize=5):
    assert A is not None
    assert 0 <= start < len(A)
    assert (end is None) or (start < end <= len(A))
    assert blocksize > 0

    """Calculate an approximate median of subarray A[start:end).

        Positional arguments:
            A      : the list to calculate the median of.
        Keyword arguments:
            start    : the starting point of the subarray; defaults to 0;
            end      : the ending point (NOT included) of the subarray;
                        defaults to the length of A;
            blocksize: the size of the blocks of elements sorted; default
                        to 5.

        Return:
            the median of medians.
    """

    # Per ogni blocco di dimensione blocksize, trova la mediana ordinandolo e
    # aggiungi la mediana a una nuova lista (medians). Effettua la ricorsione
    # su quella lista finché non rimane solo un elemento, cioè la mediana delle
    # mediane.

    if end is None:
        end = len(A)

    subarray_length = end - start
    if subarray_length == 1:
        return A[start]

    medians = []

    # Il numero di mediane da calcolare è dato dal rapporto tra il numero di
    # elementi del sottovettore considerato e la dimensione dei blocchi.
    # Siccome l'ultimo blocco può avere dimensione strettamente minore di
    # blocksize, si arrotonda per eccesso.
    n_medians = ceil(subarray_length / blocksize)
    for i in range(n_medians):
        block_start = start + i * blocksize
        block_end = min(block_start + blocksize, end)
        insertionsort(A, start=block_start, end=block_end)
        median_position = (block_start + block_end) // 2
        medians.append(A[median_position])

    return median_of_medians_non_in_place(medians, blocksize=blocksize)


def median_of_medians_quasi_in_place(A, *, start=0, end=None, blocksize=5):
    assert A is not None
    assert 0 <= start < len(A)
    assert (end is None) or (start < end <= len(A))
    assert blocksize > 0

    """Calculate an approximate median of subarray A[start:end).

        Positional arguments:
            A      : the list to calculate the median of.
        Keyword arguments:
            start    : the starting point of the subarray; defaults to 0;
            end      : the ending point (NOT included) of the subarray;
                        defaults to the length of A;
            blocksize: the size of the blocks of elements sorted; defaults
                        to 5.

        Return:
            the position of the median of medians.
    """

    # Per ogni blocco di dimensione blocksize, trova la mediana ordinandolo e
    # sposta la mediana verso l'inizio del sottovettore. Effettua la ricorsione
    # su sulla parte iniziale del sottovettore finché il sottovettore
    # considerato non ha dimensione 1, cioè quando contiene solo la mediana
    # delle mediane.

    if end is None:
        end = len(A)

    subarray_length = end - start
    if subarray_length == 1:
        return start

    # Il numero di mediane da calcolare è dato dal rapporto tra il numero di
    # elementi del sottovettore considerato e la dimensione dei blocchi.
    # Siccome l'ultimo blocco può avere dimensione strettamente minore di
    # blocksize, si arrotonda per eccesso.
    n_medians = ceil(subarray_length / blocksize)
    for i in range(n_medians):
        block_start = start + i * blocksize
        block_end = min(block_start + blocksize, end)
        insertionsort(A, start=block_start, end=block_end)
        median_position = (block_start + block_end) // 2
        A[start + i], A[median_position] = A[median_position], A[start + i]

    # Dato che le mediane vengono sempre spostate nella parte iniziale del
    # sottovettore, start rimane inalterato; invece end diventa start+n_medians
    # perché sono state spostate esattamente n_medians mediane e quindi la
    # parte iniziale contenente le mediane è lunga n_medians.
    return median_of_medians_quasi_in_place(
        A, start=start, end=start + n_medians, blocksize=blocksize
    )


def median_of_medians_in_place(A, *, start=0, end=None, blocksize=5):
    assert A is not None
    assert 0 <= start < len(A)
    assert (end is None) or (start < end <= len(A))
    assert blocksize > 0

    """Calculate an approximate median of subarray A[start:end).

        Positional arguments:
            A      : the list to calculate the median of.
        Keyword arguments:
            start    : the starting point of the subarray; defaults to 0;
            end      : the ending point (NOT included) of the subarray;
                        defaults to the length of A;
            blocksize: the size of the blocks of elements sorted; defaults
                        to 5.

        Return:
            the position of the median of medians.
    """

    # Versione iterativa di median_of_medians_quasi_in_place,

    if end is None:
        end = len(A)

    while (subarray_length := end - start) > 1:
        # Il numero di mediane da calcolare è dato dal rapporto tra il numero
        # di elementi del sottovettore considerato e la dimensione dei blocchi.
        # Siccome l'ultimo blocco può avere dimensione strettamente minore di
        # blocksize, si arrotonda per eccesso.
        n_medians = ceil(subarray_length / blocksize)
        for i in range(n_medians):
            block_start = start + i * blocksize
            block_end = min(block_start + blocksize, end)
            insertionsort(A, start=block_start, end=block_end)
            median_position = (block_start + block_end) // 2
            A[start + i], A[median_position] = A[median_position], A[start + i]
        end = start + n_medians  # vedi commento nella versione quasi in-place

    assert subarray_length == 1  # guardia nel caso in cui il ciclo dovesse
    # finire con subarray_length < 0
    return start


def select(A, k, *, start=0, end=None, pfunc):
    assert A is not None
    assert 0 <= k < len(A)
    assert 0 <= start < len(A)
    assert end is None or start < end <= len(A)
    assert pfunc is not None

    """Select the kth smallest element in list A.

        Positional arguments:
            A       : the list to search;
            k       : the position of the element to select.
        Keyword arguments:
            start   : the starting point of the portion of A to consider;
                        defaults to 0;
            end     : the ending point (NOT included) of the portion of A to
                        consider; defaults to the length of A;
            pfunc   : a function which returns the position of the pivot for
                        the partitioning; this function must accept two keyword
                        arguments: start and end.
        Return:
            the selected element.
    """

    if end is None:
        end = len(A)

    ppos = pfunc(A, start=start, end=end)
    p = partition(A, start=start, end=end, ppos=ppos)

    if p == k:
        return A[k]
    elif p > k:
        return select(A, k, start=start, end=p, pfunc=pfunc)
    else:
        return select(A, k, start=p + 1, end=end, pfunc=pfunc)


# funzione "fantoccio" che ritorna sempre end-1 (ultima posizione della lista)
# come posizione del pivot
def _standard_pfunc(A, *, start, end):
    return end - 1


# quick select si ottiene usando _standard_pfunc come funzione per trovare il
# pivot
quick_select = partial(select, pfunc=_standard_pfunc)

# medians of medians select si ottiene usando la funzione per la mediana delle
# mediane come funzione per trovare il pivot
median_of_medians_select = partial(select,
                                   pfunc=median_of_medians_quasi_in_place)
