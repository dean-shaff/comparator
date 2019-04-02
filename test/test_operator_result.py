import unittest
import logging
import json
import os

from comparator.operator_result import (
    ComparatorOperatorResult
)

test_dir = os.path.dirname(os.path.abspath(__file__))
test_data_file_path = os.path.join(test_dir, "test_operator_result.json")


class TestComparatorOperatorResult(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(test_data_file_path, "r") as f:
            result = json.load(f)

        cls.result_one_arg = ComparatorOperatorResult(result=result["this"])
        cls.result_two_arg = ComparatorOperatorResult(result=result["diff"])

    def test_getitem(self):

        # should be able to get with an index
        test_val = self.result_one_arg[0]
        test_val = self.result_two_arg[0]

        # should be able to get with a tuple
        test_val = self.result_one_arg[0, 0, 0]
        self.assertFalse(hasattr(test_val, "__iter__"))
        test_val = self.result_two_arg[0, 0, 0, 0]
        self.assertFalse(hasattr(test_val, "__iter__"))

        # should raise an error if labels aren't present
        with self.assertRaises(RuntimeError):
            self.result_one_arg["one"]

        # should be able to get with a string, if labels are present
        self.result_one_arg.labels = ["one", "two", "three"]
        self.assertTrue(self.result_one_arg["one"] == self.result_one_arg[0])
        self.result_one_arg.labels = None

    def test_len(self):
        self.assertTrue(len(self.result_one_arg) == 3)
        self.assertTrue(len(self.result_two_arg) == 3)

    def test_iter(self):
        list(self.result_one_arg)
        list(self.result_two_arg)

    def test_label(self):

        with self.assertRaises(RuntimeError):
            self.result_one_arg.labels = ["one", "two"]

        with self.assertRaises(RuntimeError):
            self.result_one_arg.labels = "foo"

        test_val = ["one", "two", "three"]
        self.result_one_arg.labels = test_val
        self.assertTrue(
            all([v0 == v1 for v0, v1
                 in zip(test_val, self.result_one_arg.labels)]))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
