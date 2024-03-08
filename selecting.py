from sorting import *


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

    m = median_of_medians(lst, start=start, end=end)
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
    if (end - start)+1 == 6:
        A[start:end+1] = sorted(A[start:end+1])
        return A[start + i]
    if end - start <= 5:
        #end=min(len(A), end+1)
        A[start:end] = sorted(A[start:end])  # Ordina se meno di 5 elementi
        return A[start + i]  # Restituisce l'i-esimo elemento
    
    # Step 1: Organizza le mediane dei blocchi di 5 all'inizio dell'array
    medians_index = start
    for sub_start in range(start, end, 5):
        median_pos = insertion_sort_5(A, sub_start)
        A[medians_index], A[median_pos] = A[median_pos], A[medians_index]
        medians_index += 1
    
    # Step 2: Trova la mediana delle mediane utilizzando la stessa funzione ricorsiva
    mid = (medians_index - start) // 2
    pivot = median_of_medians_Place(A, mid, start, medians_index)
    # Step 3: Usa il pivot per partizionare l'array
    pivot_index = partitionT(A, ppos=A.index(pivot, start, end), start=start, end=end)

    # Step 4: Ricorsione sul partizionamento corretto
    if i < pivot_index - start:
        return median_of_medians_Place(A, i, start, pivot_index-1)
    elif i > pivot_index - start:
        return median_of_medians_Place(A, i - (pivot_index - start + 1), pivot_index + 1, end)
    else:  # i == pivot_index - start
        return A[pivot_index]

# Esempio di utilizzo:
A = [1,2,3,4,5,1000,8,9,99]
print(median_of_medians_Place(A, len(A)//2))