import time
import random
import gc
import numpy as np
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


def benchmark(algorithm, n, maxv, minimum_measurable_time, runs=3, iter=0):
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
        # algorithm(A, len(A) // 2)
        algorithm(A, iter)
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
    minimum_measurable_time = get_minimum_measurable_time(0.001, timer_resolution)

    base_step = (nmax / nmin) ** (1 / (iters - 1))
    points = [[None, None, None, None]] * iters

    n = 10000
    base = (n - 1) ** (1 / (iters - 1))
    k_values = np.exp(np.linspace(np.log(1), np.log(np.log(n)), num=iters))
    k_values = np.ceil(n / np.exp(k_values - 1)).astype(int)
    # for k,i in zip(k_values, range(iters)):
    for i in range(iters):
        print(f"\r{i}", end="")
        # n = int(nmin * base_step**i)
        # print(k_t)
        # k = int(1 * (base ** i))
        # print(k)
        # if k > n:  # Assicurati che k non superi il massimo valore desiderato
        #    k = n
        points[i] = (
            # n,
            i * 100,
            benchmark(
                median_of_medians_select, n, nmax, minimum_measurable_time, iter=i
            ),
            benchmark(heap_select, n, nmax, minimum_measurable_time, iter=i),
            benchmark(quick_select, n, nmax, minimum_measurable_time, iter=i),
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
    plt.figure(figsize=(15, 8))
    plt.plot(
        n,
        times_median_of_medians_select,
        "-o",
        label="Median of Medians Select",
    )
    plt.plot(n, times_heap_select, "-o", label="Heap Select")
    plt.plot(n, times_quick_select, "-o", label="Quick Select")
    plt.xlabel("Indice k")
    plt.ylabel("Time (seconds)")
    plt.title("Benchmarking con n=10000 fissato e varia k")
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(15, 8))
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
    plt.xlabel("Indice k (scala logaritmica)")
    plt.ylabel("Time (seconds) (scala logaritmica)")
    plt.title("Benchmarking con n=10000 fissato e varia k")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    points = compute_points(nmin=1000, nmax=100000, iters=100)
    plot(points)
