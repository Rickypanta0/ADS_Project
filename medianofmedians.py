from sorting import insertionsort, partition


# Not in place
def medianofmedians(lst):
    """Calculate approximate median of lst."""

    BLOCKSIZE = 5

    if end is None or end > len(lst):
        end = len(lst)

    if start >= end:
        return

    if len(lst) == 0:
        return

    if len(lst) == 1:
        return lst[0]

    medians = []
    for i in range(0, end, BLOCKSIZE):
        real_end = min(i + BLOCKSIZE, len(lst))
        insertionsort(lst, start=i, end=real_end)
        median = lst[(real_end + i) // 2]
        medians.append(median)
        print("Fatto insertionsort", lst)

    return medianofmedians(medians)


def select(lst, k, start=0, end=None):
    if end is None:
        end = len(lst)

    print(f"Chiamata a select: {start} - {end}")
    if start >= end:
        return

    m = medianofmedians(lst, start=start, end=end)
    print(lst)
    mi = lst.index(m)
    print("La mediana è", m, "in posizione", mi)

    p = partition(lst, start=start, end=end, ppos=mi)
    print("Fatto partition", lst)

    if k > p:
        return select(lst, k, start=p + 1, end=end)
    elif k < p:
        return select(lst, k, start=start, end=p)
    else:
        return lst[p]


l = [5, 6, 2, 6, 2, 7, 8, 3, 5, 6, 1, 12, 7]
print(select(l, 3))
