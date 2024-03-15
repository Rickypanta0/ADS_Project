import time
import matplotlib.pyplot as plt
from selecting import median_of_medians_Place, Heap_select, QuickSelectVariant
import time
import random
import math
from sorting import median_of_mediansT

def resolution():
    """Determina la risoluzione del timer."""
    start = time.monotonic()
    while True:
        end = time.monotonic()
        if end != start:
            break
    return end - start

def generate_input(n, max_value):
    """Genera un array di lunghezza 'n' con valori interi pseudo-casuali fino a 'max_value'."""
    return [random.randint(0, max_value) for _ in range(n)]

def benchmark(algorithm, n, maxv, resolution, runs=3):
    times = []
    for _ in range(runs):
        A = generate_input(n, maxv)
        start_time = time.monotonic()
        #print(f"Testing array (size {n}): {A}")
        algorithm(A, len(A)//2)
        end_time = time.monotonic()
        times.append(end_time - start_time)
    return sum(times) / len(times)
"""
# Parametri per il benchmarking
nmin = 100
nmax = 10000
steps = 10
maxv = 1000000
timer_resolution = resolution()
points = []

# Calcola i vari 'n' per cui eseguire il benchmark
n_values = [nmin + i*(nmax-nmin)//steps for i in range(steps + 1)]

# Benchmarking
for n in n_values:
    time_median_of_medians = benchmark(median_of_mediansT, n, maxv, timer_resolution)
    time_heap_select = benchmark(Heap_select, n, maxv, timer_resolution)
    time_quick_select_variant = benchmark(QuickSelectVariant, n, maxv, timer_resolution)
    points.append((n, time_median_of_medians, time_heap_select, time_quick_select_variant))
"""
nmin=1000
nmax=100000
iters=100
timer_resolution = resolution()
A=nmin
B=2**((math.log(nmax)-math.log(nmin))/(iters-1))
points = [[None, None,None, None,None]]*iters
for i in range(iters):
    print(f"\r{i}", end='')
    n = int(A*(B**i))
    points[i]=(n,benchmark(median_of_medians_Place, n, nmax, timer_resolution),
               benchmark(Heap_select, n, nmax, timer_resolution),
               benchmark(QuickSelectVariant, n, nmax, timer_resolution),)
# Estrai i valori per il plotting
ns, times_median_of_medians, times_heap_select, times_quick_select_variant = zip(*points)

# Grafico
plt.figure(figsize=(10, 8))
plt.plot(ns, times_median_of_medians, '-o', label='Median of Medians')
plt.plot(ns, times_heap_select, '-o', label='Heap Select')
plt.plot(ns, times_quick_select_variant, '-o', label='Quick Select Variant')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Array Size (n)')
plt.ylabel('Time (seconds)')
plt.title('Benchmarking Selection Algorithms')
plt.legend()
plt.grid(True)
plt.show()