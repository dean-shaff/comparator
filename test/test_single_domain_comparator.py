import unittest

import numpy as np

from comparator.single_domain import (
    SingleDomainComparator,
    TimeDomainComparator,
    FrequencyDomainComparator
)


class TestSingleDomainComparator(unittest.TestCase):

    def setUp(self):
        self.comparator_time_domain = SingleDomainComparator("time")
        self.comparator_freq_domain = SingleDomainComparator(
            "freq",
            forward_transform=np.fft.fft,
            inverse_transform=np.fft.ifft
        )

    def test_set_operator(self):
        self.comparator_time_domain.operators["diff"] = \
            lambda a, b: np.abs(a - b)
        self.assertTrue("diff" in self.comparator_time_domain._operators)

    def test_set_product(self):
        self.comparator_time_domain.products["mean"] = np.mean
        self.assertTrue("mean" in self.comparator_time_domain._products)

    def test_operate(self):
        a = np.random.rand(10)
        self.comparator_time_domain.products["mean"] = np.mean
        self.comparator_time_domain.products["max"] = np.amax
        res = self.comparator_time_domain.operate(a)
        self.assertTrue("mean" in res[1])
        self.assertTrue("max" in res[1])
        self.assertTrue(res[1]["mean"] == np.mean(a))
        self.assertTrue(res[1]["max"] == np.amax(a))

    def test_compare(self):
        a = np.random.rand(10)
        b = np.random.rand(10)
        self.comparator_time_domain.operators["diff"] = \
            lambda a, b: np.abs(a - b)
        self.comparator_time_domain.products["mean"] = np.mean
        self.comparator_time_domain.products["max"] = np.amax

        res = self.comparator_time_domain.compare(a, b, "diff")
        self.assertTrue(np.allclose(np.abs(a - b), res[0]))

    def test_transform(self):
        a, b, c = [np.arange(10 + i) for i in range(3)]
        transformed = self.comparator_time_domain.transform(a, b, c)
        self.assertTrue(len(transformed) == 3)
        self.assertTrue(all([a.shape[0] == 10 for a in transformed]))

        transformed = self.comparator_freq_domain.transform(a, b, c)
        self.assertTrue(np.allclose(transformed[0], np.fft.fft(a)))

    def test_call(self):
        comp_time, comp_freq = self.comparator_time_domain, \
            self.comparator_freq_domain

        def test_res(self, comparator_result_tuple, nelem, ndim):
            self.assertTrue(isinstance(comparator_result_tuple, tuple))
            for obj in comparator_result_tuple:
                self.assertTrue("diff" in obj)
                self.assertTrue(len(obj["diff"]) == nelem)
                self.assertTrue(len(obj["diff"][0]) == nelem)
                self.assertTrue(len(obj["diff"][0][0]) == ndim)

        comp_time.operators["diff"] = \
            lambda a, b: np.abs(a - b)
        comp_time.products["mean"] = np.mean
        comp_freq.operators["diff"] = \
            lambda a, b: np.abs(a - b)
        comp_freq.products["mean"] = np.mean
        # test with real data
        nelem = 3
        test_real = [np.random.rand(4) for i in range(nelem)]
        test_res(self, comp_time(*test_real), nelem, 1)
        test_res(self, self.comparator_freq_domain(*test_real), nelem, 2)

        # test with complex data
        test_complex = [np.random.rand(10) + 1j*np.random.rand(10)
                        for i in range(nelem)]

        test_res(self, comp_time.polar(*test_complex), nelem, 2)
        test_res(self, comp_freq.polar(*test_complex), nelem, 2)
        test_res(self, comp_time.cartesian(*test_complex), nelem, 2)
        test_res(self, comp_freq.cartesian(*test_complex), nelem, 2)


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
