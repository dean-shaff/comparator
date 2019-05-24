import unittest
import json
import os
import logging

from comparator.product_result import (
    ComparatorProductResult
)

test_dir = os.path.dirname(os.path.abspath(__file__))
test_data_file_path = os.path.join(test_dir, "test_product_result.json")


class TestComparatorProductResult(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(test_data_file_path, "r") as f:
            test_data = json.load(f)

        cls.res_single = ComparatorProductResult(test_data["this"])
        cls.res_double = ComparatorProductResult(test_data["diff"])

    def test_contains(self):
        self.assertTrue("argmax" in self.res_double)
        self.assertTrue("max_power" in self.res_double)
        self.assertFalse("foo" in self.res_double)

        self.assertTrue("argmax" in self.res_single)
        self.assertTrue("max_power" in self.res_single)
        self.assertFalse("foo" in self.res_single)

    # @unittest.skip("")
    def test_iter(self):
        val = list(self.res_single)
        expected_val = [
            ("argmax", [225, 2027, 2027]),
            ("amplitude",
             [1798.589342254461, 46.61414463395067, 95465.76821033098]),
            ("max_power",
             [3234923.622071334, 456842092.67677593, 1916134616682572]),
            ("total_power",
             [4194552.109111571, 1072557111.8342557, 4498630584394866])
        ]
        self.assertTrue(json.dumps(val) == json.dumps(expected_val))

    def test_getitem_str(self):
        print("test_getitem_str")
        val = self.res_double["argmax"]
        expected_val = [
            [0, 2027, 2027],
            [2027, 0, 2027],
            [2027, 2027, 0]
        ]
        self.assertTrue(val == expected_val)

    def test_getitem_tuple_int(self):
        val = self.res_double[0, 0]
        expected_val = {
            "argmax": 0,
            "amplitude": 0,
            "max_power": 0,
            "total_power": 0
        }
        self.assertEqual(val, expected_val)
        expected_val = {
            "argmax": 2027,
            "amplitude": 95419.15406569703,
            "max_power": 1914263848313060.5,
            "total_power": 4494238463021905
        }
        val = self.res_double[2, 1]
        self.assertEqual(val, expected_val)

        val = self.res_single[0]
        expected_val = {
            "argmax": 225,
            "amplitude": 1798.589342254461,
            "max_power": 3234923.622071334,
            "total_power": 4194552.109111571
        }
        self.assertEqual(val, expected_val)
        val = self.res_single[1]
        expected_val = {
            "argmax": 2027,
            "amplitude": 46.61414463395067,
            "max_power": 456842092.67677593,
            "total_power": 1072557111.8342557
        }
        self.assertEqual(val, expected_val)

        val = self.res_double[0]
        self.assertEqual(len(val), 3)

    def test_str(self):
        """
        Doesn't actually compare to any real values (yet). Simply determines
        if str method will run.
        """
        str(self.res_double)
        str(self.res_single)
        "{:.6f}".format(self.res_single)
        "{:.4e}".format(self.res_single)

    def test_len(self):
        self.assertTrue(len(self.res_double) == 3)
        self.assertTrue(len(self.res_single) == 3)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
