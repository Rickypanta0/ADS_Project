from sorting import *
from Min_Max_heap import *
import math

def median_of_medians(lst, *, start=0, end=None):
    """Calculate approximate median of lst."""

    BLOCKSIZE = 5

    if end is None:
        end = len(lst)

    if end - start == 1:
        return lst[start]

    medians = []
    for i in range(start, end, BLOCKSIZE):
        rend = min(end, i + BLOCKSIZE)
        insertionsort(lst, start=i, end=rend)
        medians.append(lst[(i + rend) // 2])
        # print(f"Risultato insertionsort {i} - {rend}", lst)

    return median_of_medians(medians)


def select(lst, k, *, start=0, end=None):
    """Select the kth smallest element in lst."""
    assert k < len(lst)

    if end is None:
        end = len(lst)

    # print(f"Chiamata a select in {start} - {end}")

    m = median_of_medians_Place(lst,k, start=start, end=end)
    mi = lst.index(m, start, end)

    # print(f"La mediana è {m} in posizione {mi}")

    p = partition(lst, start=start, end=end, ppos=mi)

    # print("Risultato partition:", lst)
    # print("Il pivot è finito in posizione", p)

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