import time
import random
import gc
import matplotlib.pyplot as plt
from functools import partial
import numpy as np

from selecting import (
    quick_select,
    median_of_medians_select,
    heap_select,
    median_of_medians_np,
    median_of_medians_p,
)

MIN_ARRAY_LENGTH = 10**2
MAX_ARRAY_LENGTH = 10**5
MAX_VALUE = 10**5
ITERS = 10**2

RELATIVE_ERROR = 0.001


def get_timer_resolution():
    """Determina la risoluzione del timer."""
    start = time.perf_counter()
    while True:
        end = time.perf_counter()
        if end != start:
            break
    return end - start


def get_minimum_measurable_time(relative_error, timer_resolution):
    return timer_resolution * (1 + 1 / relative_error)


def generate_input(n, max_value):
    """Genera un array di lunghezza 'n' con valori interi pseudo-casuali fino a
    'max_value'."""
    return [random.randint(0, max_value) for _ in range(n)]


def generate_input_worst_case_quick_select(n, max_value, reverse=False):
    """
    Genera un vettore di lunghezza n con valori interi pseudocasuali da 0 a max_value
    in ordine crescente.
    """
    return sorted([random.randint(0, max_value) for _ in range(n)], reverse=reverse)


def benchmark(
    algorithm,
    array_length,
    max_value,
    k_value,
    minimum_measurable_time,
    input_function,
    runs=3,
):
    assert algorithm is not None
    assert array_length > 0
    assert input_function is not None
    assert runs > 0

    recorded_times = []
    i = 0
    while i < runs:
        generated_input = input_function(array_length, max_value)
        if gc.isenabled():
            gc.disable()
        start_time = time.monotonic()
        k = k_value(array_length) - 1
        assert 0 <= k < array_length
        algorithm(generated_input, k)
        end_time = time.monotonic()
        if not gc.isenabled():
            gc.enable()
        elapsed_time = end_time - start_time
        # if elapsed_time > minimum_measurable_time:
        recorded_times.append(elapsed_time)
        i += 1
    return sum(recorded_times) / len(recorded_times)


def compute_points(
    name,
    algorithms,
    k_value,
    iters=ITERS,
    min_array_length=MIN_ARRAY_LENGTH,
    max_array_length=MAX_ARRAY_LENGTH,
    max_value=MAX_VALUE,
    input_function=generate_input,
):
    assert k_value is not None
    assert iters > 0
    assert 0 < min_array_length < max_array_length
    assert input_function is not None

    print("Computing " + name)

    timer_resolution = get_timer_resolution()
    minimum_measurable_time = get_minimum_measurable_time(
        RELATIVE_ERROR, timer_resolution
    )

    array_length_base_step = (max_array_length / min_array_length) ** (1 / (iters - 1))
    points = []
    for i in range(iters):
        print(f"{i}\r", end="")
        array_length = int(min_array_length * array_length_base_step**i)
        record = []
        record.append(array_length)
        for algorithm in algorithms:
            recorded_time = benchmark(
                algorithm,
                array_length,
                max_value,
                k_value,
                minimum_measurable_time,
                input_function=input_function,
            )
            record.append(recorded_time)
        points.append(record)
    return points


def plot_points(points, algorithm_names, title, xlabel, ylabel, log_scale=False):
    assert len(points[0]) - 1 == len(algorithm_names)

    coordinates = [*zip(*points)]

    plt.figure(figsize=(15, 8))
    for i, algorithm_name in enumerate(algorithm_names):
        plt.plot(coordinates[0], coordinates[i + 1], "-o", label=algorithm_name)
    plt.xlabel(xlabel, fontsize=18)
    plt.ylabel(ylabel, fontsize=18)
    plt.title(title, fontsize=22)
    plt.legend()
    plt.grid(True)
    if log_scale:
        plt.xscale("log")
        plt.yscale("log")
    plt.show()


def compute_points_n_fixed(
    *,
    n=10000,
    iters=100,
    algorithms=(median_of_medians_select, heap_select, quick_select),
    input_function=generate_input,
):
    timer_resolution = get_timer_resolution()
    minimum_measurable_time = get_minimum_measurable_time(0.001, timer_resolution)

    points = []
    k_values = np.exp(np.linspace(np.log(1), np.log(np.log(n)), num=iters))
    k_values = np.ceil(n / np.exp(k_values - 1)).astype(int)[::-1]
    print("Computing n fissato e k variato")
    for i in range(iters):
        print(f"\r{i}", end="")
        k = k_values[i]
        record = [k]
        for algorithm in algorithms:
            recorded_time = benchmark(
                algorithm,
                n,
                MAX_VALUE,
                lambda _: k,
                minimum_measurable_time,
                input_function=input_function,
            )
            record.append(recorded_time)
        points.append(record)

    return points


