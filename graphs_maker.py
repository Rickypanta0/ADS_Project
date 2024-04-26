import time
import random
import gc
import numpy as np
import matplotlib.pyplot as plt

from selecting import quick_select, median_of_medians_select, heap_select,median_of_medians_np,median_of_medians_p


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


def benchmark(algorithm, n, maxv, minimum_measurable_time, runs=3, iter=0, k_values=None):
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
        #if k_values is None:
        #    k = random.randint(1, len(A))
        #else:
        #    k = k_values[i % len(k_values)]
        if gc.isenabled():
            gc.disable()
        start_time = time.monotonic()
        algorithm(A, k_values-1)
        end_time = time.monotonic()
        if not gc.isenabled():
            gc.enable()
        final_time = end_time - start_time
        if final_time > minimum_measurable_time:
            times.append(final_time)
            i += 1
    return min(times)
    # return sum(times) / len(times)

def compute_points_MoM(*, nmin, nmax, iters):
    timer_resolution = get_timer_resolution()
    minimum_measurable_time = get_minimum_measurable_time(0.001, timer_resolution)

    base_step = (nmax / nmin) ** (1 / (iters - 1))
    dict={}
    points = []
    print("Fixed MoM...")
    for i in range(iters):
        print(f"\r{i}", end="")
        n = int(nmin * base_step**i)
        k_values = n // 2
        points.append((
            n,
            benchmark(median_of_medians_select, n, nmax, minimum_measurable_time, iter=i, k_values=k_values),
            benchmark(median_of_medians_np, n, nmax, minimum_measurable_time, iter=i, k_values=k_values),
            benchmark(median_of_medians_p, n, nmax, minimum_measurable_time, iter=i, k_values=k_values),
        ))
    dict["fixed"]=points
    return dict

def plotMoM(points, type_k):
    (
        n,
        times_median_of_medians_select,
        times_median_of_medians_np,
        times_median_of_medians_n,
    ) = zip(*points)

    # Grafico
    plt.figure(figsize=(15, 8))
    plt.plot(n,times_median_of_medians_select,"-o",label="Median of Medians Quasi in Place",)
    plt.plot(n, times_median_of_medians_np, "-o", label="Median of Medians Non Place")
    plt.plot(n, times_median_of_medians_n, "-o", label="Median of Medians Place")
    plt.xlabel("Array (n)")
    plt.ylabel("Time (seconds)")
    plt.title(f"Benchmarking with {type_k} index")
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(15, 8))
    plt.plot(n,times_median_of_medians_select,"-o",label="Median of Medians Quasi in Place",)
    plt.plot(n, times_median_of_medians_np, "-o", label="Median of Medians Non Place")
    plt.plot(n, times_median_of_medians_n, "-o", label="Median of Medians Place")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Array (n) (scala logaritmica)")
    plt.ylabel("Time (seconds) (scala logaritmica)")
    plt.title(f"Benchmarking with {type_k} index")
    plt.legend()
    plt.grid(True)
    plt.show()

def compute_points_k_fixed(*, nmin, nmax, iters,k_types):
    timer_resolution = get_timer_resolution()
    minimum_measurable_time = get_minimum_measurable_time(0.001, timer_resolution)

    base_step = (nmax / nmin) ** (1 / (iters - 1))
    dict={}  
    for types in k_types:
        points = []
        print(f"{types}...")
        for i in range(iters):
            print(f"\r{i}", end="")
            n = int(nmin * base_step**i)
            if types == "fixed k=n/2":
                k_values = n // 2
            elif types == "random":
                k_values = random.randint(1, n)
            elif types == "fixed-edge":
                k_values = n-1
            points.append((
                n,
                benchmark(median_of_medians_select, n, nmax, minimum_measurable_time, iter=i, k_values=k_values),
                benchmark(heap_select, n, nmax, minimum_measurable_time, iter=i, k_values=k_values),
                benchmark(quick_select, n, nmax, minimum_measurable_time, iter=i, k_values=k_values),
            ))
        dict[types]=points
        print("")
    return dict

def compute_points_n_fixed(*, nmin, nmax, iters,k_types):
    timer_resolution = get_timer_resolution()
    minimum_measurable_time = get_minimum_measurable_time(0.001, timer_resolution)

    points = [[None, None, None, None]] * iters
    n = 10000
    k_values = np.exp(np.linspace(np.log(1), np.log(np.log(n)), num=iters))
    k_values = np.ceil(n / np.exp(k_values - 1)).astype(int)[::-1]
    print(f"{k_types[0]}...")
    dict={}
    for k,i in zip(k_values, range(iters)):
        print(f"\r{i}", end="")
        points[i] = (
            k,
            benchmark(median_of_medians_select, n, nmax, minimum_measurable_time, iter=k,k_values=k),
            benchmark(heap_select, n, nmax, minimum_measurable_time, iter=k,k_values=k),
            benchmark(quick_select, n, nmax, minimum_measurable_time, iter=k,k_values=k),
        )
    dict[k_types[0]]=points
    return dict


def plot(points, type_k):
    (
        n,
        times_median_of_medians_select,
        times_heap_select,
        times_quick_select,
    ) = zip(*points)

    # Grafico
    plt.figure(figsize=(15, 8))
    plt.plot(n,times_median_of_medians_select,"-o",label="Median of Medians Select",)
    plt.plot(n, times_heap_select, "-o", label="Heap Select")
    plt.plot(n, times_quick_select, "-o", label="Quick Select")
    plt.xlabel("Array (n)")
    plt.ylabel("Time (seconds)")
    plt.title(f"Benchmarking with {type_k} index")
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
    plt.xlabel("Array (n) (scala logaritmica)")
    plt.ylabel("Time (seconds) (scala logaritmica)")
    plt.title(f"Benchmarking with {type_k} index")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    nmax=100000
    nmin=1000
    iters=100
    k_types = ["fixed k=n/2", "random","fixed-edge"]
    n_fixed = ["n=10000 whit varying k"]
    graphs=[]
    graphs.append(compute_points_k_fixed(nmin=nmin, nmax=nmax, iters=iters, k_types=k_types))
    graphs.append(compute_points_n_fixed(nmin=nmin, nmax=10000, iters=iters,k_types=n_fixed))
    print("")
    point = compute_points_MoM(nmin=nmin, nmax=nmax, iters=iters)
    for x in graphs:
        for i in x:
            plot(x[i],i)
    plotMoM(point["fixed"], "fixed")
