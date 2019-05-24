import unittest

import numpy as np

from comparator.single_domain import (
    SingleDomainComparator,
    TimeDomainComparator,
    FrequencyDomainComparator
)


class TestSingleDomainComparator(unittest.TestCase):

    def setUp(self):
        self.comp_time = SingleDomainComparator("time")
        self.comp_freq = SingleDomainComparator(
            "freq",
            forward_transform=np.fft.fft,
            inverse_transform=np.fft.ifft
        )

    def test_get_operator_products(self):

        n_arrays = 3
        arrays = [np.random.rand(4) for i in range(n_arrays)]
        res_op, res_prod = self.comp_time.get_operator_products(
            lambda a: a, arrays)
        for i in range(n_arrays):
            self.assertTrue(
                np.allclose(res_op[i], arrays[i]))
        res_op, res_prod = self.comp_time.get_operator_products(
            lambda a, b: a + b, arrays)
        for i in range(n_arrays):
            for j in range(n_arrays):
                self.assertTrue(
                    np.allclose(res_op[i][j], arrays[i] + arrays[j]))

    def test_set_operator(self):
        self.comp_time.operators["diff"] = \
            lambda a, b: np.abs(a - b)
        self.assertTrue("diff" in self.comp_time._operators)

    def test_set_product(self):
        self.comp_time.products["mean"] = np.mean
        self.assertTrue("mean" in self.comp_time._products)

    def test_set_domain(self):
        n = 100
        self.comp_time.domain = [0, n]
        self.assertTrue(
            self.comp_time.domain(n).start == 0)
        self.assertTrue(
            self.comp_time.domain(n).stop == n)

        self.comp_time.domain = slice(0, None)
        self.assertTrue(
            self.comp_time.domain(n).start == 0)
        self.assertTrue(
            self.comp_time.domain(n).stop is None)

        self.comp_time.domain = [0.1, 0.9]
        self.assertTrue(
            self.comp_time.domain(n).start == int(0.1*n))
        self.assertTrue(
            self.comp_time.domain(n).stop == int(0.9*n))

    def test_transform(self):
        a, b, c = [np.arange(10 + i) for i in range(3)]
        transformed = self.comp_time.transform(a, b, c)
        self.assertTrue(len(transformed) == 3)
        self.assertTrue(all([a.shape[0] == 10 for a in transformed]))

        transformed = self.comp_freq.transform(a, b, c)
        self.assertTrue(np.allclose(transformed[0], np.fft.fft(a)))

    def test_call(self):
        comp_time, comp_freq = self.comp_time, \
            self.comp_freq

        def test_res(self, comparator_result_tuple, nelem, iscomplex):
            self.assertTrue(isinstance(comparator_result_tuple, tuple))
            for obj in comparator_result_tuple:
                self.assertTrue("diff" in obj)
                self.assertTrue(len(obj["diff"]) == nelem)
                self.assertTrue(len(obj["diff"][0]) == nelem)
            res_op, res_prod = comparator_result_tuple
            self.assertTrue(
                np.iscomplexobj(res_op["diff"][0]) == iscomplex)
            self.assertTrue(
                np.iscomplexobj(res_prod["diff"]["mean"][0]) == iscomplex)

        comp_time.operators["diff"] = lambda a, b: a - b
        comp_time.products["mean"] = np.mean
        comp_freq.operators["diff"] = lambda a, b: a - b
        comp_freq.products["mean"] = np.mean

        # test with real data
        nelem = 3
        test_real = [np.random.rand(4) for i in range(nelem)]
        test_res(self, comp_time(*test_real), nelem, False)
        test_res(self, comp_freq(*test_real), nelem, True)

        # test with complex data
        test_complex = [np.random.rand(10) + 1j*np.random.rand(10)
                        for i in range(nelem)]

        test_res(self, comp_time(*test_complex), nelem, True)
        test_res(self, comp_freq(*test_complex), nelem, True)
        test_res(self, comp_time(*test_complex), nelem, True)
        test_res(self, comp_freq(*test_complex), nelem, True)


class TestTimeDomainComparator(unittest.TestCase):

    def setUp(self):
        self.comp = TimeDomainComparator()

    def test_get_time_delay(self):
        # x = np.linspace(0, 2*pi, 100)
        offset_expected = 2
        x = np.arange(0, 100)
        a, b = np.sin(x), np.sin(x + offset_expected)
        offset = self.comp.get_time_delay(a, b)
        self.assertTrue(offset == offset_expected)


class TestFrequencyDomainComparator(unittest.TestCase):

    def test_init(self):
        FrequencyDomainComparator()


if __name__ == "__main__":
    unittest.main()
