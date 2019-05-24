import unittest
import logging
import json
import os

import numpy as np
import matplotlib.pyplot as plt

from comparator import util
from comparator.single_domain import SingleDomainComparator

test_dir = os.path.dirname(os.path.abspath(__file__))


class TestPlotOperatorResult(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if os.environ.get("COMPARATOR_TEST_PLOT", None):
            plt.ion()

    def setUp(self):
        self.comp = SingleDomainComparator("TestCornerPlot")
        self.n_dat = 100
        self.n_plots = 4
        self.dat_real = [np.random.rand(self.n_dat)
                         for i in range(self.n_plots)]
        self.dat_complex = [(np.random.rand(self.n_dat) +
                             1j*np.random.rand(self.n_dat))
                            for i in range(self.n_plots)]
        self.labels = [str(i) for i in range(self.n_plots)]

    @unittest.skip("")
    def test_plot_operator_result_one_argument_operator(self):
        self.comp.operators["this"] = lambda a: a

        res_op, res_prod = self.comp(*self.dat_real, labels=self.labels)
        figs, axes = util.plot_operator_result(res_op)

        res_op, res_prod = self.comp(*self.dat_complex, labels=self.labels)
        figs, axes = util.plot_operator_result(res_op)

        if os.environ.get("COMPARATOR_TEST_PLOT", None):
            plt.show()

    def test_plot_operator_result_two_argument_operator(self):

        self.comp.operators["diff"] = lambda a, b: a - b

        res_op, res_prod = self.comp(*self.dat_real, labels=self.labels)
        figs, axes = util.plot_operator_result(res_op)
        figs, axes = util.plot_operator_result(res_op, corner_plot=True)

        res_op, res_prod = self.comp(*self.dat_complex, labels=self.labels)
        figs, axes = util.plot_operator_result(res_op)
        figs, axes = util.plot_operator_result(res_op, corner_plot=True)

        if os.environ.get("COMPARATOR_TEST_PLOT", None):
            plt.show()

    def test_plot_operator_result_three_argument_operator(self):

        self.comp.operators["three_arg"] = lambda a, b, c: a + b + c

        with self.assertRaises(RuntimeError):
            res_op, res_prod = self.comp(*self.dat_real)
            figs, axes = util.plot_operator_result(res_op)

    @classmethod
    def tearDownClass(cls):
        if os.environ.get("COMPARATOR_TEST_PLOT", None):
            input(">>> ")


class TestNumpyEncoder(unittest.TestCase):

    def test_default(self):

        test = {"obj": np.arange(10)}
        expected_dumps = "{\"obj\": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}"
        test_dumps = json.dumps(test, cls=util.NumpyEncoder)
        self.assertTrue(test_dumps == expected_dumps)

    def test_default_int(self):

        test = {"obj": [np.int64(1), np.int32(1), np.int16(1), np.int8(1)]}
        expected_dumps = "{\"obj\": [1, 1, 1, 1]}"
        test_dumps = json.dumps(test, cls=util.NumpyEncoder)
        self.assertTrue(test_dumps == expected_dumps)

    def test_default_float(self):

        test = {"obj": [np.float16(1), np.float32(1), np.float16(1)]}
        expected_dumps = "{\"obj\": [1.0, 1.0, 1.0]}"
        test_dumps = json.dumps(test, cls=util.NumpyEncoder)
        self.assertTrue(test_dumps == expected_dumps)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("matplotlib").setLevel(logging.ERROR)
    unittest.main()
