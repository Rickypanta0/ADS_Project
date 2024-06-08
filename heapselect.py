from selecting import heap_select

if __name__ == '__main__':
    A = [int(x) for x in input().strip().split(' ')]
    k = int(input()) - 1

    print(heap_select(A, k))