def plot_middle():
    points_middle = compute_points(
        "Caso k=n/2",
        (median_of_medians_select, heap_select, quick_select),
        k_value=lambda n: n // 2,
    )
    plot_points(
        points_middle,
        ("Median of medians select", "Heap select", "Quick select"),
        "Caso k=n/2",
        "Lunghezza vettore (lineare)",
        "Tempo (s) (lineare)",
    )
    plot_points(
        points_middle,
        ("Median of medians select", "Heap select", "Quick select"),
        "Caso k=n/2",
        "Lunghezza vettore (log)",
        "Tempo (s) (log)",
        log_scale=True,
    )


def plot_extreme():
    points_extreme = compute_points(
        "Caso k=n",
        [median_of_medians_select, heap_select, quick_select],
        k_value=lambda n: n,
    )
    plot_points(
        points_extreme,
        ["Median of medians select", "Heap select", "Quick select"],
        "Caso k=n",
        "Lunghezza vettore (lineare)",
        "Tempo (s) (lineare)",
    )
    plot_points(
        points_extreme,
        ["Median of medians select", "Heap select", "Quick select"],
        "Caso k=n",
        "Lunghezza vettore (log)",
        "Tempo (s) (log)",
        log_scale=True,
    )


def plot_random():
    points_random = compute_points(
        "Caso k random",
        [median_of_medians_select, heap_select, quick_select],
        k_value=lambda n: random.randint(1, n),
    )
    plot_points(
        points_random,
        ["Median of medians select", "Heap select", "Quick select"],
        "Caso k random",
        "Lunghezza vettore (lineare)",
        "Tempo (s) (lineare)",
    )
    plot_points(
        points_random,
        ["Median of medians select", "Heap select", "Quick select"],
        "Caso k random",
        "Lunghezza vettore (log)",
        "Tempo (s) (log)",
        log_scale=True,
    )


def plot_mom():
    points_mom = compute_points(
        "Confronto tra MoM con k=n/2",
        (median_of_medians_select, median_of_medians_np, median_of_medians_p),
        k_value=lambda n: n // 2,
    )
    plot_points(
        points_mom,
        ("MoM quasi in-place", "MoM non in-place", "MoM in-place"),
        "Confronto tra MoM con k=n/2",
        "Lunghezza vettore (lineare)",
        "Tempo (s) (lineare)",
    )
    plot_points(
        points_mom,
        ("MoM quasi in-place", "MoM non in-place", "MoM in-place"),
        "Confronto tra MoM con k=n/2",
        "Lunghezza vettore (log)",
        "Tempo (s) (log)",
        log_scale=True,
    )


def plot_worst_case_quick_select():
    points_worst_case_quick_select = compute_points(
        "Caso peggiore quick select",
        [median_of_medians_select, heap_select, quick_select],
        k_value=lambda n: 1,
        input_function=generate_input_worst_case_quick_select,
        max_array_length=10**4,
    )
    plot_points(
        points_worst_case_quick_select,
        ["MoM select", "Heap select", "Quick select"],
        "Caso peggiore quick select",
        "Lunghezza vettore (lineare)",
        "Tempo (s) (lineare)",
    )
    plot_points(
        points_worst_case_quick_select,
        ["MoM select", "Heap select", "Quick select"],
        "Caso peggiore quick select",
        "Lunghezza vettore (log)",
        "Tempo (s) (log)",
        log_scale=True,
    )


def plot_var_k():
    points_n_fixed_var_k = compute_points_n_fixed()
    plot_points(
        points_n_fixed_var_k,
        ["MoM select", "Heap select", "Quick select"],
        "Caso n fissato k variato",
        "Indice k (log)",
        "Tempo (s) (log)",
    )
    plot_points(
        points_n_fixed_var_k,
        ["MoM select", "Heap select", "Quick select"],
        "Caso n fissato k variato",
        "Indice k (log)",
        "Tempo (s) (log)",
        log_scale=True,
    )


if __name__ == "__main__":
    # Commentare i vari casi secondo le necessità

    # Caso k=n/2
    plot_middle()

    # Caso k=n
    plot_extreme()

    # Caso k random
    plot_random()

    # Confronto MoM
    plot_mom()

    # Caso peggiore per quick select
    # In questo caso la lunghezza massima del vettore è 10000
    # perché altrimenti le misurazione richiedono troppo tempo
    # N.B. molto lento
    #plot_worst_case_quick_select()

    # Caso n fissato k variato
    plot_var_k()
