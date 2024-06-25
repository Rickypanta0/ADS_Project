# Classe per vari test

import unittest

from graphs_maker import generate_input
from momselect import mom_select_non_in_place, mom_select_quasi_in_place
from quickselect import quick_select
from heapselect import heap_select


class SelectTest(unittest.TestCase):

    def setUp(self):
        self.n = 1000  # grandezza del vettore da generare
        self.nmax = 100000  # numero massimo generabile
        self.generated_input = generate_input(self.n, self.nmax)
        self.sorted_input = sorted(self.generated_input)

    def test_mom_select_non_in_place(self):
        # controlla che median of medians select sia corretto per ogni posizione
        # nel vettore, confrontando il risultato con la stessa posizione nel
        # vettore ordinato
        for k in range(self.n):
            with self.subTest(i=k):
                copy = self.generated_input.copy()
                self.assertEqual(
                    mom_select_non_in_place(copy, k), self.sorted_input[k]
                )

    def test_mom_select_quasi_in_place(self):
        for k in range(self.n):
            with self.subTest(i=k):
                copy = self.generated_input.copy()
                self.assertEqual(
                    mom_select_quasi_in_place(copy, k), self.sorted_input[k]
                )

    def test_quick_select(self):
        for k in range(self.n):
            with self.subTest(i=k):
                copy = self.generated_input.copy()
                self.assertEqual(quick_select(copy, k), self.sorted_input[k])

    def test_heap_select(self):
        for k in range(self.n):
            with self.subTest(i=k):
                copy = self.generated_input.copy()
                self.assertEqual(heap_select(copy, k), self.sorted_input[k])
