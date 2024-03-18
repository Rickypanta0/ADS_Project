from sorting import *
from Min_Max_heap import *
import math

def median_of_medians_non_in_place(lst, *, start=0, end=None, blocksize=5):
    assert lst is not None
    assert 0 <= start < len(lst)
    assert (end is None) or (start < end <= len(lst))
    assert blocksize > 0

    """Calculate approximate median of subarray lst[start:end].

        Positional arguments:
            lst      : the list to calculate the median of.
        Keyword arguments:
            start    : the starting point of the subarray; defaults to 0;
            end      : the ending point (NOT included) of the subarray; defaults
                        to the length of lst;
            blocksize: the size of the blocks of elements sorted; defaults to 5.
    """

    # Per ogni blocco b di dimensione blocksize, trova la mediana ordinandolo e
    # aggiungi la mediana a una nuova lista (medians). Effettua la ricorsione su
    # quella lista finché non rimane solo un elemento, cioè la mediana delle
    # mediane.

    if end is None:
        end = len(lst)

    subarray_length = end - start
    if subarray_length == 1:
        return start

    medians = []

    # Il numero di mediane da calcolare è dato dal rapporto tra il numero di
    # elementi del sottovettore considerato e la dimensione dei blocchi. Siccome
    # l'ultimo blocco può avere dimensione strettamente minore di blocksize, si
    # arrotonda per eccesso.
    n_medians = math.ceil(subarray_length / blocksize)
    for i in range(n_medians):
        block_start = start + i * blocksize
        block_end = min(block_start + blocksize, end)
        insertionsort(lst, start=block_start, end=block_end)
        median_position = (block_start + block_end) // 2
        medians.append(lst[median_position])

    return median_of_medians_non_in_place(medians, blocksize=blocksize)



def median_of_medians_quasi_in_place(lst, *, start=0, end=None, blocksize=5):
    assert lst is not None
    assert 0 <= start < len(lst)
    assert (end is None) or (start < end <= len(lst))
    assert blocksize > 0

    """Calculate approximate median of subarray lst[start:end].

        Positional arguments:
            lst      : the list to calculate the median of.
        Keyword arguments:
            start    : the starting point of the subarray; defaults to 0;
            end      : the ending point (NOT included) of the subarray; defaults
                        to the length of lst;
            blocksize: the size of the blocks of elements sorted; defaults to 5.
    """

    # Per ogni blocco b di dimensione blocksize, trova la mediana ordinandolo e
    # sposta la mediana all'inizio del sottovettore. Effettua la ricorsione su
    # sulla parte iniziale del sottovettore, finché il sottovettore considerato
    # ha dimensione 1, cioè quando contiene solo la mediana delle mediane.

    if end is None:
        end = len(lst)

    subarray_length = end - start
    if subarray_length == 1:
        return start

    # Il numero di mediane da calcolare è dato dal rapporto tra il numero di
    # elementi del sottovettore considerato e la dimensione dei blocchi. Siccome
    # l'ultimo blocco può avere dimensione strettamente minore di blocksize, si
    # arrotonda per eccesso.
    n_medians = math.ceil(subarray_length / blocksize)
    for i in range(n_medians):
        block_start = start + i * blocksize
        block_end = min(block_start + blocksize, end)
        insertionsort(lst, start=block_start, end=block_end)
        median_position = (block_start + block_end) // 2
        lst[start+i], lst[median_position] = lst[median_position], lst[start+i]

    # Dato che le mediane vengono sempre spostate nella parte iniziale del
    # sottovettore start rimane inalterato; invece end diventa start+n_medians
    # perché sono state spostate esattamente n_medians mediane e quindi la parte
    # iniziale contenente le mediane è lunga n_medians.
    return median_of_medians_quasi_in_place(lst, start=start,
                                            end=start+n_medians,
                                            blocksize=blocksize)



def median_of_medians_in_place(lst, *, start=0, end=None, blocksize=5):
    assert lst is not None
    assert 0 <= start < len(lst)
    assert (end is None) or (start < end <= len(lst))
    assert blocksize > 0

    """Calculate approximate median of subarray lst[start:end].

        Positional arguments:
            lst      : the list to calculate the median of.
        Keyword arguments:
            start    : the starting point of the subarray; defaults to 0;
            end      : the ending point (NOT included) of the subarray; defaults
                        to the length of lst;
            blocksize: the size of the blocks of elements sorted; defaults to 5.
    """

    # Versione iterativa di median_of_medians_quasi_in_place,

    if end is None:
        end = len(lst)

    while (subarray_length := end - start) > 1:
        # Il numero di mediane da calcolare è dato dal rapporto tra il numero di
        # elementi del sottovettore considerato e la dimensione dei blocchi. Siccome
        # l'ultimo blocco può avere dimensione strettamente minore di blocksize, si
        # arrotonda per eccesso.
        n_medians = math.ceil(subarray_length / blocksize)
        for i in range(n_medians):
            block_start = start + i * blocksize
            block_end = min(block_start + blocksize, end)
            insertionsort(lst, start=block_start, end=block_end)
            median_position = (block_start + block_end) // 2
            lst[start+i], lst[median_position] = lst[median_position], lst[start+i]
        end = start + n_medians # vedi commento nella versione quasi in-place

    assert subarray_length == 1 # guardia nel caso in cui il ciclo dovesse
                                # finire con subarray_length < 0
    return start


