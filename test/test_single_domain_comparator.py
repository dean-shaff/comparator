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

    def test__operate(self):
        pass

    def test__transform(self):
        pass


class TestSingleDomainComparatorIntegration(unittest.TestCase):

    def test_call(self):
        pass


if __name__ == "__main__":
    unittest.main()
