import unittest
import json
import os

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

    def test_iter(self):
        val = list(self.res_double["argmax"])
        expected_val = [
            [[0, 0], [2027, 664], [2027, 664]],
            [[2027, 664], [0, 0], [2027, 0]],
            [[2027, 664], [2027, 0], [0, 0]]
        ]
        self.assertEqual(val, expected_val)
        with self.assertRaises(ValueError):
            list(self.res_double)

        val = list(self.res_single["argmax"])
        expected_val = [[225, 722], [2027, 1327], [2027, 1327]]
        self.assertEqual(val, expected_val)

    def test_getitem_str(self):
        val = self.res_double["argmax"]._products
        self.assertTrue(len(val) == 3)
        self.assertTrue(len(val[0]) == 3)
        self.assertTrue(len(val[0][0]) == 2)
        # self.assertEqual(val, expected_val)

    def test_getitem_tuple_int(self):
        val = self.res_double[0, 0, 0]
        expected_val = {
            "argmax": 0,
            "amplitude": 0,
            "max_power": 0,
            "total_power": 0
        }
        self.assertEqual(val, expected_val)
        expected_val = [
            {
              "argmax": 2027,
              "amplitude": 95419.15406569703,
              "max_power": 1914263848313060.5,
              "total_power": 4494238463021905
            },
            {
              "argmax": 0,
              "amplitude": 0,
              "max_power": 0,
              "total_power": 0
            }
        ]
        val = self.res_double[2, 1]
        self.assertEqual(val, expected_val)
        val = self.res_double[2, 1, 0]
        expected_val = {
          "argmax": 2027,
          "amplitude": 95419.15406569703,
          "max_power": 1914263848313060.5,
          "total_power": 4494238463021905
        }
        self.assertEqual(val, expected_val)

        val = self.res_single[0]
        expected_val = [
          {
            "argmax": 225,
            "amplitude": 1798.589342254461,
            "max_power": 3234923.622071334,
            "total_power": 4194552.109111571
          },
          {
            "argmax": 722,
            "amplitude": -0.76303198701739,
            "max_power": 9.865004202692617,
            "total_power": 10453.79011852153
          }
        ]
        self.assertEqual(val, expected_val)
        val = self.res_single[1, 1]
        expected_val = {
            "argmax": 1327,
            "amplitude": 2.2642614645301533,
            "max_power": 9.861533562929488,
            "total_power": 6925.291199628731
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

    def test_iscomplex(self):
        self.assertTrue(self.res_double.iscomplex)
        self.assertTrue(self.res_single.iscomplex)

    def test_isreal(self):
        self.assertFalse(self.res_double.isreal)
        self.assertFalse(self.res_single.isreal)

    def test_complex_dim(self):
        self.assertTrue(self.res_double.complex_dim == 2)
        self.assertTrue(self.res_single.complex_dim == 2)


if __name__ == "__main__":
    unittest.main()
