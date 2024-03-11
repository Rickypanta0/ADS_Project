def partition(lst, *, start=0, end=None, ppos=None):
    """Partition lst.

    Positional arguments:
        lst  : the list to parition
    Keyword arguments:
        start: partition lst from this position; ignore what's before.
        end  : partition lst up until this position not included;
                defaults to the length of lst.
        ppos : use the element at this position as the pivot; default
                to the last element of lst.
    """

    if end is None:
        end = len(lst)

    if start >= end:
        return

    if ppos is None:
        ppos = end - 1

    pivot = lst[ppos]
    lst[ppos], lst[end - 1] = lst[end - 1], lst[ppos]

    # if start <= k < i then lst[k] <= pivot
    # if i < k <= j     then lst[k] > pivot

    i = start
    for j in range(start, end):
        if lst[j] <= pivot:
            lst[j], lst[i] = lst[i], lst[j]
            i = i + 1

    return i - 1


# Used in medianofmedians to sort the fixed-size lists
def insertionsort(lst, *, start=0, end=None):
    """Sort lst.

    Position arguments:
        lst  : the list to sort.
    Keyword arguments:
        start: start sorting from this position.
        end  : stop sorting at this position not included.
    """

    if end is None:
        end = len(lst)

    if start >= end:
        return

    for j in range(start, end):
        k = lst[j]
        i = j - 1
        while i >= start and k <= lst[i]:
            lst[i], lst[i + 1] = lst[i + 1], lst[i]
            i = i - 1
            
def insertion_sort_5(A, start,end):
    """Sort A from start to max(len(A),start+5)

    Args:
        A : the list to sort
        start : start sorting from this position

    Returns:
        _type_: the location of the median belong to the sublist (start+2)
    """
    end = min(end+1, len(A))
    for i in range(start, end):
        key = A[i]
        j = i - 1
        while j >= start and key < A[j]:
            A[j + 1] = A[j]
            j -= 1
        A[j + 1] = key
    return start + 2 if end>=start+4 else start+1   # posizione della mediana in un blocco di 5 elementi

def partitionT(A, start=0, end=None, ppos=None):
    """Partiziona l'array A da start a end compreso intorno all'elemento in ppos.
    Modifica l'array in place e restituisce il nuovo indice del pivot."""

    if end is None or end > len(A) - 1:
        end = len(A) - 1  # Assicura che end sia l'ultimo indice valido

    # Sposta il pivot all'ultimo elemento (se ppos non è già end)
    if ppos is not None and ppos != end:
        A[ppos], A[end] = A[end], A[ppos]
    pivot = A[end]

    i = start - 1
    for j in range(start, end):  # Cicla fino a end - 1 poiché end è ora l'ultimo elemento
        if A[j] <= pivot:
            i += 1
            A[i], A[j] = A[j], A[i]
    
    # Sposta il pivot nella sua posizione corretta
    A[i + 1], A[end] = A[end], A[i + 1]
    return i + 1  # Restituisce il nuovo indice del pivot

def median_of_medians(A, i):
    """Median of medians used for tests

    Args:
        A : array
        i : index

    Returns:
        elemento nell'indice i post ordinamento
    """
    #divide A into sublists of len 5
    sublists = [A[j:j+5] for j in range(0, len(A), 5)]
    medians = [sorted(sublist)[len(sublist)//2] for sublist in sublists]
    if len(medians) <= 5:
        pivot = sorted(medians)[len(medians)//2]
    else:
        #the pivot is the median of the medians
        pivot = median_of_medians(medians, len(medians)//2)

    #partitioning step
    low = [j for j in A if j < pivot]
    high = [j for j in A if j > pivot]

    k = len(low)
    if i < k:
        return median_of_medians(low,i)
    elif i > k:
        return median_of_medians(high,i-k-1)
    else: #pivot = k
        return pivot