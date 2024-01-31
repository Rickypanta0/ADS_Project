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
