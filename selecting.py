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
