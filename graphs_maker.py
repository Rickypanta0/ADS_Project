import time
import random
import gc
import matplotlib.pyplot as plt
from functools import partial
import numpy as np

from momselect import mom_select_non_in_place, mom_select_quasi_in_place
from heapselect import heap_select
from quickselect import quick_select

MIN_ARRAY_LENGTH = 10**2
MAX_ARRAY_LENGTH = 10**5
MAX_VALUE = 10**5
ITERS = 10**2

RELATIVE_ERROR = 0.001


def get_timer_resolution():
    start = time.perf_counter()
    while True:
        end = time.perf_counter()
        if end != start:
            break
    return end - start


def get_minimum_measurable_time(relative_error, timer_resolution):
    return timer_resolution * (1 + 1 / relative_error)


def generate_input(n, max_value):
    return [random.randint(0, max_value) for _ in range(n)]


def generate_input_worst_case_quick_select(n, max_value):
    return sorted([random.randint(0, max_value) for _ in range(n)])


def benchmark(
    algorithm,
    array_length,
    max_value,
    k_value,
    minimum_measurable_time,
    input_function,
):
    """
    Misura il tempo richiesto dall'algoritmo per eseguire, assicurando
    che sia maggiore o uguale al tempo minimo misurabile.

    Argomenti:
    - algorithm               : l'algoritmo di cui misurare il tempo di esecuzione
    - array_length            : la lunghezza del vettore da generare
    - max_value               : valore massimo degli interi da generare
    - k_value                 : funzione che restituisce k in base ad array_length
    - minimum_measurable_time : tempo minimo misurabile
    - input_function          : funzione che genera l'input

    Ritorna il tempo misurato.
    """

    assert algorithm is not None
    assert array_length > 0
    assert max_value > 0
    assert k_value is not None
    assert input_function is not None

    generated_input = input_function(array_length, max_value)
    i = 0
    k = k_value(array_length) - 1
    assert 0 <= k < array_length
    if gc.isenabled():
        gc.disable()
    start_time = time.perf_counter()
    while ((end_time := time.perf_counter()) - start_time) < minimum_measurable_time:
        algorithm(generated_input.copy(), k)
        i += 1
    if not gc.isenabled():
        gc.enable()
    assert i != 0
    return (end_time - start_time) / i


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
    """
    Calcola i tempi di esecuzione degli algoritmi in input.

    Argomenti:
    - name              : nome della computazione
    - algorithms        : lista degli algoritmi da misurare
    - k_value           : funzione che restituisce k in base alla lunghezza del vettore
    - iters             : numero di iterazioni (= di punti) da calcolare
    - min_array_length  : lunghezza minima dei vettori
    - max_array_length  : lunghezza massima dei vettori
    - max_value         : valore massimo degli interi da generare
    - input_function    : funzione che genera l'input

    Ritorna una lista lunga iters in cui ogni elemento è una lista tale che il primo
        elemento è la lunghezza del vettore generato e gli altri elementi sono i tempi di
        esecuzione degli algoritmi, nell'ordine in si trovano in algorithms.
    """
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
    """
    Fa un grafico dei punti.
    """

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
    algorithms=(mom_select_quasi_in_place, heap_select, quick_select),
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
        (mom_select_quasi_in_place, heap_select, quick_select),
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
        [mom_select_quasi_in_place, heap_select, quick_select],
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
        [mom_select_quasi_in_place, heap_select, quick_select],
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
        (mom_select_quasi_in_place, mom_select_non_in_place),
        k_value=lambda n: n // 2,
    )
    plot_points(
        points_mom,
        ("MoM quasi in-place", "MoM non in-place"),
        "Confronto tra MoM con k=n/2",
        "Lunghezza vettore (lineare)",
        "Tempo (s) (lineare)",
    )
    plot_points(
        points_mom,
        ("MoM quasi in-place", "MoM non in-place"),
        "Confronto tra MoM con k=n/2",
        "Lunghezza vettore (log)",
        "Tempo (s) (log)",
        log_scale=True,
    )


def plot_worst_case_quick_select():
    points_worst_case_quick_select = compute_points(
        "Caso peggiore quick select",
        [mom_select_quasi_in_place, heap_select, quick_select],
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
        "Indice k (lineare)",
        "Tempo (s) (lineare)",
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

    ##Caso k=n/2
    # plot_middle()

    ##Caso k=n
    # plot_extreme()

    ##Caso k random
    # plot_random()

    # Confronto MoM
    # plot_mom()

    ##Caso peggiore per quick select
    ##In questo caso la lunghezza massima del vettore è 10000
    ##perché altrimenti le misurazione richiedono troppo tempo
    ##N.B. molto lento
    # plot_worst_case_quick_select()

    ##Caso n fissato k variato
    # plot_var_k()
    pass
