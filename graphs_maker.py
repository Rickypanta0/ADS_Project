import time
import random
import gc

import matplotlib.pyplot as plt

from selecting import quick_select, median_of_medians_select, heap_select


def get_timer_resolution():
    """Determina la risoluzione del timer."""
    start = time.monotonic()
    while True:
        end = time.monotonic()
        if end != start:
            break
    return end - start


def get_minimum_measurable_time(relative_error, timer_resolution):
    return timer_resolution * (1 + 1 / relative_error)


def generate_input(n, max_value):
    """Genera un array di lunghezza 'n' con valori interi pseudo-casuali fino a
    'max_value'."""
    return [random.randint(0, max_value) for _ in range(n)]


def benchmark(algorithm, n, maxv, minimum_measurable_time, runs=3):
    """
    Utilizzi:
    - usare k random:
        k = random.randint(1, len(A))
        algorithm(A, k-1)
    - usare un k fisso (es. mediano):
        algorithm(A, len(A)//2)
    Commentare le linee rispettivamente a quello che si sceglie
    """
    times = []
    i = 0
    while i < runs:
        A = generate_input(n, maxv)
        # k = random.randint(1, len(A))  # Sceglie un k casuale per ogni esecuzione
        if gc.isenabled():
            gc.disable()  # disabilita il garbage collector
        start_time = time.monotonic()
        # algorithm(A, k-1)  # Passa k-1 perché l'indice parte da 0
        # algorithm(A, len(A)-1)
        algorithm(A, len(A) // 2)
        end_time = time.monotonic()
        if not gc.isenabled():
            gc.enable()  # riabilita il garbage collector
        # accetta il tempo misurato sono se è maggiore al tempo minimo
        # misurabile
        final_time = end_time - start_time
        if final_time > minimum_measurable_time:
            times.append(final_time)
            i = i + 1
    return min(times)
    # return sum(times) / len(times)


def compute_points(*, nmin, nmax, iters):
    timer_resolution = get_timer_resolution()
    minimum_measurable_time = get_minimum_measurable_time(
        0.001, timer_resolution
    )

    base_step = (nmax / nmin) ** (1 / (iters - 1))
    points = [[None, None, None, None]] * iters

    # questo ciclo serve per "scaldare i motori"
    # print("Scaldando i motori...")
    # for i in range(iters - 5, iters):
    #     n = int(nmin * base_step**i)
    #     benchmark(median_of_medians_select, n, nmax, minimum_measurable_time),
    #     benchmark(heap_select, n, nmax, minimum_measurable_time),
    #     benchmark(quick_select, n, nmax, minimum_measurable_time)

    # questo è il ciclo che calcola i tempi
    for i in range(iters):
        print(f"\r{i}", end="")
        n = int(nmin * base_step**i)
        points[i] = (
            n,
            benchmark(
                median_of_medians_select, n, nmax, minimum_measurable_time
            ),
            benchmark(heap_select, n, nmax, minimum_measurable_time),
            benchmark(quick_select, n, nmax, minimum_measurable_time),
        )

    return points


def plot(points):
    (
        n,
        times_median_of_medians_select,
        times_heap_select,
        times_quick_select,
    ) = zip(*points)

    # Grafico
    plt.figure(figsize=(10, 8))
    plt.plot(
        n,
        times_median_of_medians_select,
        "-o",
        label="Median of Medians Select",
    )
    plt.plot(n, times_heap_select, "-o", label="Heap Select")
    plt.plot(n, times_quick_select, "-o", label="Quick Select")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Array Size (n)")
    plt.ylabel("Time (seconds)")
    plt.title("Benchmarking Selection Algorithms")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    points = compute_points(nmin=1000, nmax=100000, iters=100)
    plot(points)
