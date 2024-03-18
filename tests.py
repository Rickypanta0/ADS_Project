# Classe per vari test

import unittest
from graphs_maker import generate_input
from selecting import select
from selecting import median_of_medians_non_in_place
from selecting import median_of_medians_quasi_in_place
from selecting import median_of_medians_in_place

class SelectTest(unittest.TestCase):

    def setUp(self):
        self.n = 1000           # grandezza del vettore da generare
        self.nmax = 100000      # numero massimo generabile
        self.generated_input = generate_input(self.n, self.nmax)
        self.sorted_input = sorted(self.generated_input)

        # usa la versione non in-place come riferimento
        self.mm = median_of_medians_non_in_place(self.generated_input.copy())

    def test_select(self):
        # controlla che select sia corretto per ogni posizione nel vettore,
        # confrontando il risultato con la stessa posizione nel vettore ordinato
        for k in range(self.n):
            with self.subTest(i=k):
                copy = self.generated_input.copy()
                self.assertEqual(select(copy, k), self.sorted_input[k])

    def test_median_of_medians_quasi_in_place(self):
        copy = self.generated_input.copy()
        mm_pos = median_of_medians_quasi_in_place(copy)
        mm = copy[mm_pos]
        self.assertEqual(mm, self.mm)

    def test_median_of_medians_in_place(self):
        copy = self.generated_input.copy()
        mm_pos = median_of_medians_in_place(copy)
        mm = copy[mm_pos]
        self.assertEqual(mm, self.mm)
