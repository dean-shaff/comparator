import unittest
import json

import numpy as np
import matplotlib.pyplot as plt

from comparator import util
from comparator.single_domain import SingleDomainComparator


class TestCornerPlot(unittest.TestCase):

    def test_corner_plot(self):

        n = 100
        n_plots = 4

        comp = SingleDomainComparator("test_corner_plot")
        comp.operators["diff"] = np.subtract
        comp.operators["mul"] = np.multiply

        # dat = [np.ones(n)*i for i in range(n_plots)]
        dat_real = [np.random.rand(n) for i in range(n_plots)]

        res_op, res_prod = comp(*dat_real)
        figs, axes = util.corner_plot(res_op)

        self.assertTrue(len(figs) == 2)
        self.assertTrue(len(axes) == 2)

        dat_complex = [np.random.rand(n) + 1j*np.random.rand(n)
                       for i in range(n_plots)]

        res_op, res_prod = comp(*dat_complex)
        figs, axes = util.corner_plot(res_op)

        self.assertTrue(len(figs) == 2)
        self.assertTrue(len(axes) == 2)

        # plt.show()


class TestNumpyEncoder(unittest.TestCase):

    def test_default(self):

        test = {"obj": np.arange(10)}
        expected_dumps = "{\"obj\": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}"
        test_dumps = json.dumps(test, cls=util.NumpyEncoder)
        self.assertTrue(test_dumps == expected_dumps)


if __name__ == "__main__":
    unittest.main()
