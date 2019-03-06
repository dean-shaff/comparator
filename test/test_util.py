import unittest

import numpy as np

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
        dat = [np.random.rand(n) for i in range(n_plots)]

        res = comp(*dat)

        figs, axes = util.corner_plot(res)

        self.assertTrue(len(figs) == 2)
        self.assertTrue(len(axes) == 2)

        # plt.show()


if __name__ == "__main__":
    unittest.main()
