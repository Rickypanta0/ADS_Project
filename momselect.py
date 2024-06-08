from selecting import median_of_medians_select

if __name__ == '__main__':
    A = [int(x) for x in input().strip().split(' ')]
    k = int(input()) - 1

    print(median_of_medians_select(A, k))