def select(lst, k, *, start=0, end=None):
    """Select the kth smallest element in lst."""
    assert lst is not None
    assert 0 <= k < len(lst)
    assert 0 <= start < len(lst)
    assert end is None or start < end <= len(lst)

    if end is None:
        end = len(lst)

    median_of_medians_quasi_in_place(lst, start=start, end=end)
    p = partition(lst, start=start, end=end, ppos=start)

    if p == k:
        return lst[k]
    elif p > k:
        return select(lst, k, start=start, end=p)
    else:
        return select(lst, k, start=p + 1, end=end)

def median_of_medians_Place(A, i, start=0, end=None):
    if end is None:
        end = len(A)
    if end - start <= 5:
        end=min(len(A), end+1)
        A[start:end] = sorted(A[start:end])  # Ordina se meno di 5 elementi
        return A[i+start]  # Restituisce l'i-esimo elemento
    
    # Step 1: Organizza le mediane dei blocchi di 5 all'inizio dell'array
    medians_index = start
    for sub_start in range(start, end, 5):
        median_pos = insertion_sort_5(A, sub_start, min(end, sub_start+4))
        A[medians_index], A[median_pos] = A[median_pos], A[medians_index]
        medians_index += 1
    
    # Step 2: Trova la mediana delle mediane utilizzando la stessa funzione ricorsiva
    mid = math.ceil((medians_index-start)//2)
    pivot = median_of_medians_Place(A, mid, start, medians_index-1)
    # Step 3: Usa il pivot per partizionare l'array
    pivot_position = start + A[start:end].index(pivot)
    pivot_index = partitionT(A, start=start, end=end, ppos=pivot_position)

    # Step 4: Ricorsione sul partizionamento corretto
    if i < pivot_index - start:
        #min(i,pivot_index-2) questo perchè mi andava a selezionare un elemento all'esterno
        #dell'intervallo desiderato
        return median_of_medians_Place(A,i, start, pivot_index-1)
    elif i > pivot_index - start:
        return median_of_medians_Place(A, i - (pivot_index - start + 1), pivot_index + 1, end)
    else:  # i == pivot_index - start
        return A[pivot_index]

# Esempio di utilizzo:
#print(median_of_medians_Place(A, len(A)//2))
#print(median_of_medians_Place(B, 4,start=0,end=6))

def Heap_select(A,k):
    if k<=(len(A)//2):
        H1 = MinHeap(A)
        H1.Build_Heap()
        H2 = MinHeap()
    else:
        H1 = MaxHeap(A)
        H1.Build_Heap()
        k=len(A)-k+1
        H2 = MaxHeap()
    H2.Heap_Insert(H1.A[0])
    for i in range(0, k-1):
        root = H2.Heap_Extract()
        left=H1.left(i)
        right=H1.right(i)
        if left<=H1.heapsize:
            H2.Heap_Insert(H1.A[left])
        if right<=H1.heapsize:
            H2.Heap_Insert(H1.A[right])
    return H2.Heap_Extract()

#Esempio funzionamento
#print(Heap_select(A,4))
#print(sorted(A))

def QuickSelectVariant(A,k,start=0,end=None):
    if end is None:
        end=len(A)
    if k-1<start or k-1>end or start > end:
        return -float('inf')
    else:
        #return selectT(A,k-1,p,q)  
        return select(A,k-1,start=start,end=end)

#Esempio funzionamento
C = [1,1,1,1,1,1,1,1]
A=[3, 6, 10, 7, 6, 1, 4]
B=[58, 84, 23, 63, 95, 8, 36, 47, 41, 75, 51, 50, 65, 34, 56, 33, 55, 26, 1, 68,24,22,32,10]
#print(median_of_mediansT(B,len(B)//2))
#print(median_of_medians_Place(B,len(B)//2))
#print(sorted(B))
#print(median_of_mediansT(A,len(A)//2))
#print(median_of_medians_Place(A,len(A)//2))
#print(median_of_medians_Place(C,len(C)//2))
