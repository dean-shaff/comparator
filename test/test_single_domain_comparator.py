import unittest

import numpy as np

from comparator.single_domain import SingleDomainComparator


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
        self.assertTrue("mean" in res)
        self.assertTrue("max" in res)
        self.assertTrue(res["mean"] == np.mean(a))
        self.assertTrue(res["max"] == np.amax(a))

    def test_compare(self):
        a = np.random.rand(10)
        b = np.random.rand(10)
        self.comparator_time_domain.operators["diff"] = \
            lambda a, b: np.abs(a - b)
        self.comparator_time_domain.products["mean"] = np.mean
        self.comparator_time_domain.products["max"] = np.amax

        res = self.comparator_time_domain.compare(a, b)
        self.assertTrue("diff" in res)
        self.assertTrue(np.allclose(np.abs(a - b), res["diff"][0]))

    def test_transform(self):
        a, b, c = [np.arange(10 + i) for i in range(3)]
        transformed = self.comparator_time_domain.transform(a, b, c)
        self.assertTrue(len(transformed) == 3)
        self.assertTrue(all([a.shape[0] == 10 for a in transformed]))

        transformed = self.comparator_freq_domain.transform(a, b, c)
        self.assertTrue(np.allclose(transformed[0], np.fft.fft(a)))

    def test_call(self):
        self.comparator_time_domain.operators["diff"] = \
            lambda a, b: np.abs(a - b)
        self.comparator_time_domain.products["mean"] = np.mean
        self.comparator_freq_domain.operators["diff"] = \
            lambda a, b: np.abs(a - b)
        self.comparator_freq_domain.products["mean"] = np.mean
        # test with real data
        a, b, c = [np.random.rand(10) for i in range(3)]
        res_time_real = self.comparator_time_domain(a, b, c)
        res_freq_real = self.comparator_freq_domain(a, b, c)

        # # test with complex data
        d, e, f = [np.random.rand(10) + 1j*np.random.rand(10)
                   for i in range(3)]
        res_time_polar = self.comparator_time_domain.polar(a, b, c)
        res_freq_polar = self.comparator_freq_domain.polar(a, b, c)

        res_time_cart = self.comparator_time_domain.cartesian(a, b, c)
        res_freq_cart = self.comparator_freq_domain.cartesian(a, b, c)


if __name__ == "__main__":
    unittest.main()
